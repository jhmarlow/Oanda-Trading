
import pandas as pd
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import configparser

config = configparser.ConfigParser()
config.read('config_v20.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']
api = API(access_token=access_token)

params = {"instruments": "EUR_USD"}

r = pricing.PricingInfo(accountID=accountID, params=params)

rv = api.request(r)
info = r.response


print(pd.DataFrame(r.response['prices']))

# Normalizing the returned .json lists
info_df = pd.io.json.json_normalize(info['prices'][0])
print(info_df)

ask_prices = r.response['prices'][0]['asks']
print(ask_prices)

df = pd.io.json.json_normalize(ask_prices)
print(df)