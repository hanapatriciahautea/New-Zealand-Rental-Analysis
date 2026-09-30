#### This file provides features to load location data from the Koordinates API ####

import os
import pandas as pd
import requests
from multiprocessing import Pool
from tqdm import tqdm

# Housekeeping
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path  = os.path.join(base_dir, "../input")
output_path = os.path.join(base_dir, "../output")


## GETTING AREA CODES VIA API KEY ------------------------------------------------------------------------------------------------
def get_area_code(lat, lon, api_key, layer_id):
    '''
    Queries the Koordinates API for a single latitude/longitude pair and returns the matching area code.
    '''
    url = "https://koordinates.com/services/query/v1/vector.json"
    params = {
        "key": api_key,
        "layer": layer_id,
        "x": lon,
        "y": lat,
        "max_results": 1,
        "radius": 1000,
        "with_field_names": "true"
    }
    try:
        response = requests.get(url, params = params)
        response.raise_for_status()
        data = response.json()
        features = data['vectorQuery']['layers'][str(layer_id)]['features']
        if not features:
            return None # if no match is found within the radius
        return features[0]['properties']['SA22019_V1_00'] # extract the area code field
    except Exception as e:
        print(f"Error for lat={lat}, lon={lon}: {e}")
        return None


def query_wrapper(args):
    '''
    Helper function so multiprocessing.Pool can pass multiple arguments using .imap().
    '''
    lat, lon, api_key, layer_id = args
    return get_area_code(lat, lon, api_key, layer_id)

def add_area_codes(df, api_key, layer_id, output_file=os.path.join(output_path, 'listings_with_area_codes.csv')):
    '''
    Adds a column for area code to the dataframe from querying a Koordinates API for each Airbnb listing's latitude and longitude
    using multiprocessing & saves the result to a CSV file.
    '''
    # adding a safeguard to prevent re-running the API call
    if os.path.exists(output_file):
        return pd.read_csv(output_file)
    
    else:
        print(f"No existing file has been found. Running API queries for {len(df)} rows...")

        # build list of arguments for each row
        tasks = [(row['latitude'], row['longitude'], api_key, layer_id) for _, row in df.iterrows()]

        results = []
        with Pool(processes=5) as pool:
            for result in tqdm(pool.imap(query_wrapper, tasks), total=len(tasks)):
                results.append(result)

        df['area_code'] = results
        df.to_csv(output_file, index=False)
        print(f"The results have been saved to {output_file}.")
        return df


##  ADDING WARD CODES ------------------------------------------------------------------------------------------------------------------------------
def add_ward_codes(df, ward_concordance_file=os.path.join(input_path, 'airbnb/meshblock_2019_to_ward_2019.xlsx'), 
                   sa2_concordance_file=os.path.join(input_path, 'airbnb/meshblock_2019_to_sa2_2019.xlsx'),
                   output_file=os.path.join(output_path, 'listings_with_area_codes.csv')):
    '''
    Groups SA2 area codes into Ward areas by joining two Stats NZ meshblock files (Meshblock-to-Ward and Meshblock-to-SA2),
    then merging the resulting SA2-to-Ward onto the Airbnb dataframe using 'area_code'.
    '''
    # adding a safeguard to prevent re-merging 
    if 'ward_code' in df.columns:
        return df

    mb_to_ward = pd.read_excel(ward_concordance_file, skiprows=9)
    mb_to_sa2 = pd.read_excel(sa2_concordance_file, skiprows=9)

    # join on the shared meshblock code
    sa2_to_ward = mb_to_sa2.merge(
        mb_to_ward,
        on='Source Code',
        suffixes=('_sa2', '_ward')
    )

    sa2_to_ward = sa2_to_ward[['Target Code_sa2', 'Descriptor.1_sa2', 'Target Code_ward', 'Descriptor.1_ward']].drop_duplicates()
    sa2_to_ward.columns = ['sa2_code', 'sa2_name', 'ward_code', 'ward_name']

    df = df.merge(sa2_to_ward, left_on='area_code', right_on='sa2_code', how='left')

    print(f"Number of unique wards found in Christchurch listings: {df['ward_code'].nunique()}")
    print(f"Listings with no matching ward: {df['ward_code'].isnull().sum()}")

    df.to_csv(output_file, index=False)   # updating csv with new ward columns
    print(df[['area_code', 'sa2_name', 'ward_code', 'ward_name']].head(10))

    return df