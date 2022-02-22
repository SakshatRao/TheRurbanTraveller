import numpy as np
import pandas as pd

speed_data = np.load('./Memories/Simulated_Data/speed_time_series_data.npy')
speed_data = np.repeat(speed_data, 5, axis = 1).flatten()
num_days = speed_data.shape[0] / (24 * 60)

num_images = np.random.randint(10, 100)
image_timestamp = np.random.randint(0, num_days * 24 * 60, num_images)

np.save(open('./Memories/Simulated_Data/images.npy', 'wb'), image_timestamp)