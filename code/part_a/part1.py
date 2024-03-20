import pandas as pd
from geopy.distance import geodesic
import itertools

def tsp_brute_force(locations, depot):
    best_distance = float('inf')
    best_route = None

    for perm in itertools.permutations(locations):
        route = [depot] + list(perm) + [depot]
        total_distance = sum(geodesic(route[i], route[i+1]).kilometers for i in range(len(route)-1))
        
        if total_distance < best_distance:
            best_distance = total_distance
            best_route = route

    return best_route, best_distance

# Read dataset from CSV
df = pd.read_csv('D:\git projects\WalmartHackathon\input_datasets\part_a\part_a_input_dataset_1.csv')

# Extracting locations and depot coordinates
locations = [(row['lat'], row['lng']) for _, row in df.iterrows()]
depot = (df['depot_lat'][0], df['depot_lng'][0])

# Solve TSP
best_route, best_distance = tsp_brute_force(locations, depot)

# Create DataFrame for output
output_df = pd.DataFrame(best_route, columns=['lat', 'lng'])
output_df['order_id'] = ['depot'] + [f'order_{i}' for i in range(1, len(output_df)-1)] + ['depot']
output_df['distance_from_previous'] = [geodesic(best_route[i], best_route[i+1]).kilometers for i in range(len(best_route)-1)] + [0]
output_df['total_distance_from_depot'] = output_df['distance_from_previous'].cumsum()

# Add delivery sequence numbers
output_df['dlvr_seq_num'] = range(1, len(output_df) + 1)

# Write output to CSV file
output_df.to_csv('D:\git projects\WalmartHackathon\output_datasets\part_a\part_a_output_dataset_1.csv', index=False)

print("Output written to part_a_output_dataset_1.csv")
