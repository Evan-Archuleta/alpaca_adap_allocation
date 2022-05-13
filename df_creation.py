import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame 
from config import *
from tickers import *
import pandas as pd
import numpy as np
import pandas_datareader
import datetime

# API setup 
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL, api_version='v2')

#create df -- references config for days of data to pull. Adjust there 
df = pd.DataFrame()
stock = []
for ticker in tickers:
    bar = api.get_bars(ticker, TimeFrame.Day, start=start).df#, end=end).df
    #print(bar)
    #df[ticker.upper()] = bar[ticker,  'close']
    df[ticker.upper()] = bar['close']

# trim the date 
df.index = df.index.strftime("%Y-%m-%d")

## Export raw data to CSV 
#df.to_csv("ticker_data.csv", header=True)
#print('dataframe exported')
# change to integrate to previous format 
df2 = df.copy()

# ##*******************   Import yahoo data from Google Colab     *************************************                  
# # df2 = pd.read_csv("yfinance_df.csv")
# # df2.rename( columns={'Unnamed: 0':'Date'}, inplace=True )
# # df2.set_index(keys="Date", inplace = True)

## Calculate Historical Volatility (90 days)
returns = df2.pct_change()
df_returns = returns.backfill()                    # df_returns = returns.dropna() 
df_returns = df_returns.tail(64)
hist_vol = (df_returns.std())*(252**.5)
hist_vol = pd.DataFrame(hist_vol, columns=['Hist_Vol'])
hist_vol2 = hist_vol.T

## 200 day moving average  = 142 bus days 
df_ma = df2.tail(142)
ma_200 = df_ma.mean()
ma_df = pd.DataFrame(ma_200, columns=["ma"])

### Transpose for analysis 
ma_df2 = ma_df.T
ma_df2 = ma_df2.append(df2.tail(10))

## calculate momentum ETFs
ma_df2.loc['200_Diff %'] = (ma_df2.iloc[-1] / ma_df2.loc['ma']) -1
ma_df2.loc['10_Diff %'] = (ma_df2.iloc[-2] / ma_df2.iloc[1]) -1 

## add Hist IV
ma_df2 = ma_df2.append(hist_vol2)
df_filtered = ma_df2.T

## ETFs above 200 day MA and positive past two weeks -- Removed 
#research = df_filtered[(df_filtered['200_Diff %'] > 0) & (df_filtered['10_Diff %'] > 0)]
#research = research.sort_values('200_Diff %', ascending=False)
research = df_filtered

# calculate order size wtih inverse and sum 
research['inverse'] = 1 / research['Hist_Vol']
research = research.head(holdings)
sum_inv_hv = research['inverse'].sum()
#research["Pos_Size %"] = research['inverse'] / sum_inv_hv
#research["Pos_Size %"] = research.iloc[10] / sum_inv_hv

df = research.copy()
df['Pos_Size %'] = research['inverse'] / sum_inv_hv

# Top 10 past two weeks with pos 200MA
#print(research.head(holdings))

# Create ticker list 
tickers = df.index.tolist()

# View outputs 
print("Alpaca Data Pull")
print(df)
df.to_csv('expore.csv', header=True, index=True)
