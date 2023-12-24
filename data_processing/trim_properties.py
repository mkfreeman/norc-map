import json
import argparse

# List of properties to keep
properties_to_keep = ['id',"Address", "stop_code", "has_shelter", "has_shelter_with_bench", "bench_count", "stop_name", "distance", "Age 65+ Total", "All_Persons", "% of Seniors", "wheelchair_boarding", "latitude", "longitude", "stop_lat", "stop_lon", "amenity", "source"]

# This function will keep only the properties listed above, and
# it also does the correction to the stop amenities and wheelchair properties
# as described in Issue 28
def process_geojson(input_file):
    # Load the GeoJSON file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Process each feature in the GeoJSON file
    for feature in data['features']:
        # determine the value for the "amenity" feature
        # based on our confusing shelter and bench features. See Issue 28 for an analysis of this
        has_shelter_with_bench = feature['properties']["has_shelter_with_bench"]
        has_shelter = feature['properties']["has_shelter"]
        has_bench = feature['properties']["has_bench"]
        amenity = []
        if has_shelter_with_bench:
            amenity = ["Shelter With Bench Underneath"]
        elif has_shelter:
            amenity = ["Shelter Without Bench"]

        if feature["properties"]["bench_count"] > 0 and (len(amenity)==0 or "Without" in amenity[0]):
            amenity.append("Bench nearby")

        feature["properties"]["amenity"] = ",".join(amenity)
        
        # cleanup wheelchair to have words
        if feature["properties"]["wheelchair_boarding"] == 1:
            feature["properties"]["wheelchair_boarding"] = "Some"
        elif feature["properties"]["wheelchair_boarding"] == 2:
            feature["properties"]["wheelchair_boarding"] = "None"
        else:
            raise Exception(f"Wheelchair data for feature {feature['properties']['id']} is not 1 or 2")
            
        # Retain only the specified properties
        feature['properties'] = {key: value for key, value in feature['properties'].items() if key in properties_to_keep}

    # Output the modified GeoJSON to a new file
    with open('output_stripped_properties.geojson', 'w') as file:
        json.dump(data, file)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process a GeoJSON file and keep only specified properties.')
    parser.add_argument('input_file', help='The input GeoJSON file')
    args = parser.parse_args()

    # Process the GeoJSON file
    process_geojson(args.input_file)

if __name__ == "__main__":
    main()
