import alpaca_trade_api as tradeapi
import pyEX as p   # OPTIONAL 
from config import *
from alpaca_df import df, tickers
import pandas as pd
import numpy as np

# set up accounts
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)
c = p.Client(api_token= YOUR_API_TOKEN, version='stable') 

# find tickers last price (iex data)
def last_price(ticker):
    sym=ticker
    d = c.quote(symbol=sym)
    price = d['latestPrice']
    return(price)

# # Portfolio Market Value
account_value = api.get_account()
market_value = float(account_value.portfolio_value)

# Calculate Desired Shares (iex data)
def desired_shares(ticker):
    result = df['Pos_Size %'].loc[ticker]
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

# # Positions to liquidate 
tickers_owned = []
portfolio = api.list_positions()
for position in portfolio:
    tickers_owned.append(position.symbol)
liquidate = np.setdiff1d(tickers_owned, tickers)
    

# Calculate delta of shares
shares = []
for ticker in tickers:
    price = last_price(ticker)
    want = desired_shares(ticker)
    have = shares_owned(ticker)
    share = want - have
    shares.append(share)

# buy
def buy_order(ticker, share):
    api.submit_order(
        symbol=ticker,
        qty=share,
        side='buy',
        type='market',
        time_in_force='gtc',
        #limit_price= last_price(ticker)
    )
# sell
def sell_order(ticker, share):
    api.submit_order(
        symbol=ticker,
        qty=share,
        side='sell',
        type='market',
        time_in_force='gtc',
        #limit_price= last_price(ticker)
    )

# Sell what we have and don't want 
for liquid in liquidate:   
    sell_order(liquid, shares_owned(liquid)) 
    print("Sold {} shares of {}".format(shares_owned(liquid), liquid))

# view the desired shares 
for share, ticker in zip(shares, tickers):
    print(ticker, share)

##### 08-2-22 Error discovered needs fix -- Need to sell before we buy to avoid cashflow issues
###### 8-3-22 Error fix -- sell first then buy 
    
# # buy and sell  
# for share, ticker in zip(shares, tickers):
#     if share > 0:
#         buy_order(ticker, share)
#         print("Bought {} shares of {}".format(share, ticker))
#     elif share < 0:
#         sell_order(ticker, (share*-1)) 
#         print("Sold {} shares of {}".format(share, ticker))
#     else:
#         print("correct allocation of {}".format(ticker))

#### END FIX 8-3-22

## place orders 
# sell  
for share, ticker in zip(shares, tickers):
    if share < 0:
        sell_order(ticker, (share*-1)) 
        print("Sold {} shares of {}".format(share, ticker))

# buy  
for share, ticker in zip(shares, tickers):
    if share > 0:
        buy_order(ticker, share)
        print("Bought {} shares of {}".format(share, ticker))

# check print the quantity of shares for each position.
portfolio = api.list_positions()
for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))
