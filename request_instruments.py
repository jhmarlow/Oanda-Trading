import pandas as pd
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import configparser

config = configparser.ConfigParser()
config.read('/Users/jacobmarlow/Documents/Data Analytics/GitHub/Oanda-Trading/config_v20.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']
client = oandapyV20.API(access_token=access_token)
r = accounts.AccountInstruments(accountID=accountID, params = "EUR_USD")
info = client.request(r)

print(info)