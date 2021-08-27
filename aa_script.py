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


# Portfolio Market Value
portfolio = api.list_positions()
market_value = []
for position in portfolio:
    value = float(position.market_value)
    market_value.append(value)
market_value = sum(market_value)

# Calculate Desired Shares 
def desired_shares(ticker):
    result = research['Pos_Size %'].loc[ticker]
    shares = int(result * (to_trade + market_value) / last_price(ticker))
    return(shares)

# Find shares owned 
def shares_owned(ticker):
    portfolio = api.list_positions()
    try:
        have_1 = api.get_position(ticker)
        have = float(have_1.qty)
        return(have)
    except:
        have = 0
        return(have)  

# Positions to liquidate
tickers_owned = []
portfolio = api.list_positions()
for position in portfolio:
    tickers_owned.append(position.symbol)
liquidate = np.setdiff1d(tickers_owned, tickers)

# Calculate delta of shares
shares = []
for ticker in tickers:
    #price = last_price(ticker)
    want = desired_shares(ticker)
    have = shares_owned(ticker)
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

for share, ticker in zip(shares, tickers):
    if share > 0:
        buy_order(ticker, share)
        print("Bought {} shares of {}".format(share, ticker))
    elif share < 0:
        sell_order(ticker, (share*-1)) 
        print("Sold {} shares of {}".format(share, ticker))
    else:
        print('correct allocation -- no action needed')

# check print the quantity of shares for each position.
portfolio = api.list_positions()
for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))
