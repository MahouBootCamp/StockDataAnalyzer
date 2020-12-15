# MACHINE LEARNING

import numpy as np
import pandas as pd
from stock_analysis import KDJ


def MLDataPrepare(symbol: str):
    stock_data = pd.read_csv("./data/" + symbol + ".csv",
                             index_col=0, parse_dates=True)
    stock_data.index.name = "Date"

    stock_data = KDJ(stock_data).reset_index()[
        ["close", "K", "D", "J"]].to_numpy()
    close_array = stock_data[:, 0]
    change_array = (close_array[1:] - close_array[:-1]) / close_array[:-1]
    change_array = np.insert(change_array, 0, 0)
    stock_data = np.column_stack((stock_data, change_array))
    stock_data = np.delete(stock_data, 0, 1)
    x_array = np.empty([0, 36])
    y_array = np.empty([1, 0])
    for i in range(30, 100):  # 自30日开始，以前9日的涨跌幅、KDJ值为输入，以当日涨跌幅为输出
        x = stock_data[i-9:i].flatten()
        c = stock_data[i, 3]
        y = 0
        if c > 0.3:
            y = 1
        elif c < 0.3:
            y = 2
        x_array = np.row_stack((x_array, x))
        y_array = np.append(y_array, y)
    return x_array, y_array


stock_list = pd.read_csv("./stock_list.csv")
print(stock_list.head())
print(stock_list.shape)
stock_list = stock_list.sample(110).reset_index(drop=True)  # 挑选100家数据用于训练，10家用于测试


x_train = np.empty([0, 36])
y_train = np.empty([1, 0])
x_test = np.empty([0, 36])
y_test = np.empty([1, 0])

for i in range(100):
    x_array, y_array = MLDataPrepare(stock_list.at[i, "symbol"])
    x_train = np.row_stack((x_train, x_array))
    y_train = np.append(y_train, y_array)
for i in range(100, 110):
    x_array, y_array = MLDataPrepare(stock_list.at[i, "symbol"])
    x_test = np.row_stack((x_test, x_array))
    y_test = np.append(y_test, y_array)

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)
