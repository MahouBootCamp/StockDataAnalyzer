import os
import csv
import numpy as np
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt


def KDJ(stock_data):
    days = stock_data.shape[0]
    k = [50.0]*9
    d = [50.0]*9
    j = [50.0]*9

    for i in range(9, days):
        lown = stock_data["low"][i-9:i].min()
        highn = stock_data["high"][i-9:i].max()
        closen = stock_data["close"][i]
        rsvn = 100 * (closen - lown) / (highn - lown)
        kn = 2/3*k[i-1] + 1/3*rsvn
        dn = 2/3*d[i-1] + 1/3*kn
        jn = 3*dn-2*kn
        if jn > 100.0:
            jn = 100.0
        if jn < 0.0:
            jn = 0.0
        k.append(kn)
        d.append(dn)
        j.append(jn)

    kdj = pd.DataFrame(data={"K": k, "D": d, "J": j})
    stock_data = stock_data.reset_index().join(kdj).set_index("Date")
    stock_data.loc[:9, "K"] = np.nan
    stock_data.loc[:9, "D"] = np.nan
    stock_data.loc[:9, "J"] = np.nan
    return stock_data


def StockAnalysis(symbol: str):
    stock_data = pd.read_csv("./data/" + symbol + ".csv",
                             index_col=0, parse_dates=True)
    stock_data.index.name = "Date"

    stock_data = KDJ(stock_data)

    aps = [
        mpf.make_addplot(stock_data["K"], panel=1, color="r"),
        mpf.make_addplot(stock_data["D"], panel=1, color="g"),
        mpf.make_addplot(stock_data["J"], panel=1, color="b")
    ]

    mpf.plot(stock_data, type='candle', mav=(5, 10, 15), volume=True,
             title=symbol, datetime_format="%Y%m%d", addplot=aps, panel_ratios=(1, 1), figratio=(2, 1), figscale=1.5)


# symbol = "sh000001"
# StockAnalysis(symbol)
