import alpaca_trade_api as tradeapi
import os, sys
from config import *
import pandas as pd
import numpy as np

APIKEYID 
APISECRETKEY 
APIBASEURL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)

# # Get our account information.
# account = api.get_account()
# print('Account info:')
# print(account)

# # Check if our account is restricted from trading.
# if account.trading_blocked:
#     print('Account is currently restricted from trading.')
#     sys.exit(0)
        
# # List current positions
# print('Current positions:')
# print(api.list_positions())


# # Get daily price data for AAPL over the last 5 trading days.
# barset = api.get_barset('AAPL', 'day', limit=5)
# aapl_bars = barset['AAPL']
# print(aapl_bars)

# # See how much AAPL moved in that timeframe.
# week_open = aapl_bars[0].o
# week_close = aapl_bars[-1].c
# percent_change = (week_close - week_open) / week_open * 100
# print('AAPL moved {}% over the last 5 days'.format(percent_change))


#https://alpaca.markets/docs/api-documentation/how-to/orders/

# # Submit a market order to buy 1 share of Apple at market price
# api.submit_order(
#     symbol='AAPL',
#     qty=1,
#     side='buy',
#     type='market',
#     time_in_force='gtc'
# )

# # Submit a limit order to attempt to sell 1 share of AMD at a
# # particular price ($20.50) when the market opens
# api.submit_order(
#     symbol='AMD',
#     qty=1,
#     side='sell',
#     type='limit',
#     time_in_force='opg',
#     limit_price=20.50
# )


# Portfolio 

portfolio = api.list_positions()

# Print the quantity of shares for each position.
# for position in portfolio:
#     print("{} shares of {}".format(position.qty, position.symbol))

