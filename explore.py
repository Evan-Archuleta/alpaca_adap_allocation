import alpaca_trade_api as tradeapi
from config import *
import pandas as pd
import numpy as np 
import time
import schedule

# Set up account
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)
portfolio = api.list_positions()
account_value = api.get_account()

# trouble shooting and more account information here 
#print(account_value)
#print(portfolio)

## check print the quantity of shares for each position.
for position in portfolio:
    print("{} shares of {} daily change {}".format(position.qty, position.symbol, position.change_today))

def func():
    # print cash and portfolio values 
    print()
    cash_value = float(account_value.cash)
    print(f"Cash Value: ${cash_value}")

    account_value_1 = float(account_value.portfolio_value)
    print(f"Portfolio Balance: ${account_value_1}")

    # print portfolio performance 
    print()
    balance_change = float(account_value.equity) - float(account_value.last_equity)
    print(f'Today\'s portfolio balance change: ${balance_change:.2f}')

    todays_change = float((balance_change / account_value_1)*100)
    print(f'Today\'s portfolio change: {todays_change:.2f}%')

schedule.every(1).minutes.do(func)

while True:
    schedule.run_pending()
    time.sleep(1)