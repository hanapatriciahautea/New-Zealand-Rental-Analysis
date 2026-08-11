import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#### Parameters and Helper Variables
err_wrap = "!!!!"




# LOAD FILES  ---------------------------------------------------------------------------------------------------------------------

def read_csv_file(filename: str):
    '''
    Reads the masterfile & converts necessary column data from strings to integers/floats.
    '''
    df = pd.DataFrame(), pd.DataFrame()    #Return statement is simpler if there's always *something* to return
    #Attempt to load; return failed filename for debugging when bulk/batch loading files
    try:
        listings = pd.read_csv(filename)
        df = pd.DataFrame(listings)
    except:
        print(f"\n{err_wrap} Error loading file {filename} {err_wrap}\n")

    return df 


def read_csv_files(filenames: [str], filepath: str = None):
    ''''
    Wrapper function for read_csv_file() which takes in a list of filenames and (optionally) path details, returning a single merged dataset.
    '''
    # Prefix filenames with path, if supplied
    if filepath != None:
        if filepath[-1] == "\\":
            filepath == filepath[:-1]  #Remove slash from the end to avoid double-ups
        filepath = filepath.strip()    #Remove trailing whitespace
        filenames = [filepath + "\\" + filename for filename in filenames] # Combine the file path & name
    
    df_set = [read_csv_file(filename) for filename in filenames]    #Generate a list of dataframes based on the files
    merged_df = pd.concat(df_set, ignore_index=True)    #Merge the files and recompute indices; should handle mild column differences automatically
    
    return merged_df


def do_custom_cleaning(dataset, drop_cols: str = None):
    ''''
    Return a cleaned dataset after dropping manually specified columns, performing type conversion
    and adding Month and Year columns
    '''
    # Drop targeted columns
    # Convert str to datetime
    # Convert ints to floats
    # Convert str and int to factors
        # Ordinal - levels have an 'order' or sequence
        # Nominal
    # Add column for month and year

    return dataset




# SUMMARY STATS  -----------------------------------------------------------------------------------------------------------------

def summary_stats(df):
    '''
    Prints summary statistics of the compiled masterfile.
    '''
    # Describe the df
    print(df.shape) # print the number of rows and columns in the dataframe
    print(df.columns) # print the column names in the dataframe
    print(df.isnull().sum()) # Count missing values per column
    print(df.describe())
    



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
    df['latest_publish_date'] = "2026-06-19"
    df['latest_publish_date'] = pd.to_datetime(df['latest_publish_date'])
    df['days_since_last_review'] = df['latest_publish_date'] - df['last_review']

    df['days_since_last_review'] = (df['days_since_last_review'].dt.total_seconds() / (24 * 60 * 60))

    sns.histplot(df['days_since_last_review'], bins = 30, kde = True)
    plt.title('Days since last review')
    plt.xlabel('Days')
    plt.ylabel('Count')
    plt.show()


# Plot 3: Top 10% of properties in Christchurch with highest numbers of reviews
def top_10_reviews(df):
    '''
    Print the top 10% of properties in Christchurch with highest number of reviews.
    '''
    df_sorted = df.sort_values(by='number_of_reviews', ascending = False)
    top_10_percent = df_sorted.head(int(len(df_sorted) * 0.1))

    display_df = top_10_percent[['id', 'name', 'number_of_reviews']].rename(columns={'name':'Name of Listing', 'number_of_reviews': 'Number of Reviews'})
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




# MAIN  ----------------------------------------------------------------------------------------------------------------

def main():
    '''
    Asks user for input and returns requested graphs, statistics, tables or ends the program. 
    '''
    # Load and pre-process the file(s)
    df = read_csv_file("listings.csv")        #Import a single file
    #df = read_csv_files(filenames=["listings1.csv"])    #Import & merge multiple files
    #df = do_custom_cleaning(df, drop_cols=["licence"])
    
    df.to_csv("concatenated_listings.csv", index=False)    #Write back to disk, omitting index column
    
    options = ['Summary statistics', 'Price histogram', 'Days since last review histogram', 'Top 10 percent of reviews table', 'Quit']
    
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
            run_programme = False    #Quits the programme gracefully
            print('\nProgram closed.\n')

if __name__ == "__main__":
    main()