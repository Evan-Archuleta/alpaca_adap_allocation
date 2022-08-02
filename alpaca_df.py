import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame 
from config import *
from tickers import *
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# API setup 
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL, api_version='v2')

#create df -- references config for days of data to pull. Adjust there 
df = pd.DataFrame()
stock = []
for ticker in tickers:
    bar = api.get_bars(ticker, TimeFrame.Day, start=start, adjustment='all').df
    df[ticker.upper()] = bar['close']

# trim the date 
df.index = df.index.strftime("%Y-%m-%d")
df2 = df.copy()

## Calculate Historical Volatility (90 days)
returns = df2.pct_change()
df_returns = returns.backfill()                    
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
research = df_filtered.copy()

# calculate order size wtih inverse and sum 
research['inverse'] = 1 / research['Hist_Vol']
research = research.head(holdings)
sum_inv_hv = research['inverse'].sum()
df = research.copy()
df['Pos_Size %'] = research['inverse'] / sum_inv_hv

#### EDITS HERE

## ETFs above 200 day MA and positive past two weeks
research = df_filtered[(df_filtered['200_Diff %'] > 0) & (df_filtered['10_Diff %'] > 0)]
research = research.sort_values('200_Diff %', ascending=False)

# calculate order size wtih inverse and sum 
research['inverse'] = 1 / research['Hist_Vol']
research = research.head(holdings)
sum_inv_hv = research['inverse'].sum()
df = research.copy()
df['Pos_Size %'] = research['inverse'] / sum_inv_hv

# Create ticker list 
tickers = df.index.tolist()

### END EDITS HERE


# View outputs 
print("Alpaca Data Pull")
print(df)
