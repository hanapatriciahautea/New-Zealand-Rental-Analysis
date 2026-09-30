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

# Sanity Checks -----------------------------------------------------------------------------------------------------------

def sanity_check_hist_prices(df):
    '''
    Confirms the price data and outlier threshold going into hist_prices()
    behave as expected before the (blocking) plot is drawn.
    '''
    print("=== Sanity Check: hist_prices ===")
    assert 'price' in df.columns, "FAIL: 'price' column missing"
    assert (df['price'] >= 0).all(), "FAIL: negative prices found - price column may be corrupted"

    threshold = df['price'].quantile(0.99)
    df_filtered = df[df['price'] < threshold]
    assert len(df_filtered) < len(df), "FAIL: 99th percentile filter removed no rows - check for extreme outlier"
    print(f"PASS: 99th percentile threshold = {threshold:.2f}, filtered {len(df) - len(df_filtered)} outlier rows")
    print()


def sanity_check_hist_dates(df):
    '''
    Confirms date parsing and the negative-day filter in hist_dates() are
    still behaving as expected.
    '''
    print("=== Sanity Check: hist_dates ===")
    last_review = pd.to_datetime(df['last_review'], errors='coerce')
    publish_date = pd.to_datetime(df['publish_date'], errors='coerce')

    n_bad_dates = last_review.isnull().sum() + publish_date.isnull().sum()
    if n_bad_dates > 0:
        print(f"WARNING: {n_bad_dates} unparseable date values found")
    else:
        print("PASS: all last_review and publish_date values parsed successfully")

    days_diff = (publish_date - last_review).dt.total_seconds() / (24 * 60 * 60)
    n_negative = (days_diff < 0).sum()
    print(f"INFO: {n_negative} rows have a negative days_since_last_review (excluded from plot)")

    assert (days_diff.dropna() >= 0).sum() > 0, "FAIL: no valid non-negative date differences found - plot would be empty"
    print("PASS: at least some valid non-negative date differences exist to plot")
    print()


def sanity_check_plot_price_diffs(summary):
    '''
    Confirms the 'summary' table passed into plot_price_diffs() has the
    columns and value coverage the plot depends on.
    '''
    print("=== Sanity Check: plot_price_diffs ===")
    required_cols = {'ward_name', 'Mean Difference'}
    missing = required_cols - set(summary.columns)
    assert not missing, f"FAIL: summary is missing expected columns: {missing}"
    print("PASS: summary contains required columns")

    n_wards = summary['ward_name'].nunique()
    assert n_wards > 0, "FAIL: no wards present in summary"
    print(f"PASS: {n_wards} wards present in summary for plotting")

    n_valid = summary['Mean Difference'].notnull().sum()
    if n_valid < n_wards:
        print(f"WARNING: only {n_valid}/{n_wards} wards have a valid Mean Difference (others likely have no long-term listings)")
    else:
        print("PASS: every ward has a valid Mean Difference value")
    print()