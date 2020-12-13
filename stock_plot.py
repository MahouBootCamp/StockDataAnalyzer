import os
import csv
import pandas as pd
import mplfinance as mpf


def stock_plot(symbol: str, name: str):
    stock_data = pd.read_csv("./data/" + symbol + ".csv",
                             index_col=0, parse_dates=True)
    stock_data.index.name = "Date"
    mpf.plot(stock_data, type='candle', mav=(5, 10, 15), volume=True,
    title=name, datetime_format="%Y%M%d")
    return


stock_plot("sh000001", "sh000001")
