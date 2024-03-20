import pandas as pd
import numpy as np
from itertools import permutations

# Function to calculate distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in km
    dlat = np.deg2rad(lat2 - lat1)
    dlon = np.deg2rad(lon2 - lon1)
    a = np.sin(dlat / 2) * np.sin(dlat / 2) + np.cos(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2)) * np.sin(dlon / 2) * np.sin(dlon / 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c  # Distance in km
    return distance

# Function to assign orders to vehicles
def assign_orders_to_vehicles(order_data, vehicle_capacity):
    orders = order_data.values.tolist()
    depot_lat, depot_lon = orders[0][3], orders[0][4]
    orders = orders[1:]  # Exclude depot from orders
    orders_distances = [(order[0], calculate_distance(depot_lat, depot_lon, order[1], order[2])) for order in orders]
    orders_distances.sort(key=lambda x: x[1])  # Sort orders based on distance from depot
    vehicles_routes = [[] for _ in range(len(orders) // vehicle_capacity + 1)]  # List to store routes for each vehicle
    vehicle_index = 0
    for i in range(0, len(orders), vehicle_capacity):
        orders_subset = orders_distances[i:i+vehicle_capacity]
        for order, _ in orders_subset:
            vehicles_routes[vehicle_index].append(order)
        vehicle_index += 1
    return vehicles_routes

# Function to generate delivery routes for each vehicle
def generate_delivery_routes(order_data, vehicles_routes):
    depot_lat, depot_lon = order_data.iloc[0]['depot_lat'], order_data.iloc[0]['depot_lng']
    delivery_routes = []
    for vehicle_index, orders in enumerate(vehicles_routes, start=1):
        route = ['depot'] + orders + ['depot']  # Route starts and ends at depot
        route_coords = [(depot_lat, depot_lon)] + [(order_data.loc[order_data['order_id'] == order]['lat'].values[0],
                                                    order_data.loc[order_data['order_id'] == order]['lng'].values[0]) for order in orders] + [(depot_lat, depot_lon)]
        route_distances = [calculate_distance(route_coords[i][0], route_coords[i][1], route_coords[i+1][0], route_coords[i+1][1]) for i in range(len(route_coords)-1)]
        total_distance = sum(route_distances)
        delivery_routes.extend([(order, *coords, depot_lat, depot_lon, vehicle_index, seq_num) for order, coords, seq_num in zip(orders, route_coords[1:], range(1, len(orders)+1))])
    return delivery_routes

# Read input data from CSV
input_file = "input_datasets\part_b\part_b_input_dataset_1.csv"
order_data = pd.read_csv(input_file)

# Parameters
vehicle_capacity = 20  # Maximum number of orders each vehicle can deliver

# Assign orders to vehicles
vehicles_routes = assign_orders_to_vehicles(order_data, vehicle_capacity)

# Generate delivery routes for each vehicle
delivery_routes = generate_delivery_routes(order_data, vehicles_routes)

# Write output to CSV
output_columns = ['order_id', 'lng', 'lat', 'depot_lat', 'depot_lng', 'vehicle_num', 'dlvr_seq_num']
output_data = pd.DataFrame(delivery_routes, columns=output_columns)
output_data.to_csv('output.csv', index=False)