from turtle import speed
import numpy as np
import pandas as pd
from geopy import distance, Point

gps_coords = pd.read_csv('./Memories/GPS_Coords_Data/gps_coords.csv', header = None)
gps_coords.columns = ['lat', 'lon']
# print(gps_coords.head())
gps_dist = [0]
total_gps_dist = 0
for idx in np.arange(gps_coords.shape[0] - 1):
    p1 = Point(latitude = gps_coords.iloc[idx]['lat'], longitude = gps_coords.iloc[idx]['lon'])
    p2 = Point(latitude = gps_coords.iloc[idx + 1]['lat'], longitude = gps_coords.iloc[idx + 1]['lon'])
    dist = distance.geodesic(p1, p2).km
    total_gps_dist += dist
    gps_dist.append(dist)
gps_dist = np.cumsum(gps_dist)
print(f"Total GPS Distance: {total_gps_dist}")

speed_data = np.load('./Memories/Simulated_Data/speed_time_series_data.npy')
speed_data = np.repeat(speed_data, 5, axis = 1).flatten()
total_speed_dist = speed_data.sum()
print(f"Total Speed Distance: {total_speed_dist}")
speed_data = speed_data * total_gps_dist / total_speed_dist

cum_dist_data = np.cumsum(speed_data)
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return (gps_coords.iloc[idx]['lat'], gps_coords.iloc[idx]['lon'])

gps_coords_timeline = np.zeros((speed_data.shape[0], 2))
for dist_idx, dist in enumerate(cum_dist_data):
    gps_coords_timeline[dist_idx, :] = find_nearest(gps_dist, dist)

np.save(open('./Memories/Simulated_Data/gps_time_series_data.npy', 'wb'), gps_coords_timeline)