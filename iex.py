import pyEX as p
from config import *

c = p.Client(api_token= YOUR_API_TOKEN, version='stable') 

sym='UPRO'
d = c.quote(symbol=sym)
price = d['latestPrice']

print(price)