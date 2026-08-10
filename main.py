import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_csv_data():
    '''
    Reads the masterfile & converts necessary column data from strings to integers/floats.
    '''
    listings = pd.read_csv("listings.csv")
    df = pd.DataFrame(listings)
    return df, listings

def summary_stats(df, listings):
    '''
    Prints summary statistics of the compiled masterfile.
    '''
    # Describe the df - IMPROVE THIS
    print(df.describe())

    # Count missing values per column
    print(df.isnull().sum())
    print(listings.shape) ##print the number of rows and columns in the dataframe
    print(listings.columns) ##print the column names in the dataframe
    print(listings.info()) ##print information about the dataframe

# VISUALISATIONS  ----------------------------------------------------------------------------------------------------------------

# Plot 1: Histogram of distribution of prices (New Zealand & Christchurch City)
def hist_prices(df):
    '''
    Prints a histogram of the distribution of Airbnb listing prices in Christchurch city.
    '''
    ## Filtering outliers (99th percentile) to get a better view of the distribution
    ## Note: the dataset is already filtered to christchurch only
    threshold = df['price'].quantile(0.99)
    df_filtered = df[df['price'] < threshold]

    fig, axs = plt.subplots(2, 1, figsize=(10, 10))

    # First subplot
    sns.histplot(df_filtered['price'], bins = 30, kde = True)
    plt.title('Distribution of Price (99th percentile cutoff)')
    plt.xlabel('Price')
    plt.ylabel('Count (# of listings)')
    # include both with and without outliers 

    # Second subplot
    sns.histplot(df['price'], bins = 30, kde = True)
    plt.title('Distribution of Price (99th percentile cutoff)')
    plt.xlabel('Price')
    plt.ylabel('Count (# of listings)')

    plt.show()

# Plot 2: Days since last review (scrape/publish date vs last review date)
def hist_dates(listings):
    '''
    Visualising the distribution of the number of days since the last review.
    '''
    listings['last_review'] = pd.to_datetime(listings['last_review'])
    listings['latest_publish_date'] = "2026-06-19"
    listings['latest_publish_date'] = pd.to_datetime(listings['latest_publish_date'])
    listings['days_since_last_review'] = listings['latest_publish_date'] - listings['last_review']

    listings['days_since_last_review'] = (listings['days_since_last_review'].dt.total_seconds() / (24 * 60 * 60))

    sns.histplot(listings['days_since_last_review'], bins = 30, kde = True)
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
    while i < len(options):
        print(f'{i} {options[i]}')
        i += 1

    selection = int(input(prompt))
    while selection < 0 or selection >= len(options):
        print(f'{selection} is not a valid input. Try again.')
        selection = int(input(prompt))
    return selection

# MAIN  ----------------------------------------------------------------------------------------------------------------
def main():
    '''
    Asks user for input and returns requested graphs, statistics, tables or ends the program. 
    '''
    df, listings = read_csv_data()
    options = ['Summary statistics', 'Price histogram', 'Days since last review histogram', 'Top 10 percent of reviews table', 'Quit']
    user_input = option_selection(options)
    if user_input == 0:
        summary_stats(df, listings)
    elif user_input == 1:
        hist_prices(df)
    elif user_input == 2:
        hist_dates(listings)
    elif user_input == 3:
        top_10_reviews(df)
    elif user_input == 4:
        print('Program closed.')

if __name__ == "__main__":
    main()