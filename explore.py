# %%
import pandas as pd
import numpy as np 
import pandas_datareader

df = pd.read_csv('ticker_data.csv', index_col='time')
returns = df.pct_change()

# %%
returns.NAIL.hist()



# %%
df.NAIL.plot()
# %%

