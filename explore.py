
import alpaca_trade_api as tradeapi
#from df_creation import research
from config import *
import pandas as pd
import numpy as np 
import pandas_datareader
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)


# def have(ticker):
#     shares_owned2 = api.get_position(ticker)
#     shares_owned2 = shares_owned2.qty
#     shares_owned = int(shares_owned2)
#     return(shares_owned)
    

# print(type(have('TMF')))
# print(have('TMF'))

## check print the quantity of shares for each position.
portfolio = api.list_positions()
for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))

account_value = api.get_account()
account_value = float(account_value.last_equity)
print("Avalible to trade:", account_value)

portfolio = api.list_positions()
market_value = []
for position in portfolio:
    value = float(position.market_value)
    market_value.append(value)
market_value = sum(market_value)


print("Market Value:", market_value)
print("Portfolio Value:", (market_value+account_value))



# for position in portfolio:
#     print("{} shares of {}".format(position.qty, position.symbol))

# print('test')
# print(portfolio)   

# print('test_real')
# tmf_position = api.get_position('TMF')
# #print("test2")
# print(tmf_position.qty)
# # export df to csv 
# #print(research)
# #research.to_csv('explore.csv', header=True)
