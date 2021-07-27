import alpaca_trade_api as tradeapi
import pyEX as p
from config import *
from df_creation import research, tickers
import pandas as pd
import numpy as np

api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)
c = p.Client(api_token= YOUR_API_TOKEN, version='stable') 

# find tickers last price 
def last_price(ticker):
    sym=ticker
    d = c.quote(symbol=sym)
    price = d['latestPrice']
    return(price)

# Calculate Desired Shares 
def desired_shares(ticker):
    result = research['Pos_Size %'].loc[ticker]
    shares = int(result * to_trade / last_price(ticker))
    return(shares)

# Find shares owned 
portfolio = api.list_positions()
for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))

# Calculate delta of shares
shares = []
for ticker in tickers:
    #price = last_price(ticker)
    want = desired_shares(ticker)
    have = 0 #will have to do after we see how it's formatted 
    share = want - have
    shares.append(share)

## place orders 
# buy
def buy_order(ticker, share):
    api.submit_order(
        symbol=ticker,
        qty=share,
        side='buy',
        type='limit',
        time_in_force='gtc',
        limit_price= last_price(ticker)
    )
# sell
def sell_order(ticker, share):
    api.submit_order(
        symbol=ticker,
        qty=share,
        side='sell',
        type='limit',
        time_in_force='gtc',
        limit_price= last_price(ticker)
    )

print(shares)
print(tickers)

for share, ticker in zip(shares, tickers):
    if share > 0:
        buy_order(ticker, share)
        print("Bought {} shares of {}".format(share, ticker))
    elif share < 0:
        sell_order(ticker, share) 
        print("Sold {} shares of {}".format(share, ticker))
    else:
        print('correct allocation -- no action needed')


# check print the quantity of shares for each position.
portfolio = api.list_positions()
for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))




