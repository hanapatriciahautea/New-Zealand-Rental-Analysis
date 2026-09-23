import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from multiprocessing import Pool
from tqdm import tqdm
import os
import numpy as np

#### Parameters and Helper Variables
err_wrap = "!!!!"

# LOAD FILES  ---------------------------------------------------------------------------------------------------------------------

def read_csv_file(filename: str):
    '''Reads the masterfile & converts necessary column data from strings to integers/floats.'''
    print(".", end="")
    df = pd.DataFrame()    #Return statement is simpler if there's always *something* to return
    #Attempt to load; return failed filename for debugging when bulk/batch loading files
    try:
        listings = pd.read_csv(filename)
        df = pd.DataFrame(listings)
    except:
        print(f"\n{err_wrap} Error loading file {filename} {err_wrap}\n")

    return df 


def read_csv_files(filenames: list[str], filepath: str = None):
    '''Wrapper function for read_csv_file() which takes in a list of filenames and (optionally) path details, returning a single merged dataset.'''
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
        df = read_csv_file(filename)
        df['year'], df['month'], df['day'] = publish_dates[i]    # Add new columns for publishing year and month; type conversion is handled later
        df['publish_date'] = pd.to_datetime('-'.join(publish_dates[i]), format = "%Y-%m-%d")    # Published date in datetime format
        df_set.append(df)
       
    #Merge the dataframes (recomputing row indices) then return results; should handle mild column differences automatically
    merged_df = pd.concat(df_set, ignore_index=True)
    print(" Loading complete.")   
    return merged_df


# CLEAN DATA  ---------------------------------------------------------------------------------------------------------------------

def do_basic_cleaning(df):
    '''Return a cleaned dataset after dropping manually specified columns, performing type conversion and adding Month and Year columns. (Wrapper for 'cleaning task')'''
    actions_taken = []    #Collects details of actions taken, for reporting when complete
    
    # Drop targeted columns
    df, action = cleaning_task(df, 'drop_col', ['license'])
    actions_taken.append(action)
    
    # Convert strings to datetime
    df, action = cleaning_task(df, 'str_to_date', ['last_review'])
    actions_taken.append(action)

    # Convert ints to floats
    df, action = cleaning_task(df, 'int_to_flt', [])    #TODO: Populate this list
    actions_taken.append(action)

    # Convert strings to ints
    df, action = cleaning_task(df, 'str_to_int', [])    #TODO: Populate this list
    actions_taken.append(action)
    
    # Report on process and return a cleaned dataset
    print("Basic data Cleaning:\n" + '\n'.join(actions_taken))
    return df


def cleaning_task(df, cleaning_mode = None, target_columns = []):
    '''Perform a single, pre-defined cleaning task, and return the dataset and a change-log.'''
    columns_affected = []    #Track which columns actually get altered

    # Make the requested change to the identified columns
    for col in target_columns:
        if col in list(df.columns):
            if cleaning_mode == 'drop_col':
                df.drop(columns=[col], inplace=True)
            elif cleaning_mode == 'str_to_date':
                df[col] = pd.to_datetime(df[col], format='%Y-%m-%d')    #Dates in the AirBnB 'listings' files look like "2026-03-20" and "2025-12-06"
            elif cleaning_mode == 'int_to_flt':
                df[col] = df[col].astype(float)
            elif cleaning_mode == 'str_to_int':
                df[col] = df[col].astype(int)
            columns_affected.append(col)  #Update the log

    # Generate report on what happened
    num_affected = len(columns_affected)
    if num_affected > 0:
        change_log = f' - {cleaning_mode} on {num_affected} column{'s' if num_affected > 1 else ""} {columns_affected}'
    else:
        change_log = f' - No {cleaning_mode} performed'
    
    return df, change_log


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


# SUMMARY STATS  -----------------------------------------------------------------------------------------------------------------

def summary_stats(df):
    '''
    Prints summary statistics of the compiled masterfile.
    '''
    # Describe the df
    print("\033[1m" + "\n Number of rows and columns in the dataframe " + "\033[0m") #  "\033[1m" and "\033[0m" are to indicate bold formatting
    print(df.shape) 

    print("\033[1m" + "\n Column names" + "\033[0m")
    print(df.columns) 

    print("\033[1m" + "\n Number of missing values per column" + "\033[0m")
    print(df.isnull().sum()) 

    print("\033[1m" + "\n Descriptive statistics of dataset" + "\033[0m")
    print(df.describe())

    print("\033[1m" + "\n Data types per column" + "\033[0m")
    print(df.dtypes)   
    
