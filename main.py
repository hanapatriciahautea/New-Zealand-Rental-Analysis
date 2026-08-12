import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#### Parameters and Helper Variables
err_wrap = "!!!!"



# LOAD FILES  ---------------------------------------------------------------------------------------------------------------------

def read_csv_file(filename: str):
    '''Reads the masterfile & converts necessary column data from strings to integers/floats.'''
    print(".", end="")
    df = pd.DataFrame(), pd.DataFrame()    #Return statement is simpler if there's always *something* to return
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
    publish_dates = [filename.split('_')[1:] for filename in filenames]
    
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
        df_set.append(df)
    
    #Merge the dataframes (recomputing row indices) then return results; should handle mild column differences automatically
    merged_df = pd.concat(df_set, ignore_index=True)
    print(" Loading complete.")   
    return merged_df


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


def filter_rows(df):
    '''Drops all the rows which don't refer to Christchurch'''
    start_length = df.shape[0]
    
    neighbourhood_group_options = ["Christchurch City"]    #The locations to keep
    
    # Keep only the rows which mention the above
    df = df[df['neighbourhood_group'].isin(neighbourhood_group_options)]
    end_length = df.shape[0]

    print(f"Dropped {start_length - end_length} rows (down from {start_length} to {end_length} rows).")
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
    print(df.shape) # print the number of rows and columns in the dataframe
    print(df.columns) # print the column names in the dataframe
    print(df.isnull().sum()) # Count missing values per column
    print(df.describe())
    print(df.dtypes)    #Print the data types for the columns of the dataframe
    



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
    df = read_csv_files(filenames=["listings_2026_06_19.csv"])    # Import & merge multiple files; filenames should be "listings_YYYY_MM_DD.csv"
    df = filter_rows(df)
    df = do_basic_cleaning(df)
    df = convert_categoricals(df)

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
