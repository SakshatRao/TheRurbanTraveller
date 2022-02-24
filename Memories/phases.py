from re import L
from turtle import speed
import numpy as np
import matplotlib.pyplot as plt

speed_data = np.load('./Memories/Simulated_Data/speed_time_series_data.npy')
speed_data = np.repeat(speed_data, 5, axis = 1).flatten()
gps_data = np.load(open('./Memories/Simulated_Data/gps_time_series_data.npy', 'rb'))

# plt.scatter(gps_data[:, 1], gps_data[:, 0], alpha = 0.1)
# plt.show()

SPEED_THRESH = speed_data[speed_data > 0].mean() / 2
GPS_VAR_THRESH = 1e-6
WINDOW_SIZE = int(0.5 * 60)
num_windows = gps_data.shape[0] // WINDOW_SIZE

phases = np.zeros(num_windows - 1)
for window_num in np.arange(num_windows - 1):
    if((speed_data[window_num * WINDOW_SIZE: (window_num + 1) * WINDOW_SIZE].mean() > SPEED_THRESH) and (gps_data[window_num * WINDOW_SIZE: (window_num + 1) * WINDOW_SIZE, :].var(axis = 0).max() > GPS_VAR_THRESH)):
        phases[window_num] = 1
    else:
        phases[window_num] = 0

gps_coords = np.zeros((num_windows - 1, 2))
for window_num in np.arange(num_windows - 1):
    gps_coords[window_num, :] = gps_data[window_num * WINDOW_SIZE: (window_num + 1) * WINDOW_SIZE, :].mean(axis = 0)

# plt.scatter(gps_coords[:, 1], gps_coords[:, 0])
# for idx in np.arange(gps_coords.shape[0]):
#     plt.annotate(['Travel' if x else 'Stop' for x in [phases[idx]]][0], (gps_coords[idx, 1], gps_coords[idx, 0]))
# plt.show()

np.save(open('./Memories/Processed_Data/phases.npy', 'wb'), phases)
np.save(open('./Memories/Processed_Data/gps_coords.npy', 'wb'), gps_coords)