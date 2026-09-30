import pandas as pd

# LOAD FILE  ----------------------------------------------------------------------------------------------------------------

def read_csv_file(filename: str, separator):
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

def main():
    '''
    Loads files. 
    '''
    rental_data = "Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv"
    SA2_data = "Dwelling_SA2.csv"
    # Load and pre-process the file(s)
    #df_rental = read_csv_file(rental_data, ",") 
    #df_SA2 = read_csv_file(SA2_data, ";")   
    df_rental = read_csv_file(rental_data, ",") 
    df_SA2 = read_csv_file(SA2_data, ",")

    df_rental_cleaned = clean_rental(df_rental, df_SA2)

    summary_stats(df_rental_cleaned)

    print(df_rental_cleaned.head(n=100))

    df_rental_cleaned.to_csv("Merged-Data.csv", index=False)
    
if __name__ == "__main__":
    main()
