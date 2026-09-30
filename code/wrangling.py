import os
import numpy as np
import pandas as pd


# LOAD FILES  ---------------------------------------------------------------------------------------------------------------------
def read_csv_files(filenames, filepath: str = None):
    '''Takes in a list of filenames and (optionally) path details, loads the files and returns a single merged dataset.'''
    # if single filename provided as a string, wrap it in a list
    if type(filenames) == type("A string"):
        filenames = [filenames]

    # Capture publish date (year, month, day) from filename - ditch the non-date parts
    publish_dates = [filename.replace('.csv',"").split('_')[1:] for filename in filenames]
    
    # Prefix filenames with path, if supplied
    if filepath != None:
        if filepath[-1] == "\\":
            filepath == filepath[:-1]  #Remove slash from the end to avoid double-ups
        filepath = filepath.strip()    #Remove trailing whitespace
        filename = [filepath + "\\" + filename for filename in filenames] # Combine the file path & name
    print("\nLoading Files...", end="")
    
    # Generate a list of dataframes based on the files
    df_set = []
    for i, filename in enumerate(filenames):
        raw_data = pd.read_csv(filename)
        df = pd.DataFrame(raw_data)
        df['year'], df['month'], df['day'] = publish_dates[i]    # Add new columns for publishing year and month; type conversion is handled later
        df['publish_date'] = pd.to_datetime('-'.join(publish_dates[i]), format = "%Y-%m-%d")    # Published date in datetime format
        df_set.append(df)
       
    #Merge the dataframes (recomputing row indices) then return results; should handle mild column differences automatically
    merged_df = pd.concat(df_set, ignore_index=True)
    print(" Loading complete.")   
    return merged_df


def read_bond_file(filename: str, separator):
    '''Reads the masterfile & converts necessary column data from strings to integers/floats.'''
    print(".", end="")
    if separator == ";":
        df = pd.DataFrame()
        dataset = pd.read_csv(filename, sep = ";")
        df = pd.DataFrame(dataset)
    else: 
        df = pd.DataFrame()
        dataset = pd.read_csv(filename)
        df = pd.DataFrame(dataset)

    return df 


# CLEAN DATA  ---------------------------------------------------------------------------------------------------------------------
def cleaning_drop_col(df, target_columns):
    '''Return a copy of the supplied dataframe, with the specified columns removed.'''
    for col in target_columns:
        df.drop(columns=[col], inplace=True)
    print(f" Dropped {len(target_columns)} columns from the dataset: {target_columns}")
    return df

def cleaning_str_to_date(df, target_columns):
    '''Convert strings to datetime'''
    
    for col in target_columns:
        df[col] = pd.to_datetime(df[col], format='%Y-%m-%d')    #Dates in the AirBnB 'listings' files look like "2026-03-20" and "2025-12-06"
    print(f" Converted {len(target_columns)} columns from string to datetime: {target_columns}")
    return df

def cleaning_int_to_flt(df, target_columns):
    '''Convert ints to floats'''
    for col in target_columns:
        df[col] = df[col].astype(float)
    print(f" Converted {len(target_columns)} columns from int to float: {target_columns}")
    return df

def cleaning_str_to_int(df, target_columns):
    '''Convert strings to ints'''
    for col in target_columns:
        df[col] = df[col].astype(int)
    print(f" Converted {len(target_columns)} columns from string to int: {target_columns}")
    return df

def do_basic_cleaning(df):
    '''
    Wrapper function for airbnb-specific cleaning tasks:
    Return a cleaned dataset after dropping manually specified columns, performing type conversion and adding Month and Year columns.
    '''
    print("Cleaning airbnb dataset:")
    df = cleaning_drop_col(df, ['license'])
    df = cleaning_str_to_date(df, ['last_review'])
    df = cleaning_int_to_flt(df, [])    #TODO: Populate this list
    df = cleaning_str_to_int(df, [])    #TODO: Populate this list
    print("Dataset cleaned")
    return df


def clean_airbnb(df):
    # Came from the merge function, so presumably used for that somehow
    #create month ranges: MM=04 -> JAN-MAR, MM=07 -> APR-JUN, MM=10 -> JUL-SEP, MM=01 -> OCT-DEC
    df['months'] = df['month'].replace({1: "JAN-MAR", 2: "JAN-MAR", 3: "JAN-MAR", 4: "APR-JUN", 5: "APR-JUN", 6: "APR-JUN", 7: "JUL-SEP", 8: "JUL-SEP", 9: "JUL-SEP", 10: "OCT-DEC", 11: "OCT-DEC", 12: "OCT-DEC"})       
    df['months-year'] = df['months'].astype(str) + "-" + df['year'].astype(str)
    #remove all data before Q4 2025 and after Q1 2026 to match rental bond dataset
    df = df[(df['months-year'] == 'OCT-DEC-2025') | (df['months-year'] == 'JAN-MAR-2026')]
    #merge by quarters and find mean of price
    df_merge_areas = df.groupby(['year', 'months', 'area_code'], as_index=False).agg(airbnb_mean_price=('price', 'mean'),total_airbnb_properties=('price', 'count'))
    df_merge_areas = df_merge_areas.rename(columns={'area_code': 'Location Id'})
    #Preview the results
    print(df_merge_areas.head())
    df_merge_areas.to_csv("airbnb_ready_for_merge.csv", index=False)
    return df_merge_areas


