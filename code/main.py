# Load standard library modules
from glob import glob    #Friendly pattern-matching for path and filenames
import os
import pandas as pd
import sys

# Load custom libraries
import location as lo
import plots as pl
import stats as st
import wrangling as wr

start_date = "2020_01_01"
end_date   = "2026_04_30"

# Filenames to import
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path  = os.path.join(base_dir, "../input")
output_path = os.path.join(base_dir, "../output")
airbnb_data = glob(os.path.join(input_path, "airbnb/listings_*.csv"))    #Find all CSV files in the folder - filenames should be "listings_YYYY_MM_DD.csv"
rental_data = "Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv"
sa2_data = "Dwelling_SA2.csv"
classified_path = os.path.join(base_dir, "../Classified.txt")
with open(classified_path, 'r') as f:
    api_key = f.read().strip()


def option_selection(options):
    '''
    Ask the user to select an option from a list of options, and handle invalid inputs.
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
        print(f'\n{selection} is not a valid input. Please try again.\n')
        selection = int(input(prompt))
    return selection


def export_files(files_and_df:dict, filepath:str=output_path):
    '''
    Output the datasets to CSV files in the designated output folder, omitting the index column.
    'files_and_df' expects a dict of filename:dataset (excluding file extensions).
    '''
    for export_filename, export_data in files_and_df.items():
        export_data.to_csv(os.path.join(filepath, export_filename + ".csv"), index=False)

    print (f"{len(files_and_df)} files output to {os.path.abspath(output_path)}")

def run_batch(df_airbnb, df_rental_cleaned, merged_df):
    '''
    For the non-interactive automated pipeline. Runs every analysis/export step once with no menu.
    Used by 'make run' so the whole pipeline can be run with one command.
    '''
    def section(title): # defining this for uniform formatting to distinguish the outputs
        print("\n" + "-" * 70)
        print(f" {title}")
        print("-" * 70)

    section("SUMMARY STATISTICS - Airbnb Data")
    st.summary_stats(df_airbnb)

    section("SUMMARY STATISTICS - Tenancy Bond Data")
    st.summary_stats(df_rental_cleaned)

    section("PRICE HISTOGRAM - Airbnb Listings (saved to output/hist_prices.png)")
    pl.hist_prices(df_airbnb, output_path=output_path)

    section("DAYS SINCE LAST REVIEW HISTOGRAM - Airbnb Listings (saved to output/hist_dates.png)")
    pl.hist_dates(df_airbnb, output_path=output_path)

    section("TOP 10% OF LISTINGS BY NUMBER OF REVIEWS")
    st.top_10_reviews(df_airbnb)

    section("SHORT- VS LONG-TERM RENTAL PRICE COMPARISON BY WARD")
    st.compare_short_vs_long_term_rentals(df_airbnb)

    section("EXPORTING FILES")
    export_files({"concatenated_listings": df_airbnb,
                  "Merged-Data": df_rental_cleaned,
                  "airbnb_rental_merged": merged_df})

    print("\n" + "-" * 70)
    print("AUTOMATIC PIPELINE COMPLETE")
    print("-" * 70)

# Main Programme ------------------------------------------------------------------------
def main():
    '''
    Asks user for input and returns requested graphs, statistics, tables or ends the program. 
    '''
    # Load the file
    df_airbnb = wr.read_csv_files(filenames=[os.path.join(input_path, "airbnb", filename) for filename in airbnb_data])    #Import & merge multiple files
    df_rental = wr.read_bond_file(os.path.join(input_path, "tenancy", rental_data), ",") 
    df_sa2    = wr.read_bond_file(os.path.join(input_path, "tenancy", sa2_data), ",")

    # Clean the Files
    df_airbnb = wr.filter_locations(df_airbnb)
    df_airbnb = wr.do_basic_cleaning(df_airbnb)
    df_airbnb = wr.filter_timeframe(df_airbnb, start_date=start_date, end_date=end_date)
    df_airbnb = wr.convert_categoricals(df_airbnb)

    # Add the location data to the Airbnb data
    df_airbnb = lo.add_area_codes(df_airbnb, api_key=api_key, layer_id=98970, output_file=os.path.join(output_path,'listings_with_area_codes.csv'))
    df_airbnb = lo.add_ward_codes(df_airbnb)
    
    # Merge the files after some final cleaning/tweaks
    airbnb_aggregated = wr.clean_airbnb(df_airbnb)    #May be unnecessary
    df_rental_cleaned = wr.clean_rental(df_rental, df_sa2)
    merged_df = pd.merge(df_rental_cleaned, airbnb_aggregated, on=['year', 'months', 'Location Id'], how='left')

    # For the automated pipeline
    if "--auto" in sys.argv:
        run_batch(df_airbnb, df_rental_cleaned, merged_df)
        return # skip interactive menu if this is run

    # Gather & respond to user input
    options = ['Quit', 'Summary statistics', 'Price histogram', 'Days since last review histogram',
               'Top 10 percent of reviews table', 'Price Extremes', 'Export Files', 'Run Checks']
    run_programme = True
    while run_programme:
        user_input = option_selection(options)
        if user_input == 0:
            run_programme = False    #Quits the programme gracefully
            print('\nProgram closed.\n')
        elif user_input == 1:
            print("== Airbnb Data: ==")
            st.summary_stats(df_airbnb)
            print("== Tenancy Bond Data: ==")
            st.summary_stats(df_rental_cleaned)
        elif user_input == 2:
            print("\nGenerating Graph...\n")
            pl.hist_prices(df_airbnb)
        elif user_input == 3:
            print("\nGenerating Graph...\n")
            pl.hist_dates(df_airbnb)
        elif user_input == 4:
            st.top_10_reviews(df_airbnb)
        elif user_input == 5:
            st.compare_short_vs_long_term_rentals(df_airbnb)
        elif user_input == 6:
            export_files({"concatenated_listings":df_airbnb,
                          "Merged-Data":df_rental_cleaned,
                          "airbnb_rental_merged":merged_df})
        elif user_input == 7:
            check_options = options[1:-2]    #Trims off the 'quit', and the last options
            check_options_text = "\n".join(f"{i+1}: {o}" for i, o in enumerate(check_options))
            user_input_check_type = int(input(f"\nWhich component should be checked?\n{check_options_text}\n"))
            if user_input_check_type == 1:
                print(f"Checking {check_options[user_input_check_type - 1]}")
                st.sanity_check_summary_stats(df_airbnb)
            elif user_input_check_type == 2:
                print(f"Checking {check_options[user_input_check_type - 1]}")
                pl.sanity_check_hist_prices(df_airbnb)
            elif user_input_check_type == 3:
                print(f"Checking {check_options[user_input_check_type - 1]}")
                pl.sanity_check_hist_dates(df_airbnb)
            elif user_input_check_type == 4:
                print(f"Checking {check_options[user_input_check_type - 1]}")
                st.sanity_check_top_10_reviews(df_airbnb)
            elif user_input_check_type == 5:
                print(f"Checking {check_options[user_input_check_type - 1]}")
                st.sanity_check_compare_short_vs_long_term_rentals(df_airbnb)
            else:
                print("That wasn't a valid check option - if you weren't trying to escape the menu, try again...\n")
            

# Run the main() function
if __name__ == "__main__":
    main()
