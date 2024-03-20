import pandas as pd
from geopy.distance import geodesic
import numpy as np

def nearest_neighbor(locations, depot):
    remaining_locations = locations.copy()
    current_location = depot
    route = [depot]

    while remaining_locations:
        nearest_location = min(remaining_locations, key=lambda loc: geodesic(current_location, loc).kilometers)
        route.append(nearest_location)
        remaining_locations.remove(nearest_location)
        current_location = nearest_location

    route.append(depot)
    return route

try:
    # Read dataset from CSV
    df = pd.read_csv('D:\git projects\WalmartHackathon\input_datasets\part_a\part_a_input_dataset_2.csv')

    # Extracting locations and depot coordinates
    locations = list(zip(df['lat'], df['lng']))
    depot = (df['depot_lat'][0], df['depot_lng'][0])

    # Solve TSP using nearest neighbor algorithm
    best_route = nearest_neighbor(locations, depot)

    # Calculate total distance
    total_distance = sum(geodesic(best_route[i], best_route[i+1]).kilometers for i in range(len(best_route)-1))

    # Output the result
    output_df = pd.DataFrame(best_route, columns=['lat', 'lng'])
    output_df['order_id'] = ['depot'] + [f'order_{i}' for i in range(1, len(output_df)-1)] + ['depot']
    output_df['distance_from_previous'] = [geodesic(best_route[i], best_route[i+1]).kilometers for i in range(len(best_route)-1)] + [0]
    output_df['total_distance_from_depot'] = output_df['distance_from_previous'].cumsum()
    output_df['dlvr_seq_num'] = range(1, len(output_df) + 1)

    # Write output to CSV file
    output_df.to_csv('D:\git projects\WalmartHackathon\output_datasets\part_a\part_a_output_dataset_2.csv', index=False)

    print("Output saved to output.csv")

except Exception as e:
    print("An error occurred:", e)
