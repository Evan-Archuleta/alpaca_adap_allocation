import alpaca_trade_api as tradeapi
from config import *
from tickers import *
import pandas as pd
import numpy as np
import pandas_datareader

api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

# create df -- references config for days of data to pull. Adjust there 

# df = pd.DataFrame()
# stock = []
# for ticker in tickers:
#     bar = api.get_barset(ticker, 'day', limit=days).df
#     df[ticker.upper()] = bar[ticker,  'close']

# # trim the date 
# df.index = df.index.strftime("%Y-%m-%d")

# #export raw data
# df.to_csv("ticker_data.csv", header=True)
# print('dataframe exported')


df2 = pd.read_csv("yfinance_df.csv")
print(df2.shape)

df2.rename( columns={'Unnamed: 0':'Date'}, inplace=True )
df2.set_index(keys="Date", inplace = True)

## historical 90 day vol 

returns = df2.pct_change()
df_returns = returns.dropna()
df_returns = df_returns.tail(64)

hist_vol = (df_returns.std())*(252**.5)
print(hist_vol)

print(df_returns.shape)
print(df_returns.head())