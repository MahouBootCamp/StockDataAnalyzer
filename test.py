import pandas as pd

df = pd.DataFrame(
    data={"symbol": ["sh000001", "sz399001", "sh000300"], "name": ["上证指数", "深证成指", "沪深300"]})

# df = df[df.name == "上证指数"]
df = df[df["name"].str.contains("上")]
print(df)
