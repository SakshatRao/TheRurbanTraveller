import numpy as np
import matplotlib.pyplot as plt

class OBD2_Simulator:
    def __init__(self, sim_time = 24 * 60, debug = False):
        self.debug = debug
        self.sim_time = sim_time
        self.speed = np.zeros(self.sim_time)
        self.refuels = []
        
        self.acc_rates = []
        self.dec_rates = []
        self.top_speeds = []
        self.cruise_minutes = []
        self.trip_times = []
        self.office_trips = []

        self.ACC_RATE_AVG = 35 / 60     # km/min2
        self.ACC_RATE_VAR = 3 / 60
        self.DEC_RATE_AVG = 35 / 60     # km/min2
        self.DEC_RATE_VAR = 3 / 60
        self.TOP_SPEED_AVG = 35 / 60    # km/min
        self.TOP_SPEED_VAR = 10 / 60
        self.CRUISE_MINUTE_AVG = 5      # min
        self.CRUISE_MINUTE_VAR = 1

        self.tank = 50 # litres
        self.tank_capacity = 50 # litres
        self.fuel_price = np.random.uniform(80, 90) # Rs.
        self.total_fuel_cost = 0 # Rs.
        self.refuel_level = [80, 100] # Percentage
        self.fuel_lower_thresh = [20, 10] # Percentage
        self.mileage = np.random.uniform(10, 15) # km/l
        self.work_distance = np.random.uniform(5, 10)
        if(self.debug == True):
            print(f"Work Distance: {self.work_distance}")
    
    def check_speed_limits(self):
        self.speed[self.speed < 0] = 0
    
    def add_random_traffic(self):
        non_zero_speed = (self.speed != 0)
        random_traffic_var = np.random.normal(0, 4/60, self.speed.shape[0])
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
        plt.yticks(np.arange(0, 10) * 10 / 60, labels = np.arange(0, 10) * 10)
        plt.show()
    
    def add_acc_cruise_dec(self, idx, acc_rate, dec_rate, top_speed, cruise_minutes):
        start = self.add_acceleration(acc_rate, top_speed)
        self.speed[idx: idx + start.shape[0]] = start
        mid = self.add_cruise(top_speed, cruise_minutes)
        self.speed[idx + start.shape[0]: idx + start.shape[0] + mid.shape[0]] = mid
        end = self.add_deceleration(dec_rate, top_speed)
        self.speed[idx + start.shape[0] + mid.shape[0]: idx + start.shape[0] + mid.shape[0] + end.shape[0]] = end

        # Fuel Consumption
        # print("Fuel Stats")
        # print(((top_speed ** 2) / (2 * acc_rate)))
        # print(((top_speed ** 2) / (2 * dec_rate)))
        # print((top_speed * cruise_minutes))
        self.tank -= (((top_speed ** 2) / (2 * acc_rate)) + ((top_speed ** 2) / (2 * dec_rate)) + (top_speed * cruise_minutes)) / self.mileage
    
    def randomize_cruise_params(self):
        for idx in np.arange(self.trip_times.shape[0]):
            while_iter = 0
            while(while_iter < 1000):
                try:
                    self.acc_rates[idx] = np.random.normal(self.ACC_RATE_AVG, self.ACC_RATE_VAR)
                    self.dec_rates[idx] = np.random.normal(self.DEC_RATE_AVG, self.DEC_RATE_VAR)
                    
                    if(idx < self.trip_times.shape[0] - 1):
                        time_diff = self.trip_times[idx + 1] - self.trip_times[idx]
                        max_top_speed = (time_diff - self.CRUISE_MINUTE_AVG) / (2 * ((1 / self.ACC_RATE_AVG) + (1 / self.DEC_RATE_AVG)))
                        if(max_top_speed < self.TOP_SPEED_AVG):
                            self.top_speeds[idx] = np.random.normal(max_top_speed - 1.65 * self.TOP_SPEED_VAR, self.TOP_SPEED_VAR)
                            if(self.top_speeds[idx] < 0):
                                self.top_speeds[idx] = 0
                        else:
                            self.top_speeds[idx] = np.random.normal(self.TOP_SPEED_AVG, self.TOP_SPEED_VAR)
                    else:
                        self.top_speeds[idx] = np.random.normal(self.TOP_SPEED_AVG, self.TOP_SPEED_VAR)
                    
                    if(self.office_trips[idx] == True):
                        self.cruise_minutes[idx] = (self.work_distance - ((self.top_speeds[idx] ** 2) / (2 * self.acc_rates[idx])) - ((self.top_speeds[idx] ** 2) / (2 * self.dec_rates[idx]))) / self.top_speeds[idx]
                    else:
                        self.cruise_minutes[idx] = int(np.round(np.random.normal(self.CRUISE_MINUTE_AVG, self.CRUISE_MINUTE_VAR)))
                    break
                except:
                    while_iter += 1
            
            if(self.debug == True):
                print(idx)
                print(self.acc_rates[idx])
                print(self.dec_rates[idx])
                print(self.top_speeds[idx])
                print(self.cruise_minutes[idx])
    
    def randomize_trip_times(self):
        
        # Even number of trips more probable (to-fro)
        num_trips = np.random.choice([0, 1, 2, 3, 4, 5], p = [1/12, 1/12, 4/12, 2/12, 3/12, 1/12])
        
        self.trip_times = np.zeros(num_trips, dtype = np.int32)
        self.office_trips = np.zeros(num_trips, dtype = bool)
        if(num_trips >= 2):
            self.trip_times[0] = int(np.random.normal(9 * 60, 0.5 * 60))
            self.office_trips[0] = True
            self.trip_times[1] = int(np.random.normal(17 * 60, 0.5 * 60))
            self.office_trips[1] = True
            if(num_trips > 2):
                remaining_trip_times = np.random.uniform(18 * 60, 22 * 60, num_trips - 2)
                remaining_trip_times = np.sort(remaining_trip_times)
                for trip_idx, trip_time in enumerate(remaining_trip_times):
                    self.trip_times[2 + trip_idx] = int(trip_time)
                    self.office_trips[2 + trip_idx] = False
        elif(num_trips == 1):
            self.trip_times[0] = int(np.random.uniform(8, 22))
            self.office_trips[0] = False
    
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
            self.monitor_fuel(trip_time)
            self.add_acc_cruise_dec(trip_time, acc_rate, dec_rate, top_speed, cruise_minute)
        self.add_random_traffic()
    
    def monitor_fuel(self, trip_time):
        if(self.tank / self.tank_capacity * 100 < np.random.uniform(self.fuel_lower_thresh[1], self.fuel_lower_thresh[0])):
            print("<<<<<<<<< Refueling >>>>>>>>>")
            new_fuel_level = self.tank_capacity * np.random.uniform(self.refuel_level[0], self.refuel_level[1]) / 100
            self.total_fuel_cost = (new_fuel_level - self.tank) * self.fuel_price
            self.tank = new_fuel_level
            self.refuels.append(trip_time)

NUM_SIMS = 365
fuel_data = []
speed_data = np.zeros((NUM_SIMS, 24 * 60))
obd2_sim = OBD2_Simulator()

SEED = np.random.randint(0, 1000)
print(f"Seed - {SEED}")

for sim_iter in np.arange(NUM_SIMS):
    sim_success = False
    modifier = 0
    print(f"Starting iteration {sim_iter + 1}")
    obd2_sim.simulate_speed(SEED + sim_iter + modifier)
    speed_data[sim_iter, :] = obd2_sim.speed
    fuel_data.extend([(x + 24 * 60 * sim_iter) / (24 * 60) for x in obd2_sim.refuels])

fuel_cost = obd2_sim.total_fuel_cost

print("Done")
print(fuel_data)
print(fuel_cost)
# np.save(open('./speed_time_series_data.npy', 'wb'), speed_data)







# obd2_sim = OBD2_Simulator(debug = True)
# obd2_sim.simulate_speed(281 + 743 - 1)