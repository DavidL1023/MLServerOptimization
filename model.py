import pandas as pd
from statsmodels.tsa.seasonal import STL
import matplotlib.pyplot as plt
dataframe = pd.read_csv("24h_data.csv")
dataframe = pd.Series(dataframe["95th"])
print(dataframe)
model = STL(dataframe,period=7)
result = model.fit()
