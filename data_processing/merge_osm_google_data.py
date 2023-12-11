import json
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape

def load_geojson(file_path):
    """ Load a GeoJSON file. """
    with open(file_path, 'r') as file:
        return json.load(file)

def merge_datasets(open_street_maps_file, google_maps_file):
    # Load datasets
    osm_data = load_geojson(open_street_maps_file)
    gmaps_data = load_geojson(google_maps_file)

    # Convert datasets to dictionaries for easy access
    osm_features = {feature['properties']['id']: feature for feature in osm_data['features']}
    gmaps_features = {feature['properties']['id']: feature for feature in gmaps_data['features']}

    # Prepare the list for GeoDataFrame
    gdf_list = []

    # Iterate and merge
    for osm_id, osm_feature in osm_features.items():
        if osm_id not in gmaps_features:
            raise Exception(f"OSM ID {osm_id} not found in Google Maps dataset")

        gmaps_feature = gmaps_features[osm_id]
        selected_feature = None
        source = None

        if osm_feature['properties']['stop_id'] == gmaps_feature['properties']['stop_id']:
            selected_feature = gmaps_feature
            source = 'Google'
        else:
            osm_distance = osm_feature['properties']['distance']
            gmaps_distance = gmaps_feature['properties']['distance']
            distance_diff = abs(osm_distance - gmaps_distance)

            if distance_diff > 20:
                if osm_distance < gmaps_distance:
                    selected_feature = osm_feature
                    source = 'OpenStreetMaps'
                else:
                    selected_feature = gmaps_feature
                    source = 'Google'
            else:
                selected_feature = gmaps_feature
                source = 'Google'

        # Add the source property
        selected_feature['properties']['source'] = source
        # Create a GeoDataFrame and add it to the list
        if selected_feature['geometry'] is not None:
            gdf = gpd.GeoDataFrame([selected_feature['properties']], geometry=[shape(selected_feature['geometry'])], crs="EPSG:4326")
        else:
            gdf = gpd.GeoDataFrame([selected_feature['properties']], geometry=None)
        gdf_list.append(gdf)

    # Combine all GeoDataFrames and save as GeoJSON
    final_gdf = pd.concat(gdf_list, ignore_index=True)
    final_gdf.to_file('merged_data.geojson', driver='GeoJSON')

# Usage example
merge_datasets('../public/norcs_with_closest_stops_valhalla.geojson', '../public/norcs_with_closest_stops_google.geojson')
