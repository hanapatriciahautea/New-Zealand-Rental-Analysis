import pandas as pd

def read_csv_file(filename: str):
    '''Reads the masterfile & converts necessary column data from strings to integers/floats.'''
    print(".", end="")
    df = pd.DataFrame()
    dataset = pd.read_csv(filename)
    df = pd.DataFrame(dataset)

    return df 

def clean_airbnb(df):

    #create month ranges: MM=04 -> JAN-MAR, MM=07 -> APR-JUN, MM=10 -> JUL-SEP, MM=01 -> OCT-DEC
    df['months'] = df['month'].replace({1: "JAN-MAR", 2: "JAN-MAR", 3: "JAN-MAR", 4: "APR-JUN", 5: "APR-JUN", 6: "APR-JUN", 7: "JUL-SEP", 8: "JUL-SEP", 9: "JUL-SEP", 10: "OCT-DEC", 11: "OCT-DEC", 12: "OCT-DEC"})       
    df['months-year'] = df['months'].astype(str) + "-" + df['year'].astype(str)

    #remove all data before Q4 2025 and after Q1 2026 to match rental bond dataset
    df = df[(df['months-year'] == 'OCT-DEC-2025') | (df['months-year'] == 'JAN-MAR-2025')]

    #merge by quarters and find mean of price
    df_merge_areas = df.groupby(['year', 'months', 'area_code'], as_index=False)['price'].mean()
    df_merge_areas = df_merge_areas.rename(columns={'price': 'mean_price'})
    df_merge_areas = df_merge_areas.rename(columns={'area_code': 'Location Id'})

    print(df_merge_areas.head())

    df_merge_areas.to_csv("airbnb_ready_for_merge.csv", index=False)

    return df_merge_areas

def clean_rental(df):
    df = df[(df['Dwelling Type'] == 'ALL') & (df['Number Of Beds'] == 'ALL')]
    df.to_csv("rental_ready_for_merge.csv", index=False)
    return df

def main():
    '''prepare and merge airbnb and rental bon data.'''
    airbnb_data = 'listings_with_area_codes.csv'
    rental_data = 'Merged-Data.csv'

    airbnb_df = read_csv_file(airbnb_data)
    rental_df = read_csv_file(rental_data)

    airbnb_aggregated = clean_airbnb(airbnb_df)
    rental_cleaned = clean_rental(rental_df)

    merged_df = pd.merge(rental_cleaned, airbnb_aggregated, on=['year', 'months', 'Location Id'], how='left')

    merged_df.to_csv("airbnb_rental_merged.csv", index=False)

main()