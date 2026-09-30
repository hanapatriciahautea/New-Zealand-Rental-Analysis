#### This file provides statistical summary/descriptive and analysis functions ####
import pandas as pd
import numpy as np
import plots as p


def summary_stats(df):  # Came from main.py and Rental-Bond-Data.py
    '''
    Prints summary statistics of the supplied dataset.
    '''
    # Describe the df; "\033[1m" and "\033[0m" indicate bold formatting
    print("=== Dataset Summary ===")
    print("\033[1m" + "Number of rows and columns in the dataframe:" + "\033[0m" + f" {df.shape}")
    print("\033[1m" + "Column names" + "\033[0m:" + ", ".join(df.columns) + ".")

    print("\n\033[1m" + "Data types per column" + "\033[0m")
    print(df.dtypes)

    print("\n\033[1m" + "Number of missing values per column:" + "\033[0m")
    print(df.isnull().sum())

    print("\n\033[1m" + "Descriptive statistics of dataset:" + "\033[0m")
    print(df.describe())


def top_10_reviews(df):
    '''
    Print the top 10% of properties in Christchurch with highest number of reviews.
    '''
    df_sorted = df.sort_values(by='number_of_reviews', ascending = False)
    top_10_percent = df_sorted.head(int(len(df_sorted) * 0.1))

    display_df = top_10_percent[['id', 'name', 'number_of_reviews', 'publish_date']].rename(columns={'id': 'ID', 'name':'Name of Listing', 'number_of_reviews': 'Number of Reviews', 'publish_date':'Publish Date'})
    display_df['Rank'] = top_10_percent['number_of_reviews'].rank(ascending = False, method='min').astype(int) # using min method to tie values at the lowest possible rank, reasonable for ranking reviews
    print(display_df)

    # To view the full table, you can uncomment the following lines to export to CSV:
    #display_df.to_csv('top_10_percent_listings.csv', index=False)



#  TODO: ANSWERS TO DELIVERABLE 5 ------------------------------------------------------------------------------------------------------------------------------
def get_answers_del_5(df):
    '''
    Produce answers to deliverable 5
    '''
    # Display the median Airbnb price in Christchurch central
    print("\nWhat's the median AirBnB price in Christchurch Central (Location ID 326600)?\n")
    airbnb_median = df.loc[df['area_code'] == 326600, 'price'].median()
    print(f'The median Airbnb price in Christchurch Central is {airbnb_median} NZD.')

    # Report the largest gap between short and long-term rental prices
    print("\nIn which part of Christchurch can we observe the craziest (largest) gap between short- and long-term rental prices?\n")
    df['short_or_long'] = np.where(df['minimum_nights'] >= 28, 'long', 'short')
    summary = pd.pivot_table(
        df, 
        values='price', 
        index='ward_name', 
        columns='short_or_long', 
        aggfunc=['min', 'max', 'mean'])

    # Flatten the multi-level columns to match the names we want to use
    summary.columns = ['lowest price long', 'lowest price short', 'highest price long', 'highest price short', 'long mean', 'short mean']

    # Calculate the difference between group means, cheapest long vs most expensive short, and cheapest short vs most expensive long
    summary['Mean Difference'] = abs(summary['long mean'] - summary['short mean']) # differences in average price of long- vs short- term stays
    summary['Diff low long - high short'] = abs(summary['lowest price long'] - summary['highest price short']) 
    summary['Diff low short - high long'] = abs(summary['lowest price short'] - summary['highest price long'])
    summary = summary.reset_index()

    p.plot_price_diffs(summary) # for the next plotting function

    # highest average difference between short vs long term rental 
    ward_with_largest_mean_difference = summary.loc[summary["Mean Difference"].idxmax(), 'ward_name']
    ward_max_diff = summary.loc[summary['ward_name'] == ward_with_largest_mean_difference,'Mean Difference'].iloc[0]

    # biggest gap between lowest long vs highest short term rental
    ward_with_largest_lowLong_highShort = summary.loc[summary["Diff low long - high short"].idxmax(), 'ward_name']
    ward_max_1 = summary.loc[summary['ward_name'] == ward_with_largest_lowLong_highShort,'Diff low long - high short'].iloc[0]

    # biggest gap between lowest short vs highest long term rental
    ward_with_largest_lowShort_highLong = summary.loc[summary["Diff low short - high long"].idxmax(), 'ward_name']
    ward_max_2 = summary.loc[summary['ward_name'] == ward_with_largest_lowShort_highLong,'Diff low short - high long'].iloc[0]

    print(f'The ward with the highest difference of mean short vs mean long term rental is {ward_with_largest_mean_difference} / {ward_max_diff:.2f} NZD.')
    print(f'The ward highest difference between lowest long term rental vs highest short term rental price is {ward_with_largest_lowLong_highShort} / {ward_max_1:.2f} NZD.')
    print(f'The ward highest difference between lowest short term rental vs highest long term rental price is {ward_with_largest_lowShort_highLong} / {ward_max_2:.2f} NZD.')
    print()
    print('To compare how many AirBnBs and rental properties we have in each location; See "airbnb_rental_merged.csv" for details.')

    # comment out below to verify that some wards have no rentals classified as 'long term'
    #print(summary[['ward_name', 'long mean', 'short mean', 'Mean Difference']])
