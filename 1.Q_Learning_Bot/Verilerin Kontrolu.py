import pandas as pd

df = pd.read_csv("btc_5min_250k.csv")
print(df.head())
print(df.info())
print(df.describe())