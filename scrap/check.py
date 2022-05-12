import pandas as pd

df = pd.read_csv("./hobby.csv", header=None)

print(df.describe())