# alpaca_adap_allocation

Notes 

1) To change the timeframe it's in df_creation under days. This will probably get moved to config 
    1a) This is business days. Ie 90 days results in almost 4 months of data 

2) Don't trust this data too much. It is not adjusted close -- splits look like large drops 

3) Need to revise data source from Alpca to Yahoo Finance Adjusted Close 
    3a) See if yfinance still having a hard time with daily price 
    3b) yfinance.download is failing with json
    3c) this does work on google colab for some reason. 
TODO: figure out how to get yfinance to work in VSC

4) do not write out dates as it will keep them and not auto-update duh

5) need to delete duplicate funds ie upro and spxl are both 3x s&p500 

6) number of holdings to select is in config 

7) for the first version we're using the upro, tqqq, tmf model. If less than 200 day MA will not invest 
    7a) do we go to cash in this instance? 

8) need this to update daily
TODO:    - wake up windows to run script 