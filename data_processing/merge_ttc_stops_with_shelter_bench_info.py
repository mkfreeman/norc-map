import pandas as pd

def update_stops_data(stops_df, shelters_df, stop_id_column, new_boolean_column_name):

    # Remove rows where SITEID is NaN
    shelters_df = shelters_df.dropna(subset=[stop_id_column])

    # Ensure SITEID is a string before replacing and convert to integer
    shelters_df['SITEID'] = shelters_df[stop_id_column].astype(str).str.replace('T', '')

    # Handle any remaining non-numeric entries and convert to integer
    shelters_df['SITEID'] = pd.to_numeric(shelters_df[stop_id_column], errors='coerce').fillna(0).astype(int)

    # Perform a left join on the stop_code and SITEID columns
    combined_df = pd.merge(stops_df, shelters_df[[stop_id_column]], left_on='stop_code', right_on=stop_id_column, how='left', indicator=True)

    # Add the 'has_shelter_with_bench' column
    combined_df[new_boolean_column_name] = combined_df['_merge'] == 'both'

    # Drop unnecessary columns
    combined_df.drop(columns=[stop_id_column, '_merge'], inplace=True)

    # Display the first few rows of the DataFrame
    print(combined_df.head())
    return combined_df


# Read the CSV file into a DataFrame
stops_df = pd.read_csv('../public/stops.txt')

# Read the shelter/benches files into a DataFrames
shelters_df = pd.read_csv('../raw_data/Transit shelter data - 4326 (1).csv')
benches_df = pd.read_csv('../raw_data/Street furniture-Bench data - 4326 (1).csv')
shelters_with_benches_df = pd.read_excel('../raw_data/Transit_Shelters_With_Benches_11062023 (1).xls')

combined_df = update_stops_data(stops_df, shelters_df, "SITEID", "has_shelter")

combined_df = update_stops_data(combined_df, shelters_with_benches_df, "TTC Stop ID", "has_shelter_with_bench")

combined_df = update_stops_data(combined_df, benches_df, "SITEID", "has_bench")

combined_df.to_csv("stops_with_shelter_bench_info.csv")
