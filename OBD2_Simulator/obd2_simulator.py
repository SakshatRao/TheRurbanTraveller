import numpy as np
import matplotlib.pyplot as plt

class OBD2_Simulator:
    def __init__(self, sim_time = 24 * 60):
        self.sim_time = sim_time
        self.speed = np.zeros(sim_time)
        
        self.acc_rates = []
        self.dec_rates = []
        self.top_speeds = []
        self.cruise_minutes = []
        self.trip_times = []

        self.tank = 100
        self.fuel_price = np.random.uniform(80, 90)
        self.total_fuel_cost = 0
        self.refuel_level = [80, 100]
        self.fuel_lower_thresh = [20, 10]
        self.mileage = np.random.uniform(10, 15)
        self.work_distance = np.random.uniform(1, 10)
        self.work_num_traffic_signals = np.random.uniform(0, 5)
        self.sleeping_times = [np.random.uniform(9, 12), np.random.uniform(6, 9)]
    
    def check_speed_limits(self):
        self.speed[self.speed < 0] = 0
    
    def add_random_traffic(self):
        non_zero_speed = (self.speed != 0)
        random_traffic_var = np.random.normal(0, 8, self.speed.shape[0])
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
        plt.show()
    
    def add_acc_cruise_dec(self, idx, acc_rate, dec_rate, top_speed, cruise_minutes):
        start = self.add_acceleration(acc_rate, top_speed)
        self.speed[idx: idx + start.shape[0]] = start
        mid = self.add_cruise(top_speed, cruise_minutes)
        self.speed[idx + start.shape[0]: idx + start.shape[0] + mid.shape[0]] = mid
        end = self.add_deceleration(dec_rate, top_speed)
        self.speed[idx + start.shape[0] + mid.shape[0]: idx + start.shape[0] + mid.shape[0] + end.shape[0]] = end
    
    def randomize_cruise_params(self):
        for idx, trip_time in enumerate(self.trip_times):
            self.acc_rates[idx] = np.random.normal(75, 20)
            self.dec_rates[idx] = np.random.normal(75, 20)
            self.top_speeds[idx] = np.random.normal(50, 10)
            self.cruise_minutes[idx] = int(np.round(np.random.normal(10, 3)))
    
    def simulate_speed(self):
        self.trip_times = [20, 60, 100]
        self.acc_rates = np.zeros(len(self.trip_times))
        self.dec_rates = np.zeros(len(self.trip_times))
        self.top_speeds = np.zeros(len(self.trip_times))
        self.cruise_minutes = np.zeros(len(self.trip_times), dtype = np.int32)
        self.randomize_cruise_params()
        for trip_time, acc_rate, dec_rate, top_speed, cruise_minute in zip(self.trip_times, self.acc_rates, self.dec_rates, self.top_speeds, self.cruise_minutes):
            self.add_acc_cruise_dec(trip_time, acc_rate, dec_rate, top_speed, cruise_minute)
        self.add_random_traffic()

obd2_sim = OBD2_Simulator(3 * 60)
obd2_sim.simulate_speed()
obd2_sim.plot_speed()