def filter_locations(df):
    '''Drops all the rows which don't refer to Christchurch'''
    start_length = df.shape[0]
    neighbourhood_group_options = ["Christchurch City"]    #The locations to keep
    
    # Keep only the rows which mention the above
    df = df[df['neighbourhood_group'].isin(neighbourhood_group_options)]
    end_length = df.shape[0]

    print(f"Dropped {start_length - end_length} rows (down from {start_length} to {end_length} rows).")
    return df

def filter_timeframe(df, start_date, end_date):
    '''Drops rows which aren't inside the target date-range (inclusive).'''
    # Convert date strings to datetime format (as used in target col)
    start_date_conv = pd.to_datetime(start_date, format='%Y_%m_%d')
    end_date_conv   = pd.to_datetime(end_date, format='%Y_%m_%d')
    
    # Select and return only the rows which don't fall inside the date range
    start_length = df.shape[0]
    df = df[(df['publish_date'] >= start_date_conv) & (df['publish_date'] <= end_date_conv)]
    end_length = df.shape[0]

    # Report the actions then return
    print(f"Dropped {start_length - end_length} rows. {end_length}, remain, between {start_date} and {end_date}.")
    return df

def convert_categoricals(df):
    '''Convert string and integer variables into categorical variables; function provides all specifications so will need amending to alter expected behaviours.'''
    columns_affected = {'ordinal':[], 'nominal':[]}
    # The list of variables to be converted, and (ONLY if ordinal) the correct factor order
    conversion_variables = {
        #variableName:[isOrdinal, [Category labels in ascending order]]
        "room_type":[True, ["Shared room", "Private room", "Entire home/apt", "Hotel room"]],
        "month":[True, ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]],
        "neighbourhood_group":[False],
        "neighbourhood":[False]
    }
    # Convert the variables, ordering categories where required - check variable values with print(df[varName].unique())
    for var_name, var_details in conversion_variables.items():
        if var_details[0]:
            # Variable is ordinal - need to convert and include ordered value labels
            ord_labels = var_details[1]
            df[var_name] = pd.Categorical(df[var_name], ord_labels, ordered = True)
            columns_affected['ordinal'].append(var_name)
        else:
            # Variable is nominal - can just do basic type conversion
            df[var_name] = df[var_name].astype("category")
            columns_affected['nominal'].append(var_name)
    num_variables = len(conversion_variables.keys())
    print(f'Converted {num_variables} variable{'s' if num_variables > 1 else ""} to ordinal {columns_affected['ordinal']} or nominal {columns_affected['nominal']} categorical type.')
    return df


def clean_rental(df, df2):
    '''Cleans rental bond dataset, filters data for only Christchurch City, matched datat to Airbnb dataset'''

    #drop all Location Id = NULL
    df = df.dropna(subset=['Location Id'])

    #drop all Location Id = -99
    df = df[df['Location Id'] != -99]

    #convert Location Id from float into integer
    df['Location Id'] = df['Location Id'].astype(int)

    #convert TimeFrame from string into datetime
    df['TimeFrame'] = pd.to_datetime(df['TimeFrame'])

    #create new columns for year and month
    df['year'] = df['TimeFrame'].dt.year
    df['months'] = df['TimeFrame'].dt.month

    #create month ranges: MM=04 -> JAN-MAR, MM=07 -> APR-JUN, MM=10 -> JUL-SEP, MM=01 -> OCT-DEC
    df['months'] = df['months'].replace({4: "JAN-MAR", 7: "APR-JUN", 10: "JUL-SEP", 1: "OCT-DEC"})

    #if TimeFrame is YYYY-01-01, then year in file needs to be changed to previous year
    df.loc[df['months'] == "OCT-DEC", 'year'] = df['year'] - 1

    #remove all data prior to OCT-DEC 2025 and after JAN-MAR 2026
    #Timeframe OCT 2025 to MAR 2026 represents the timeframe, where we have complete month data for Airbnb and rental
    target_timeframes = pd.to_datetime(["2026-01-01", "2026-04-01"])
    df = df[df['TimeFrame'].isin(target_timeframes)]
    
    # Drop unnecessary columns from 'Dwelling_SA2' and deduplicate
    df2 = df2[['SA2Code', 'TAName']].drop_duplicates()

    #merge rental data with SA2 data. New columns SA2Code and TAName, when Location Id and SA2Code match
    df = df.merge(df2[['SA2Code', 'TAName']],
                  left_on= 'Location Id',
                  right_on= 'SA2Code',
                  how= 'left'
                  )

    #rename TAName column to neighbourhood_group
    df = df.rename(columns={'TAName':'neighbourhood_group'})

    #remove column SA2Code
    df = df.drop(columns=['SA2Code'])

    #remove all columns with neighbourhood_group not Christchurch City
    df = df[df['neighbourhood_group'] == "Christchurch City"]

    #rename Dwelling types to match Airbnb listings data
    dwelling_change = {
            "House": "Entire home/apt",
            "Flat": "Entire home/apt",
            "Apartment": "Entire home/apt",
            "Boarding House": "Private room",
            "Room": "Private room"}
    df['Dwelling Type'] = df['Dwelling Type'].replace(dwelling_change)

    return df


def clean_rental_MERGE(df):
    # Drop the rows which aren't Dwelling Type of 'ALL' 
    df = df[(df['Dwelling Type'] == 'ALL') & (df['Number Of Beds'] == 'ALL')]
    df['No_Rental_Properties'] = df['Total Bonds'] + df['Active Bonds'] + df['Closed Bonds']
    df.to_csv("rental_ready_for_merge.csv", index=False)
    return df
