import os
import pandas as pd
import geopandas as gpd
from geopy.distance import distance
from routingpy import Valhalla, Google
from shapely.geometry import Point, LineString, mapping
import pickle

def calculate_shortest_paths(norcs_file, stops_file, distance_threshold, routing_service='valhalla', valhalla_server_url='http://localhost:8002', google_api_key=None):
    # Load the data
    norcs_df = pd.read_excel(norcs_file)
    stops_df = pd.read_csv(stops_file)

    # Initialize the routing client based on the chosen service
    if routing_service == 'google' and google_api_key:
        client = Google(api_key=google_api_key)
    else:
        client = Valhalla(base_url=valhalla_server_url)

    # Prepare the output list
    gdf_list = []

    # Iterate through each NORC
    i = 0
    for _, norc in norcs_df.iterrows():
        i += 1
        print(i)
        norc_point = (norc['latitude'], norc['longitude'])

        # Find nearby stops
        nearby_stops = []
        for _, stop in stops_df.iterrows():
            stop_point = (stop['stop_lat'], stop['stop_lon'])
            d = distance(norc_point, stop_point).m
            if d <= distance_threshold:
                nearby_stops.append((d,stop))
        print("Number of nearby stops: ", len(nearby_stops))
        nearby_stops.sort(key=lambda x: x[0])
        if routing_service == 'google':
            # we limit API calls on Google to only the 10 nearest straight-line distance stops, which should be more than enough
            nearby_stops = nearby_stops[:10]

        # Now find out which is nearest by walking distance, and
        # save the shortest one
        shortest_distance = float('inf')
        shortest_path = None
        for (_, stop) in nearby_stops:
            # Generate file name based on stop ID and NORC address
            file_name = f"tmp/{stop['stop_id']}_{norc['Address'].replace(' ', '_')}.pkl"

            # Check if file exists
            if routing_service == 'google' and os.path.exists(file_name):
                with open(file_name, 'rb') as file:
                    #print("Got cached data for ", file_name)
                    route = pickle.load(file)
            else:
                # Make a routing request
                try:
                    if routing_service == 'valhalla':
                        route = client.directions(locations=[(norc_point[1], norc_point[0]), (stop['stop_lon'], stop['stop_lat'])], profile='foot', costing='pedestrian', format='geojson')
                    elif routing_service == 'google':
                         route = client.directions(locations=[(norc_point[1], norc_point[0]), (stop['stop_lon'], stop['stop_lat'])], profile='walking')
                         # Save the route data to a file
                         with open(file_name, 'wb') as file:
                             pickle.dump(route, file)
                except Exception as e:
                    print(f"Error computing route: {e}")
                    break

            # Process route
            route_distance = route.distance
            if route_distance < shortest_distance:
                shortest_distance = route_distance
                shortest_path = LineString([])
                if shortest_distance > 0:
                    shortest_path = LineString(route.geometry)
                closest_stop = stop
        # Construct GeoJSON feature
        properties = {**norc.to_dict(), **closest_stop.to_dict(), 'distance': shortest_distance} 
        gdf = gpd.GeoDataFrame([properties], geometry=[shortest_path], crs="EPSG:4326")
        gdf_list.append(gdf)

    # Combine all GeoDataFrames and save as GeoJSON
    final_gdf = pd.concat(gdf_list, ignore_index=True)
    final_gdf['id'] = range(1, len(final_gdf) + 1)
    final_gdf.to_file('output.geojson', driver='GeoJSON')

# Example usage
#calculate_shortest_paths('../raw_data/NORCs_Toronto_Geocoded.xlsx', '../public/stops_with_shelter_bench_info.csv', 800)
google_maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
calculate_shortest_paths('../raw_data/NORCs_Toronto_Geocoded.xlsx', '../public/stops_with_shelter_bench_info.csv', 800, routing_service='google', google_api_key=google_maps_api_key)
