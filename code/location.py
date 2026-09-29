# GETTING AREA CODES -------------------------------------------------------------------------------------------------------
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

def add_area_codes(df, api_key, layer_id, output_path='listings_with_area_codes.csv'):
    '''
    Adds a column for area code to the dataframe by querying a Koordinates API for each Airbnb listing's latitude and longitude
    using multiprocessing to assist with 28,000+ calls, then saves the result to a CSV file.
    '''
    # adding a safeguard to prevent re-running the API call
    if os.path.exists(output_path):
        print("There is already an existing file at {output_path}. Loading the saved results instead of re-querying the API.")
        return pd.read_csv(output_path)
    else:
        print(f"No existing file has been found. Running API queries for {len(df)} rows...")

        # build list of arguments for each row
        tasks = [(row['latitude'], row['longitude'], api_key, layer_id) for _, row in df.iterrows()]

        results = []
        with Pool(processes=5) as pool:
            for result in tqdm(pool.imap(query_wrapper, tasks), total=len(tasks)):
                results.append(result)

        df['area_code'] = results
        df.to_csv(output_path, index=False)
        print(f"The results have been saved to {output_path}.")
        return df

# ADDING WARD CODES ----------------------------------------------------------------------------------------------------
def add_ward_codes(df, ward_concordance_path='meshblock_2019_to_ward_2019.xlsx', 
                   sa2_concordance_path='meshblock_2019_to_sa2_2019.xlsx', output_path='listings_with_area_codes.csv'):
    '''
    Groups SA2 area codes into larger Ward areas by joining two Stats NZ meshblock files (Meshblock-to-Ward and Meshblock-to-SA2)
    on the shared meshblock code, then merging the resulting SA2-to-Ward onto the Airbnb dataframe using 'area_code'.
    '''
    mb_to_ward = pd.read_excel(ward_concordance_path, skiprows=9)
    mb_to_sa2 = pd.read_excel(sa2_concordance_path, skiprows=9)

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

    df.to_csv(output_path, index=False)   # updating csv with new ward columns
    print(df[['area_code', 'sa2_name', 'ward_code', 'ward_name']].head(10))

    return df

def get_answers_del_5(df):
    '''produce answers to deliverable 5'''

    print()
    print("What’s the median AirBnB price in Christchurch Central (Location ID 326600)?")
    print()

    airbnb_median = df.loc[df['area_code'] == 326600, 'price'].median()

    print(f'The median Airbnb price in Christchurch Central is {airbnb_median} NZD.')
    print()
    print("In which part of Christchurch can we observe the craziest (largest) gap between short- and long-term rental prices?")
    print()

    #mark each row by short or long term rent (short = less than 90 days)

    df['short_or_long'] = np.where(df['minimum_nights'] >= 90, 'long', 'short')
    
    summary = pd.pivot_table(
        df, 
        values='price', 
        index='ward_name', 
        columns='short_or_long', 
        aggfunc=['min', 'max', 'mean'])

    # Flatten the multi-level columns to match your exact requested names
    summary.columns = ['lowest price long', 'lowest price short', 
    'highest price long', 'highest price short', 'long mean', 'short mean']

    summary['Mean Difference'] = abs(summary['long mean'] - summary['short mean'])
    summary['Diff low long - high short'] = abs(summary['lowest price long'] - summary['highest price short'])
    summary['Diff low short - high long'] = abs(summary['lowest price short'] - summary['highest price long'])

    summary = summary.reset_index()

    ward_with_largest_mean_difference = summary.loc[summary["Mean Difference"].idxmax(), 'ward_name']
    ward_max_diff = summary.loc[summary['ward_name'] == ward_with_largest_mean_difference,'Mean Difference'].iloc[0]
    ward_with_largest_lowLong_highShort = summary.loc[summary["Diff low long - high short"].idxmax(), 'ward_name']
    ward_max_1 = summary.loc[summary['ward_name'] == ward_with_largest_lowLong_highShort,'Diff low long - high short'].iloc[0]
    ward_with_largest_lowShort_highLong = summary.loc[summary["Diff low short - high long"].idxmax(), 'ward_name']
    ward_max_2 = summary.loc[summary['ward_name'] == ward_with_largest_lowShort_highLong,'Diff low short - high long'].iloc[0]

    print(f'The ward with the highest difference of mean short vs mean long term rental is {ward_with_largest_mean_difference[0]} / {ward_max_diff:.2f}.')
    print(f'The ward highest difference between lowest long term rental vs highest short term rental price is {ward_with_largest_lowLong_highShort} / {ward_max_1:.2f}.')
    print(f'The ward highest difference between lowest short term rental vs highest long term rental price is  {ward_with_largest_lowShort_highLong} / {ward_max_2:.2f}.')
    print()

    print('Compare how many AirBnBs and rental properties we have in each location.')
    print()
    print('See "airbnb_rental_merged.csv" for details.')
    print()