# VISUALISATIONS  ----------------------------------------------------------------------------------------------------------------

# Plot 1: Histogram of distribution of prices
def hist_prices(df):
    '''
    Prints a histogram of the distribution of Airbnb listing prices in Christchurch city.
    '''
    # First subplot - excluding outliers (99th percentile)
    threshold = df['price'].quantile(0.99)
    df_filtered = df[df['price'] < threshold]

    fig, axs = plt.subplots(2, 1, figsize=(10, 10))
    
    sns.histplot(df_filtered['price'], bins = 30, kde = True, ax = axs[0])
    axs[0].set_title('Distribution of Price (excluding outliers - 99th percentile cutoff)')
    axs[0].set_xlabel('Price')
    axs[0].set_ylabel('Count (# of listings)')

    # Second subplot - including outliers
    sns.histplot(df['price'], bins = 30, kde = True, ax = axs[1])
    axs[1].set_title('Distribution of Price (including outliers)')
    axs[1].set_xlabel('Price')
    axs[1].set_ylabel('Count (# of listings)')

    plt.tight_layout()  # prevents titles/labels from overlapping between subplots
    plt.show()


# Plot 2: Days since last review (scrape/publish date vs last review date)
def hist_dates(df):
    '''
    Visualising the distribution of the number of days since the last review.
    '''
    df['last_review'] = pd.to_datetime(df['last_review'])
    df['publish_date'] = pd.to_datetime(df['publish_date'])

    df['days_since_last_review'] = df['publish_date'] - df['last_review']
    df['days_since_last_review'] = (df['days_since_last_review'].dt.total_seconds() / (24 * 60 * 60))

    fig, axs = plt.subplots(2, 1, figsize=(10, 10))

    # Filtering out negative date differences that occur after the publish date
    df_no_negatives = df[df['days_since_last_review'] >= 0]

    # Confirmation that the graph filters out negative date differences
    print(f"Total rows: {len(df)}")
    print(f"Rows with negative days_since_last_review: {(df['days_since_last_review'] < 0).sum()}")
    print(f"Rows after filtering: {len(df_no_negatives)}")

    # First subplot - excluding outliers (99th percentile)
    threshold = df_no_negatives['days_since_last_review'].quantile(0.99)
    df_filtered = df_no_negatives[df_no_negatives['days_since_last_review'] < threshold]
    sns.histplot(df_filtered['days_since_last_review'], bins = 30, kde = True, ax = axs[0])
    axs[0].set_title('Days since last review (excluding outliers - 99th percentile cutoff)')
    axs[0].set_xlabel('Days')
    axs[0].set_ylabel('Count (# of listings)')

    # Second subplot - including outliers
    sns.histplot(df_no_negatives['days_since_last_review'], bins = 30, kde = True, ax = axs[1])
    axs[1].set_title('Days since last review (including outliers)')
    axs[1].set_xlabel('Days')
    axs[1].set_ylabel('Count (# of listings)')

    plt.tight_layout()  # prevents titles/labels from overlapping between subplots
    plt.show()    


# Plot 3: Top 10% of properties in Christchurch with highest numbers of reviews
def top_10_reviews(df):
    '''
    Print the top 10% of properties in Christchurch with highest number of reviews.
    '''
    df_sorted = df.sort_values(by='number_of_reviews', ascending = False)
    top_10_percent = df_sorted.head(int(len(df_sorted) * 0.1))

    display_df = top_10_percent[['id', 'name', 'number_of_reviews', 'publish_date']].rename(columns={'id': 'ID', 'name':'Name of Listing', 'number_of_reviews': 'Number of Reviews', 'publish_date':'Publish Date'})
    display_df['Rank'] = top_10_percent['number_of_reviews'].rank(ascending = False, method='min').astype(int) # using min method to tie values at the lowest possible rank, reasonable for ranking reviews
    print(display_df)

    # To view the full table, you can uncomment the following lines to export to CSV
    # display_df.to_csv('top_10_percent_listings.csv', index=False)


def option_selection(options):
    '''
    Ask the user to select an option from a list of options.
    '''
    prompt = 'Please select an option: '
    i = 0
    print()    #Insert a blank line above the options, for readability
    while i < len(options):
        print(f'{i} {options[i]}')
        i += 1
    
    print('-' * (len(prompt)-1))    #Print a line above where the prompt will appear
    selection = int(input(prompt))
    while selection < 0 or selection >= len(options):
        print(f'\n{err_wrap} {selection} is not a valid input. Try again. {err_wrap}\n')
        selection = int(input(prompt))
    return selection

