import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point
import json

def count_benches_near_stops(transit_stops_file, benches_file):
    # Load transit stops data
    stops_df = pd.read_csv(transit_stops_file)
    # Convert to GeoDataFrame
    stops_gdf = gpd.GeoDataFrame(
        stops_df, 
        geometry=gpd.points_from_xy(stops_df.stop_lon, stops_df.stop_lat),
        crs="EPSG:4326"
    )

    # Load benches data
    benches_df = pd.read_csv(benches_file)
    # Convert the 'geometry' column from stringified GeoJSON to Shapely objects
    benches_df['geometry'] = benches_df['geometry'].apply(lambda x: shapely.geometry.shape(json.loads(x.replace("'", '"'))))
    benches_gdf = gpd.GeoDataFrame(benches_df, crs="EPSG:4326")

    # Buffer stops by 5 meters to create a search area (adjust EPSG if needed for proper distance calculation)
    buffer_radius = 10  # meters
    stops_gdf['buffered'] = stops_gdf.geometry.to_crs(epsg=3857).buffer(buffer_radius).to_crs(epsg=4326)

    # Save the buffers and benches to Shapefiles
    #stops_gdf['buffered'].to_file('stop_buffers.shp')
    #benches_gdf.to_file('street_furniture_locations.shp')
    
    # Count benches within the buffer for each stop
    counts = stops_gdf['buffered'].apply(lambda x: benches_gdf.within(x).sum())
    result = pd.DataFrame({
        'stop_code': stops_gdf['stop_code'],
        'bench_count': counts
    })

    return result

# Example usage
result_df = count_benches_near_stops('../public/stops.txt', '../raw_data/Street furniture-Bench data - 4326 (1).csv')
result_df.to_csv('output_bench_count.csv', index=False)
