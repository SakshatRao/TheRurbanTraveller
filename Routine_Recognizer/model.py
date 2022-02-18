import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import autocorrelation_plot
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

dates = pd.date_range(datetime(2021, 1, 1, 0, 0, 0), periods = 365 * 24 * 60 // 30, freq = '30min')
speed_data = np.load(open('./OBD2_Simulator/Simulated_Data/speed_time_series_data.npy', 'rb'))
# speed_data = np.repeat(speed_data, 5, axis = 1)
flat_speed_data = speed_data.flatten()
speed_timeseries_df = pd.Series(flat_speed_data, index = dates)

TRAINING_DAYS = 10
speed_timeseries_df = speed_timeseries_df.head(TRAINING_DAYS * 24 * 60 // 30)
print(speed_timeseries_df.head())

# fit model
model = ARIMA(speed_timeseries_df, order=(24 * 60 // 30, 1, 0))
model_fit = model.fit(low_memory = True)

FORECAST_DAYS = 7
forecast_dates = pd.date_range(speed_timeseries_df.index[speed_timeseries_df.shape[0] - 1], freq = '30min', periods = FORECAST_DAYS * 24 * 60 // 30)
forecast = model_fit.forecast(FORECAST_DAYS * 24 * 60 // 30)
forecast_timeseries_df = pd.Series(forecast, index = forecast_dates)

final_timeseries_df = pd.DataFrame(pd.concat([speed_timeseries_df, forecast_timeseries_df], axis = 0), columns = ['speed'])
final_timeseries_df = final_timeseries_df.assign(is_forecast = np.concatenate([np.zeros(TRAINING_DAYS * 24 * 60 // 30), np.ones(FORECAST_DAYS * 24 * 60 // 30)]))
final_timeseries_df = final_timeseries_df.reset_index(drop = False)

# print(final_timeseries_df.shape)
# print(final_timeseries_df.tail(5))

sns.lineplot(x = 'index', y = 'speed', hue = 'is_forecast', data = final_timeseries_df)
plt.show()