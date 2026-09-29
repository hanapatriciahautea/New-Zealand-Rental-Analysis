#### From main.py ####

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

#### End of content from main.py ####




#### From rentalBondData.py ####
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

#### From rentalBondData.py ####