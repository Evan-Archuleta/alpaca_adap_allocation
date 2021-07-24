import alpaca_trade_api as tradeapi
from config import *
from tickers import *
import pandas as pd
import numpy as np

api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

# create df -- references config for days of data to pull. Adjust there 

df = pd.DataFrame()
stock = []
for ticker in tickers:
    bar = api.get_barset(ticker, 'day', limit=days).df
    df[ticker.upper()] = bar[ticker,  'close']

# trim the date 
df.index = df.index.strftime("%Y-%m-%d")

df.to_csv("ticker_data.csv", header=True)

print('dataframe exported')