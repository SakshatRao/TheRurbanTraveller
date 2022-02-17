import matplotlib.pyplot as plt
import numpy as np

NUM_DAYS = 100

with open('./OBD2_Simulator/Simulated_Data/fuel_info.txt', 'r') as read_file:
    content = read_file.read().strip().split('\n')
    fuel_cost = float(content[0])
    fuel_data = [float(x) for x in content[1:]]
speed_data = np.load(open('./OBD2_Simulator/Simulated_Data/speed_time_series_data.npy', 'rb'))
speed_data = np.repeat(speed_data, 5, axis = 1)

plot_start_idx = np.random.randint(0, 365 - NUM_DAYS)
plot_speed = speed_data[plot_start_idx: plot_start_idx + NUM_DAYS, :].flatten()
plot_refuels = []
for refuel in fuel_data:
    if((refuel >= plot_start_idx) and (refuel < plot_start_idx + NUM_DAYS)):
        plot_refuels.append(refuel)

plt.plot(plot_speed, label = "Speed")
plt.vlines([(x - plot_start_idx) * 24 * 60 for x in plot_refuels], ymin = 0, ymax = 100 / 60, color = 'red', label = "Refuelling Points")
plt.xticks(np.arange(0, NUM_DAYS) * 60 * 24, labels = np.arange(0, NUM_DAYS) + plot_start_idx, rotation = 90)
plt.yticks(np.arange(0, 10) * 10 / 60, labels = np.arange(0, 10) * 10)
plt.title(f"{NUM_DAYS}-day Simulation")
plt.xlabel("Day #")
plt.ylabel("Speed")
plt.legend(loc = 'best')
plt.show()

plt.plot(speed_data.mean(axis = 0), label = "Speed")
plt.xticks(np.arange(0, 24) * 60, labels = np.arange(0, 24))
plt.yticks(np.arange(0, 5) * 10 / 60, labels = np.arange(0, 5) * 10)
plt.title(f"Avg. Speed")
plt.xlabel("Hour")
plt.ylabel("Speed")
plt.show()