import alpaca_trade_api as tradeapi
from config import *
import pandas as pd
import numpy as np 

# Set up account
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)
portfolio = api.list_positions()
account_value = api.get_account()

## check print the quantity of shares for each position.
# for position in portfolio:
#     print("{} shares of {}".format(position.qty, position.symbol))

## Market Value
print("Account Information:")
market_value = float(account_value.long_market_value)
print("Stocks Value:", market_value)

cash_value = float(account_value.cash)
print("Cash Value:", cash_value)

account_value_1 = float(account_value.portfolio_value)
print("Cash + Stocks:", account_value_1)

#print(portfolio)