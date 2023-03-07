import alpaca_trade_api as tradeapi
from config import *
import pandas as pd
import numpy as np 
import time
import schedule
import matplotlib.pyplot as plt
import datetime


# Set up account
api = tradeapi.REST(APIKEYID, APISECRETKEY, APIBASEURL)
portfolio = api.list_positions()
account_value = api.get_account()

# trouble shooting and more account information here 
print(account_value)
#print(portfolio)

# check print the quantity of shares for each position.
for position in portfolio:
    print("{} shares of {} daily change {}".format(position.qty, position.symbol, position.change_today))

port_val = []
time_stamp = []
df = pd.DataFrame({'timestamp': [],'port_daily_change': []})

def func():
    portfolio = api.list_positions()
    account_value = api.get_account()
    
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

    # append to portvalue
    balance_change = float(round(balance_change, 2))
    port_val.append(balance_change)

    #time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    time = (datetime.datetime.utcnow() - datetime.timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")
    time_stamp.append(time)
    df.loc[df.shape[0]] = [time, balance_change] # from time_stamp
	
    print(df)
    df.to_csv('daily_change.csv', header=True, index=False)
    plt.plot(df['port_daily_change']) #change
    plt.show()


schedule.every(5).seconds.do(func)

while True:
    schedule.run_pending()
    time.sleep(1)