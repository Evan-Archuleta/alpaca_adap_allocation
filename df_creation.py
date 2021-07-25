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

## historical 90 day vol -- check for accuracy https://www.etfreplay.com/volatility.aspx

returns = df2.pct_change()
df_returns = returns.dropna()
df_returns = df_returns.tail(64)
hist_vol = (df_returns.std())*(252**.5)
print(hist_vol)

## 200 day moving average  = 142 bus days 

df_ma = df2.tail(142)
ma_200 = df_ma.mean()

print(ma_200)

ma_df = pd.DataFrame(ma_200, columns=["ma"])
ma_df2 = ma_df.T
ma_df2 = ma_df2.append(df2.tail(1))

ma_df2.loc['Diff'] = ma_df2.loc['2021-07-23'] - ma_df2.loc['ma'] 
ma_df2.loc['Diff %'] = (ma_df2.loc['2021-07-23'] / ma_df2.loc['ma']) -1

df_filtered = ma_df2.T

print(df_filtered)

df_filtered = df_filtered[df_filtered['Diff %'] > 0 ]
sort = df_filtered['Diff %'].sort_values(ascending=False)
print(sort)