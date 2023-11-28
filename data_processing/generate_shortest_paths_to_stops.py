import pandas as pd
import geopandas as gpd
from geopy.distance import distance
from routingpy import Valhalla
from shapely.geometry import Point, LineString, mapping
import json

# by default we assume you are running a Valhalla server. Pass in the
# empty string to run against the Valhalla public server, but this will
# be very slow
# TODO(omar): need to handle loading in different types of data, basically Excel, CSV and GeoJSON. That should cover everything. 
def calculate_shortest_paths(norcs_file, stops_file, distance_threshold,valhalla_server_url='http://localhost:8002'):
    # Load the data
    norcs_df = pd.read_excel(norcs_file)
    #norcs_df = norcs_df[norcs_df['Address'].str.contains('138 Bonis')]
    stops_df = pd.read_csv(stops_file)

    # Initialize the routing client with the Valhalla server
    client = Valhalla(base_url=valhalla_server_url)
    #client = Valhalla()
    # Prepare the output list
    gdf_list = []

    # Iterate through each NORC, and identify a subset of stops that
    # might be the closest just based on straight line distance
    i = 0
    for _, norc in norcs_df.iterrows():
        i = i + 1
        print(i)
        norc_point = (norc['latitude'], norc['longitude'])
        print(norc['Address'])
        # Find stops within the specified distance
        nearby_stops = []
        closest_stop = None
        for _, stop in stops_df.iterrows():
            stop_point = (stop['stop_lat'], stop['stop_lon'])
            #print (stop_point, norc_point, stop.stop_name, distance(norc_point, stop_point).m)
            if distance(norc_point, stop_point).m <= distance_threshold:
                #print(stop.stop_name)
                nearby_stops.append(stop)
        print("Number of nearby stops: ", len(nearby_stops))
        # Compute walking distances and paths
        # for the candidate stops, use Valhalla to find the actual
        # walking path. 
        shortest_distance = float('inf')
        shortest_path = None
        for stop in nearby_stops:
            try:
                
                route = client.directions(locations=[(norc_point[1], norc_point[0]), (stop['stop_lon'], stop['stop_lat'])], profile='foot', costing='pedestrian', format='geojson')
                #print(stop.stop_name)
                #print(route.distance)
                if route.distance < shortest_distance:
                    #print(shortest_distance)
                    #print(norc.Address)
                    shortest_distance = route.distance
                    shortest_path = LineString(route.geometry)
                    closest_stop = stop
            except Exception as e:
                print(f"Error computing route: {e}")

        # Construct GeoJSON feature
        if shortest_path:
            properties = {**norc.to_dict(), **closest_stop.to_dict(), 'distance': shortest_distance}
        else:
            properties = {**norc.to_dict(), 'distance': None}
        gdf = gpd.GeoDataFrame([properties], geometry=[shortest_path], crs="EPSG:4326")
        gdf_list.append(gdf)

    # Combine all GeoDataFrames
    final_gdf = pd.concat(gdf_list, ignore_index=True)

    # add a building id to the file since there isn't one in the raw data
    final_gdf['id'] = range(1, len(final_gdf) + 1)
    # Save as GeoJSON
    final_gdf.to_file('output.geojson', driver='GeoJSON')

# Example usage: Note the 300, which indicates TTC stop candidates are
# up to 300 meters from the building. This is rather large, but
# will make sure every stop is included. 
calculate_shortest_paths('../raw_data/NORCs_Toronto_Geocoded.xlsx', '../public/stops_with_shelter_bench_info.csv', 800)
#calculate_shortest_paths('../raw_data/NORCs_Toronto_Geocoded.xlsx', '../public/ttc_subway_stations.csv', 800)
