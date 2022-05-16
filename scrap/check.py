import pandas as pd

df = pd.read_csv("./posts.csv", header=None)

print(df.describe())
print(df.info())