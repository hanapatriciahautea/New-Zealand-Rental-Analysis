import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from multiprocessing import Pool
from tqdm import tqdm
import os
import numpy as np

#### Parameters and Helper Variables

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
    df = read_csv_files(filenames=["listings_2026_06_19.csv","listings_2026_05_23.csv","listings_2026_04_16.csv",
                                   "listings_2026_03_17.csv","listings_2026_02_13.csv","listings_2026_01_16.csv",
                                   "listings_2025_12_11.csv","listings_2025_11_07.csv","listings_2025_10_05.csv"])    
                                   # Import & merge multiple files; filenames should be "listings_YYYY_MM_DD.csv"
    df = filter_locations(df)
    df = do_basic_cleaning(df)
    df = filter_timeframe(df, start_date="2020_01_01", end_date="2026_04_30")
    df = convert_categoricals(df)
    
    df.to_csv("concatenated_listings.csv", index=False)    #Write back to disk, omitting index column
    
    df_airbnb = add_area_codes(df, api_key='api_key', layer_id=98970, output_path='listings_with_area_codes.csv')
    df_airbnb = add_ward_codes(df_airbnb)
 
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
            get_answers_del_5(df_airbnb)
        elif user_input == 5:
            run_programme = False    #Quits the programme gracefully
            print('\nProgram closed.\n')

if __name__ == "__main__":
    main()




#### From rentalBondData.py ####
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

#### End of material from rentalBondData.py ####




#### From mergeing.py ####
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

#### End of material from mergeing.py ####