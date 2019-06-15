# Algorithmic trading strategy using Oanda API


# import modules
from configparser import SafeConfigParser
import os
import oandapy as opy
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# API access ----
# If using config file to bring in tokens/account ID


def get_config_info(filepath, section, variable):

    if os.path.isfile(filepath):
        parser = SafeConfigParser()
        parser.read(filepath)
        config_token = parser.get(section, variable)
    else:
        print("CodeError: Config file not found")

    return config_token

# Access Oanda API
oanda = opy.API(environment='practice',
                access_token=get_config_info("/Users/jacobmarlow/Documents/Data Analytics/GitHub/Oanda Trading/oanda.cfg",
                                                'oanda_info', 'access_token'))

# Data to be requested
data = oanda.get_history(instrument='EUR_USD',  # our instrument
                         start='2016-12-08',  # start data
                         end='2016-12-10',  # end date
                         granularity='M1')  # minute bars

# Place data into dataframe , requested data returned in candle format
df = pd.DataFrame(data['candles']).set_index('time')
# Index against datatime
df.index = pd.DatetimeIndex(df.index)
# display retrieved data
df.info()


# Trading strategy ---
# log of close asking price divided by close asking price +1
df['returns'] = np.log(df['closeAsk'] / df['closeAsk'].shift(1))

# empty array
cols = [] 

# Plot each time strategy and instrument
for momentum in [15, 30, 60, 120]:
    col = 'position_{}'.format(momentum)
    # return whether momentum positive or negative with 'np.sign'
    # mean momentum is the window size (using 'df.rolling') 
    # considered 
    df[col] = np.sign(df['returns'].rolling(momentum).mean())
    cols.append(col)

strats = ['returns']

print('Orig')
print(df[col])
print('shift')
print(df[col].shift(1))

for col in cols:
    # window size from col names (e.g. 15, 30, etc.)
    strat = 'strategy_{}'.format(col.split('_')[1])

    df[strat] = df[col].shift(1) * df['returns']


    strats.append(strat)

df[strats].dropna().cumsum().apply(np.exp).plot()
plt.show()

# # Automated Trading ---

# class MomentumTrader(opy.Streamer):

#     def __init__(self, momentum, *args, **kwargs):
#         opy.Streamer.__init__(self, *args, **kwargs)
#         self.ticks = 0
#         self.position = 0
#         self.df = pd.DataFrame()
#         self.momentum = momentum
#         self.units = 100000

#     def create_order(self, side, units):
#         order = oanda.create_order(config['oanda']['account_id'], 
#             instrument='EUR_USD', units=units, side=side,
#             type='market')
#         print('\n', order)

#     def on_success(self, data):
#         self.ticks += 1
#         # print(self.ticks, end=', ')
#         # appends the new tick data to the DataFrame object
#         self.df = self.df.append(pd.DataFrame(data['tick'],
#                                  index=[data['tick']['time']]))
#         # transforms the time information to a DatetimeIndex object
#         self.df.index = pd.DatetimeIndex(self.df['time'])
#         # resamples the data set to a new, homogeneous interval
#         dfr = self.df.resample('5s').last()
#         # calculates the log returns
#         dfr['returns'] = np.log(dfr['ask'] / dfr['ask'].shift(1)) 
#         # derives the positioning according to the momentum strategy
#         dfr['position'] = np.sign(dfr['returns'].rolling( 
#                                       self.momentum).mean())
#         if dfr['position'].ix[-1] == 1:
#             # go long
#             if self.position == 0:
#                 self.create_order('buy', self.units)
#             elif self.position == -1:
#                 self.create_order('buy', self.units * 2)
#             self.position = 1
#         elif dfr['position'].ix[-1] == -1:
#             # go short
#             if self.position == 0:
#                 self.create_order('sell', self.units)
#             elif self.position == 1:
#                 self.create_order('sell', self.units * 2)
#             self.position = -1
#         if self.ticks == 250:
#             # close out the position
#             if self.position == 1:
#                 self.create_order('sell', self.units)
#             elif self.position == -1:
#                 self.create_order('buy', self.units)
#             self.disconnect()

# mt = MomentumTrader(momentum=12, environment='practice',
#                     access_token=config['oanda']['access_token'])

# mt.rates(account_id=config['oanda']['account_id'],
#          instruments=['DE30_EUR'], ignore_heartbeat=True)