from calendar import week
from turtle import speed
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

speed_data = np.load('./OBD2_Simulator/Simulated_Data/speed_time_series_data.npy')
weekday_usage = [speed_data[np.arange(speed_data.shape[0])[i::7], :].flatten() for i in range(7)]
weekday_usage = [len(x[x > 0]) / len(x) for x in weekday_usage]

with open('./OBD2_Simulator/Simulated_Data/fuel_info.txt', 'r') as read_file:
    content = read_file.read().strip().split('\n')
    fuel_cost = float(content[0])
    fuel_data = [float(x) for x in content[1:]]
time_between_refuels = [fuel_data[x + 1] - fuel_data[x] for x in range(len(fuel_data) - 1)]
avg_time_between_refuels = np.mean(time_between_refuels)

fig = make_subplots(rows = 3, cols = 1, vertical_spacing = 0.2, subplot_titles = ('Speed Usage for last week (km/hr)', 'Pickup Usage for each weekday (%)', f'Estimated Cost for {len(fuel_data)} Refuels: Rs. {fuel_cost:.0f}'))

NUM_DAYS_PLOT = 7
dates = pd.date_range(datetime(2022, 1, 1, 0, 0, 0) - timedelta(days = NUM_DAYS_PLOT), datetime(2022, 1, 1, 0, 0, 0), freq = '5min')[:-1]
data = [
    go.Scatter(x = dates, y = speed_data[-NUM_DAYS_PLOT:, :].flatten() * 60),
    go.Bar(x = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], y = weekday_usage * 100),
    go.Histogram(x = time_between_refuels)
]
data = data[::-1]

fig.add_trace(data[0],
          row=3, col=1)

fig.add_trace(data[1],
          row=2, col=1)

fig.add_trace(data[2],
          row=1, col=1)

fig.update_layout(
    width = 980, height = 2000,
    font = {'size': 25},
    showlegend = False,
    hoverlabel = {'font': {'size': 30}}
)
fig.update_annotations(font_size = 40)
config = {'displayModeBar': False}
pyo.plot(fig, filename = "./WebDev/Plotly/sample.html", auto_open = False, output_type = 'file', include_plotlyjs = 'False', config = config)
# fig.show(config = config)