import numpy as np
import pandas as pd
import datetime
import yfinance as yf

now = datetime.datetime.now()
start = datetime.datetime((now.year-1), now.month, now.day)
end = datetime.datetime(now.year, now.month, now.day)
dates= pd.date_range(start, end)
df = pd.DataFrame(index=dates)

tickers = ["TMF", "UPRO", "TQQQ"]

stock = []
for ticker in tickers:
  stocks = yf.download(ticker.upper(),start=start, end=end, progress=False)
  df[ticker.upper()] = stocks['Adj Close']
  
df.backfill(axis=0, inplace = True)
df.tail(5)