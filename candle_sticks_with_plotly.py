import plotly.plotly as py
import plotly.graph_objs as go
import plotly

import pandas as pd
from datetime import datetime

plotly.tools.set_credentials_file(username='jmarlow1', api_key='f5s2qVQP91fs8xoAnGKC')

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

trace = go.Candlestick(x=df['Date'],
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close'])
data = [trace]
py.iplot(data, filename='simple_candlestick')