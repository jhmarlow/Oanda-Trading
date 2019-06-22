from datetime import datetime, timedelta
import pandas as pd
import oandapy
import configparser

config = configparser.ConfigParser()
config.read('/Users/jacobmarlow/Documents/Data Analytics/GitHub/Oanda-Trading/config_v20.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']

oanda = oandapy.API(environment="practice", 
                    access_token=access_token)


class MyStreamer(oandapy.Streamer):
    def __init__(self, count=10, *args, **kwargs):
        super(MyStreamer, self).__init__(*args, **kwargs)
        self.count = count
        self.reccnt = 0

    def on_success(self, data):
        print(data, "\n")
        self.reccnt += 1
        if self.reccnt == self.count:
            self.disconnect()

    def on_error(self, data):
        print('error')
        self.disconnect()

stream = MyStreamer(environment="practice", 
                    access_token=access_token)
stream.rates(accountID, instruments="EUR_USD")

print('end')