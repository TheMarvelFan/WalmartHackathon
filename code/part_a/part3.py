import pandas as pd
from geopy.distance import geodesic
import numpy as np

def sorted_nearest_neighbor(locations, depot):
    remaining_locations = locations.copy()
    current_location = depot
    route = [depot]

    while remaining_locations:
        distances = [geodesic(current_location, loc).kilometers for loc in remaining_locations]
        min_index = np.argmin(distances)
        nearest_location = remaining_locations[min_index]
        route.append(nearest_location)
        remaining_locations.pop(min_index)
        current_location = nearest_location

    route.append(depot)
    return route

try:
    # Read dataset from CSV
    df = pd.read_csv('D:\git projects\walmart-sct-hackathon-round-1\input_datasets\part_a\part_a_input_dataset_3.csv')

    # Extracting locations and depot coordinates
    locations = list(zip(df['lat'], df['lng']))
    depot = (df['depot_lat'][0], df['depot_lng'][0])

    # Solve TSP using sorted nearest neighbor algorithm
    best_route = sorted_nearest_neighbor(locations, depot)

    # Calculate total distance
    total_distance = sum(geodesic(best_route[i], best_route[i+1]).kilometers for i in range(len(best_route)-1))

    # Prepare output dataframe
    output_df = pd.DataFrame(best_route, columns=['lat', 'lng'])
    output_df['order_id'] = ['depot'] + [f'order_{i}' for i in range(1, len(output_df)-1)] + ['depot']
    output_df['distance_from_previous'] = [geodesic(best_route[i], best_route[i+1]).kilometers for i in range(len(best_route)-1)] + [0]
    output_df['total_distance_from_depot'] = output_df['distance_from_previous'].cumsum()
    output_df['dlvr_seq_num'] = range(1, len(output_df) + 1)

    # Write output to CSV file
    output_df.to_csv('D:\git projects\walmart-sct-hackathon-round-1\output_datasets\part_a\part_a_output_dataset_3.csv', index=False)

    print("Output saved to output.csv")

except Exception as e:
    print("An error occurred:", e)
