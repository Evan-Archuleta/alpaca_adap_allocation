# alpaca_adap_allocation

Notes 

1) To change the timeframe it's in df_creation under days. This will probably get moved to config 
    1a) This is business days. Ie 90 days results in almost 4 months of data 

2) Don't trust this data too much. It is not adjusted close -- splits look like large drops 
UPDATE -- IEX real time data is good. Historic we can pull from yfinance or iex 
Returning adjusted close only: 2 credits per symbol per time interval  
https://intercom.help/iexcloud/en/articles/4063720-historical-stock-prices-on-iex-cloud

3) Need to revise data source from Alpca to Yahoo Finance Adjusted Close 
    3a) See if yfinance still having a hard time with daily price 
    3b) yfinance.download is failing with json
    3c) this does work on google colab for some reason. 
TODO: figure out how to get yfinance to work in VSC -- not really necessary but would be nice to have

5) need to delete duplicate funds ie upro and spxl are both 3x s&p500 

6) number of holdings to select is in config 

7) for the first version we're using the upro, tqqq, tmf model. If less than 200 day MA will not invest 
    7a) do we go to cash in this instance? 

8) need this to update daily
TODO:    - wake up windows to run script 

Get current prices - uses 2 credits per price 
https://iexcloud.io/blog/how-to-get-market-data-in-python