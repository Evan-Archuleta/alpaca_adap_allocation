import numpy as np
import pandas as pd
import datetime
import yfinance as yf
from config import *
from tickers import *
from df_creation import df2

# Set up dataframe
dates= pd.date_range(start, end)
df = pd.DataFrame(index=dates)


# yahoo adjusted close better data import 
stock = []
for ticker in tickers:
  stocks = yf.download(ticker.upper(),start=start, end=end, progress=False)
  df[ticker.upper()] = stocks['Adj Close']  
df.dropna(axis=0, inplace = True)

# replace last observed iex result to yahoo finance adjusted close 
#df = df.iloc[:-1,:]   ### yahoo used to report day of info which it does not anymore. Removed to avoid dropping a day 
last_row = df2.tail(1)
df = df.append(last_row)

# check dataframe

## Calculate Historical Volatility (90 days)
returns = df.pct_change()
df_returns = returns.backfill()                    # df_returns = returns.dropna() 
df_returns = df_returns.tail(64)
hist_vol = (df_returns.std())*(252**.5)
hist_vol = pd.DataFrame(hist_vol, columns=['Hist_Vol'])
hist_vol2 = hist_vol.T

## 200 day moving average  = 142 bus days 
df_ma = df.tail(142)
ma_200 = df_ma.mean()
ma_df = pd.DataFrame(ma_200, columns=["ma"])

### Transpose for analysis 
ma_df = ma_df.T
ma_df = ma_df.append(df.tail(10))

## calculate momentum ETFs
ma_df.loc['200_Diff %'] = (ma_df.iloc[-1] / ma_df.loc['ma']) -1
ma_df.loc['10_Diff %'] = (ma_df.iloc[-2] / ma_df.iloc[1]) -1 

## add Hist IV
ma_df = ma_df.append(hist_vol2)
df_filtered = ma_df.T

## ETFs above 200 day MA and positive past two weeks -- Removed 
research = df_filtered[(df_filtered['200_Diff %'] > 0) & (df_filtered['10_Diff %'] > 0)]
research = research.sort_values('200_Diff %', ascending=False)
#research = df_filtered

# calculate order size wtih inverse and sum 
research['inverse'] = 1 / research['Hist_Vol']
research = research.head(holdings)
sum_inv_hv = research['inverse'].sum()
# research["Pos_Size %"] = research['inverse'] / sum_inv_hv
# research["Pos_Size %"] = research.iloc[10] / sum_inv_hv

df = research.copy()
df['Pos_Size %'] = research['inverse'] / sum_inv_hv

# Top 10 past two weeks with pos 200MA
print(research.head(holdings))

# Create ticker list 
tickers = df.index.tolist()

# View outputs 
print("Yahoo Finance Data")
print(df)

df.to_csv('expore.csv', header=True, index=True)