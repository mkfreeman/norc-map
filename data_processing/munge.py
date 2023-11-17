import geopandas as gpd

# Load the GeoJSON file into a GeoDataFrame
gdf = gpd.read_file('output.geojson')

# Add an 'id' column, starting at 1 and incrementing by 1 for each feature
gdf['id'] = range(1, len(gdf) + 1)

# Save the modified GeoDataFrame back to a GeoJSON file
gdf.to_file('modified_geojson_file.geojson', driver='GeoJSON')
