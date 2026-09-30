#### This file provides data visualisation functions ####
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# General Purpose -----------------------------------------------------------------------------------------------------
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


# Price Differences  -----------------------------------------------------------------------------------------------------
def plot_price_diffs(summary):
    '''
    Plotting the difference in price per night for short- vs long-term Airbnb rentals per ward.
    '''
    # sorting in descending order
    summary_sorted = summary.sort_values('Mean Difference', ascending=False)

    plt.figure(figsize=(10,8))
    sns.barplot(data=summary_sorted, y='ward_name', x='Mean Difference')
    plt.title('Average price gap between Short- and Long-term Airbnb rentals per ward')
    plt.xlabel('Mean Price Difference per Night (NZD)')
    plt.ylabel('Ward')
    plt.tight_layout()
    plt.show()
    