# GETTING AREA CODES VIA API KEY -------------------------------------------------------------------------------------------------
def get_area_code(lat, lon, api_key, layer_id):
    '''
    Queries the Koordinates API for a single latitude/longitude pair and returns the matching area code.
    '''
    url = "https://koordinates.com/services/query/v1/vector.json"
    params = {
        "key": api_key,
        "layer": layer_id,
        "x": lon,
        "y": lat,
        "max_results": 1,
        "radius": 1000,
        "with_field_names": "true"
    }
    try:
        response = requests.get(url, params = params)
        response.raise_for_status()
        data = response.json()
        features = data['vectorQuery']['layers'][str(layer_id)]['features']
        if not features:
            return None # if no match is found within the radius
        return features[0]['properties']['SA22019_V1_00'] # extract the area code field
    except Exception as e:
        print(f"Error for lat={lat}, lon={lon}: {e}")
        return None

def query_wrapper(args):
    '''
    Helper function so multiprocessing.Pool can pass multiple arguments using .imap().
    '''
    lat, lon, api_key, layer_id = args
    return get_area_code(lat, lon, api_key, layer_id)

def add_area_codes(df, api_key, layer_id, output_path='listings_with_area_codes.csv'):
    '''
    Adds a column for area code to the dataframe from querying a Koordinates API for each Airbnb listing's latitude and longitude
    using multiprocessing & saves the result to a CSV file.
    '''
    # adding a safeguard to prevent re-running the API call
    if os.path.exists(output_path):
        return pd.read_csv(output_path)
    
    else:
        print(f"No existing file has been found. Running API queries for {len(df)} rows...")

        # build list of arguments for each row
        tasks = [(row['latitude'], row['longitude'], api_key, layer_id) for _, row in df.iterrows()]

        results = []
        with Pool(processes=5) as pool:
            for result in tqdm(pool.imap(query_wrapper, tasks), total=len(tasks)):
                results.append(result)

        df['area_code'] = results
        df.to_csv(output_path, index=False)
        print(f"The results have been saved to {output_path}.")
        return df

#  ADDING WARD CODES -------------------------------------------------------------------------------------------------------------------------------
def add_ward_codes(df, ward_concordance_path='meshblock_2019_to_ward_2019.xlsx', 
                   sa2_concordance_path='meshblock_2019_to_sa2_2019.xlsx', output_path='listings_with_area_codes.csv'):
    '''
    Groups SA2 area codes into Ward areas by joining two Stats NZ meshblock files (Meshblock-to-Ward and Meshblock-to-SA2),
    then merging the resulting SA2-to-Ward onto the Airbnb dataframe using 'area_code'.
    '''
    # adding a safeguard to prevent re-merging 
    if 'ward_code' in df.columns:
        return df

    mb_to_ward = pd.read_excel(ward_concordance_path, skiprows=9)
    mb_to_sa2 = pd.read_excel(sa2_concordance_path, skiprows=9)

    # join on the shared meshblock code
    sa2_to_ward = mb_to_sa2.merge(
        mb_to_ward,
        on='Source Code',
        suffixes=('_sa2', '_ward')
    )

    sa2_to_ward = sa2_to_ward[['Target Code_sa2', 'Descriptor.1_sa2', 'Target Code_ward', 'Descriptor.1_ward']].drop_duplicates()
    sa2_to_ward.columns = ['sa2_code', 'sa2_name', 'ward_code', 'ward_name']

    df = df.merge(sa2_to_ward, left_on='area_code', right_on='sa2_code', how='left')

    print(f"Number of unique wards found in Christchurch listings: {df['ward_code'].nunique()}")
    print(f"Listings with no matching ward: {df['ward_code'].isnull().sum()}")

    df.to_csv(output_path, index=False)   # updating csv with new ward columns
    print(df[['area_code', 'sa2_name', 'ward_code', 'ward_name']].head(10))

    return df

