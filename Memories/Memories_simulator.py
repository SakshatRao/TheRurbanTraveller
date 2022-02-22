import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Memories_Simulator:
    def __init__(self, sim_time = 24 * 60):
        self.sim_time = sim_time
        self.speed = np.zeros(self.sim_time)
        self.gps = np.zeros((self.sim_time, 2))
        
        self.acc_rates = []
        self.dec_rates = []
        self.top_speeds = []
        self.cruise_minutes = []
        self.trip_times = []

        self.ACC_RATE_AVG = 35 / 60     # km/min2
        self.ACC_RATE_VAR = 3 / 60
        self.DEC_RATE_AVG = 35 / 60     # km/min2
        self.DEC_RATE_VAR = 3 / 60
        self.TOP_SPEED_AVG = 90 / 60    # km/min
        self.TOP_SPEED_VAR = 10 / 60
        self.CRUISE_MINUTE_AVG = 120      # min
        self.CRUISE_MINUTE_VAR = 30
    
    def check_speed_limits(self):
        self.speed[self.speed < 0] = 0
    
    def add_random_traffic(self):
        non_zero_speed = (self.speed != 0)
        random_traffic_var = np.random.normal(0, 1/60, self.speed.shape[0])
        random_traffic_var = random_traffic_var * non_zero_speed
        self.speed = self.speed + random_traffic_var
        self.check_speed_limits()

    def add_acceleration(self, rate, top_speed):
        return np.linspace(0, top_speed, int(top_speed // rate))
    
    def add_deceleration(self, rate, top_speed):
        return np.linspace(top_speed, 0, int(top_speed // rate))
    
    def add_cruise(self, speed, minutes):
        return np.ones(minutes) * speed
    
    def plot_speed(self):
        plt.plot(self.speed)
        plt.xticks(np.arange(0, 24) * 60, labels = np.arange(0, 24))
        plt.yticks(np.arange(0, 12) * 10 / 60, labels = np.arange(0, 12) * 10)
        plt.show()
    
    def add_acc_cruise_dec(self, idx, acc_rate, dec_rate, top_speed, cruise_minutes):
        start = self.add_acceleration(acc_rate, top_speed)
        self.speed[idx: idx + start.shape[0]] = start
        mid = self.add_cruise(top_speed, cruise_minutes)
        self.speed[idx + start.shape[0]: idx + start.shape[0] + mid.shape[0]] = mid
        end = self.add_deceleration(dec_rate, top_speed)
        self.speed[idx + start.shape[0] + mid.shape[0]: idx + start.shape[0] + mid.shape[0] + end.shape[0]] = end
    
    def randomize_cruise_params(self):
        for idx in np.arange(self.trip_times.shape[0]):
            self.acc_rates[idx] = np.random.normal(self.ACC_RATE_AVG, self.ACC_RATE_VAR)
            self.dec_rates[idx] = np.random.normal(self.DEC_RATE_AVG, self.DEC_RATE_VAR)
            self.top_speeds[idx] = np.random.normal(self.TOP_SPEED_AVG, self.TOP_SPEED_VAR)
            self.cruise_minutes[idx] = int(np.round(np.random.normal(self.CRUISE_MINUTE_AVG, self.CRUISE_MINUTE_VAR)))
    
    def randomize_trip_times(self):
        
        num_trips = np.random.choice([0, 1, 2, 3, 4, 5], p = [1/20, 3/20, 4/20, 5/20, 4/20, 3/20])
        
        self.trip_times = np.zeros(num_trips, dtype = np.int32)
        remaining_trip_times = np.random.uniform(6 * 60, 20 * 60, num_trips)
        remaining_trip_times = np.sort(remaining_trip_times)
        for trip_idx, trip_time in enumerate(remaining_trip_times):
            self.trip_times[trip_idx] = int(trip_time)
        
    def simulate_speed(self, seed):
        np.random.seed(seed)
        self.speed = np.zeros(self.sim_time)
        self.refuels = []
        self.randomize_trip_times()
        self.acc_rates = np.zeros(len(self.trip_times))
        self.dec_rates = np.zeros(len(self.trip_times))
        self.top_speeds = np.zeros(len(self.trip_times))
        self.cruise_minutes = np.zeros(len(self.trip_times), dtype = np.int32)
        self.randomize_cruise_params()
        for trip_time, acc_rate, dec_rate, top_speed, cruise_minute in zip(self.trip_times, self.acc_rates, self.dec_rates, self.top_speeds, self.cruise_minutes):
            self.add_acc_cruise_dec(trip_time, acc_rate, dec_rate, top_speed, cruise_minute)
        self.add_random_traffic()

NUM_SIMS = np.random.choice([1, 2, 3, 4, 5], p = [1/9, 2/9, 3/9, 2/9, 1/9])
print(f"NUM_DAYS - {NUM_SIMS}")
speed_data = np.zeros((NUM_SIMS, 24 * 60))
mem_sim = Memories_Simulator()

SEED = np.random.randint(0, 1000)
print(f"Seed - {SEED}")

for sim_iter in np.arange(NUM_SIMS):
    print(f"Starting iteration {sim_iter + 1}")
    mem_sim.simulate_speed(SEED + sim_iter)
    speed_data[sim_iter, :] = mem_sim.speed

print("Done")
print(f"Total Distance: {speed_data.flatten().sum():.1f} km")

sampled_idx = [x for x in np.arange(24 * 60) if x % 5 == 0]
np.save(open('./Memories/Simulated_Data/speed_time_series_data.npy', 'wb'), speed_data[:, sampled_idx])