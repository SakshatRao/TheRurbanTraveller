from turtle import speed
import matplotlib.pyplot as plt
import numpy as np

speed_data = np.load(open('./Memories/Simulated_Data/speed_time_series_data.npy', 'rb'))
speed_data = np.repeat(speed_data, 5, axis = 1)

NUM_DAYS = speed_data.shape[0]

plot_start_idx = 0
plot_speed = speed_data[plot_start_idx: plot_start_idx + NUM_DAYS, :].flatten()

plt.plot(plot_speed, label = "Speed")
plt.xticks(np.arange(0, NUM_DAYS) * 60 * 24, labels = np.arange(0, NUM_DAYS) + plot_start_idx, rotation = 90)
plt.yticks(np.arange(0, 12) * 10 / 60, labels = np.arange(0, 12) * 10)
plt.title(f"{NUM_DAYS}-day Simulation")
plt.xlabel("Day #")
plt.ylabel("Speed")
plt.legend(loc = 'best')
plt.show()