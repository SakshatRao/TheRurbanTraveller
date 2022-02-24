import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

dates = pd.date_range(datetime(2021, 1, 1, 0, 0, 0), periods = 365 * 24 * 60, freq = '1min')
speed_data = np.load(open('./OBD2_Simulator/Simulated_Data/speed_time_series_data.npy', 'rb'))
speed_data = np.repeat(speed_data, 5, axis = 1)
flat_speed_data = speed_data.flatten()
speed_timeseries_df = pd.Series(flat_speed_data, index = dates)

WINDOW_SIZE = 10    # in days

past_n_days = speed_timeseries_df.tail(WINDOW_SIZE * 24 * 60).values.reshape(WINDOW_SIZE, -1)
past_n_weekdays = speed_timeseries_df.tail(7 * WINDOW_SIZE * 24 * 60)
past_weekdays_idx = np.arange(past_n_weekdays.shape[0] - 1)
past_weekdays_idx = past_weekdays_idx[(past_weekdays_idx // (24 * 60)) % 7 == 0]
past_n_weekdays = past_n_weekdays.iloc[past_weekdays_idx].values.reshape(WINDOW_SIZE, -1)

ALPHA = 0.7
past_n_days_forecast = past_n_days[0, :]
for idx in range(1, 7):
    past_n_days_forecast = ALPHA * past_n_days[idx, :] + (1 - ALPHA) * past_n_days_forecast
past_n_weekdays_forecast = past_n_weekdays[0, :]
for idx in range(1, 7):
    past_n_weekdays_forecast = ALPHA * past_n_weekdays[idx, :] + (1 - ALPHA) * past_n_weekdays_forecast

forecast = (past_n_days_forecast + past_n_weekdays_forecast) / 2.0
forecast = forecast / forecast.sum()
forecast = np.expand_dims(forecast, 1)

forecast_dates = pd.date_range(speed_timeseries_df.index[speed_timeseries_df.shape[0] - 1], freq = '1min', periods = 24 * 60)
forecast_timeseries_df = pd.DataFrame(forecast, index = forecast_dates, columns = ['speed']).reset_index(drop = False)

office_forecast_df = forecast_timeseries_df.iloc[1 * 60: 12 * 60]
max_speed = office_forecast_df['speed'].max()
forecasted_office_time = office_forecast_df[office_forecast_df['speed'] == max_speed].iloc[0]['index']
print(f"Forecasted Office Time: {forecasted_office_time}")

# sns.lineplot(x = 'index', y = 'speed', data = forecast_timeseries_df)
# plt.show()

remind_data_text1 = '''
var reminder = {
    remind: 1,
    time: "'''
remind_data_text2 = '''"
};

export { reminder };
'''

remind_data_text = remind_data_text1 + datetime.strftime(forecasted_office_time, "%I:%M %p") + remind_data_text2
with open('./WebDev/JSON/reminder_data.js', 'w') as save_file:
    save_file.write(remind_data_text)