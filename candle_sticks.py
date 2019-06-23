import pandas as pd
import oandapyV20 as opy
import configparser
from dateutil import parser
from pandas.plotting import register_matplotlib_converters
import oandapyV20.endpoints.instruments as instruments
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns

# Set figure style
sns.set()
# sns.set(style="ticks", context="talk")
# sns.set_style("whitegrid")
# plt.style.use("dark_background")
register_matplotlib_converters()

# Security info from config file
config = configparser.ConfigParser()
config.read('config_v20.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']

# Setup client to access API
client = opy.API(access_token=access_token)

# Setup request parameters
instrument_names = ["WHEAT_USD", "SUGAR_USD", "XCU_USD", "BCO_USD"]

fig, axs = plt.subplots(4,1)

data_dictionary = {}
for x, instrument in enumerate(instrument_names):

    # Parameters
    params = {
        "count": 500,
        "granularity": "H12"
        }

    r = instruments.InstrumentsCandles(instrument=instrument, params=params)

    # Make request
    submitted_request = client.request(r)
    info_response = r.response

    # Format returned data
    dat = []
    for oo in r.response['candles']:
        dat.append([oo['time'], oo['volume'], oo['mid']['o'], oo['mid']['h'],
                    oo['mid']['l'], oo['mid']['c']])

    df = pd.DataFrame(dat)
    df.columns = ['Time', 'Volume', 'Open', 'High', 'Low', 'Close']
    df = df.set_index('Time')

    df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].astype(np.float)
    # Index against datatime
    df.index = pd.DatetimeIndex(df.index)
    data_dictionary[instrument] = df
    print(df.head(n=10))

    axs[x].plot(df['Open'], linewidth=0.75, label='Open')
    axs[x].plot(df['High'], linewidth=0.75, label='High')
    axs[x].plot(df['Low'], linewidth=0.75, label='Low')
    axs[x].plot(df['Close'], linewidth=0.75, label='Close')
    plt.xticks(rotation=90)
    axs[x].set_ylabel(instrument)
    axs[x].legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()