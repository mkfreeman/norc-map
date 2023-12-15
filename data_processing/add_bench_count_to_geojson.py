import geopandas as gpd
import pandas as pd
import argparse

def add_bench_count_to_geojson(geojson_file, bench_count_file):
    # Load bench count data
    bench_counts_df = pd.read_csv(bench_count_file)
    
    # Load GeoJSON data
    gdf = gpd.read_file(geojson_file)
    
    # Merge the GeoDataFrame with bench counts based on 'stop_code'
    merged_gdf = gdf.merge(bench_counts_df, on='stop_code', how='left')
    
    # Save the merged data back to a new GeoJSON file
    output_file = 'updated_' + geojson_file.split('/')[-1]
    merged_gdf.to_file(output_file, driver='GeoJSON')

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Add bench count to GeoJSON file based on stop_code.')
    parser.add_argument('geojson_file', help='The input GeoJSON file with transit stop information.')
    parser.add_argument('bench_count_file', default='output_bench_count.csv', nargs='?',
                        help='The CSV file with bench count data. Defaults to output_bench_count.csv if not provided.')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the function with the provided arguments
    add_bench_count_to_geojson(args.geojson_file, args.bench_count_file)

if __name__ == "__main__":
    main()