#  ANSWERS TO DELIVERABLE 5 ------------------------------------------------------------------------------------------------------------------------------
def get_answers_del_5(df):
    '''produce answers to deliverable 5'''

    print()
    print("What’s the median AirBnB price in Christchurch Central (Location ID 326600)?")
    print()

    airbnb_median = df.loc[df['area_code'] == 326600, 'price'].median()

    print(f'The median Airbnb price in Christchurch Central is {airbnb_median} NZD.')
    print()
    print("In which part of Christchurch can we observe the craziest (largest) gap between short- and long-term rental prices?")
    print()

    #mark each row by short or long term rent (short = less than 90 days)

    df['short_or_long'] = np.where(df['minimum_nights'] >= 90, 'long', 'short')
    
    summary = pd.pivot_table(
        df, 
        values='price', 
        index='ward_name', 
        columns='short_or_long', 
        aggfunc=['min', 'max', 'mean'])

    # Flatten the multi-level columns to match your exact requested names
    summary.columns = ['lowest price long', 'lowest price short', 
    'highest price long', 'highest price short', 'long mean', 'short mean']

    summary['Mean Difference'] = abs(summary['long mean'] - summary['short mean'])
    summary['Diff low long - high short'] = abs(summary['lowest price long'] - summary['highest price short'])
    summary['Diff low short - high long'] = abs(summary['lowest price short'] - summary['highest price long'])

    summary = summary.reset_index()

    ward_with_largest_mean_difference = summary.loc[summary["Mean Difference"].idxmax(), 'ward_name']
    ward_max_diff = summary.loc[summary['ward_name'] == ward_with_largest_mean_difference,'Mean Difference'].iloc[0]
    ward_with_largest_lowLong_highShort = summary.loc[summary["Diff low long - high short"].idxmax(), 'ward_name']
    ward_max_1 = summary.loc[summary['ward_name'] == ward_with_largest_lowLong_highShort,'Diff low long - high short'].iloc[0]
    ward_with_largest_lowShort_highLong = summary.loc[summary["Diff low short - high long"].idxmax(), 'ward_name']
    ward_max_2 = summary.loc[summary['ward_name'] == ward_with_largest_lowShort_highLong,'Diff low short - high long'].iloc[0]

    print(f'The ward with the highest difference of mean short vs mean long term rental is {ward_with_largest_mean_difference} / {ward_max_diff:.2f} NZD.')
    print(f'The ward highest difference between lowest long term rental vs highest short term rental price is {ward_with_largest_lowLong_highShort} / {ward_max_1:.2f} NZD.')
    print(f'The ward highest difference between lowest short term rental vs highest long term rental price is  {ward_with_largest_lowShort_highLong} / {ward_max_2:.2f} NZD.')
    print()

    print('Compare how many AirBnBs and rental properties we have in each location.')
    print()
    print('See "airbnb_rental_merged.csv" for details.')
    print()

# MAIN  ----------------------------------------------------------------------------------------------------------------

def main():
    '''
    Asks user for input and returns requested graphs, statistics, tables or ends the program. 
    '''
    # Load and pre-process the file(s)
    df = read_csv_files(filenames=["listings_2026_06_19.csv","listings_2026_05_23.csv","listings_2026_04_16.csv",
                                   "listings_2026_03_17.csv","listings_2026_02_13.csv","listings_2026_01_16.csv",
                                   "listings_2025_12_11.csv","listings_2025_11_07.csv","listings_2025_10_05.csv"])    
                                   # Import & merge multiple files; filenames should be "listings_YYYY_MM_DD.csv"
    df = filter_locations(df)
    df = do_basic_cleaning(df)
    df = filter_timeframe(df, start_date="2020_01_01", end_date="2026_04_30")
    df = convert_categoricals(df)
    
    df.to_csv("concatenated_listings.csv", index=False)    #Write back to disk, omitting index column
    
    df = add_area_codes(df, api_key='api_key', layer_id=98970, output_path='listings_with_area_codes.csv')
    df = add_ward_codes(df)
 
    options = ['Summary statistics', 'Price histogram', 'Days since last review histogram', 'Top 10 percent of reviews table', 'Deliverable 5', 'Quit']
    
    run_programme = True
    while run_programme:
        user_input = option_selection(options)
        if user_input == 0:
            summary_stats(df)
        elif user_input == 1:
            print("\nGenerating Graph...\n")
            hist_prices(df)
        elif user_input == 2:
            print("\nGenerating Graph...\n")
            hist_dates(df)
        elif user_input == 3:
            top_10_reviews(df)
        elif user_input == 4:
            get_answers_del_5(df)
        elif user_input == 5:
            run_programme = False    #Quits the programme gracefully
            print('\nProgram closed.\n')

if __name__ == "__main__":
    main()
