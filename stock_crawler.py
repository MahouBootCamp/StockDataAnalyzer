import urllib.parse
import json
import csv
import requests
import os
from datetime import datetime
from multiprocessing.dummy import Pool
from functools import partial
import pandas as pd


def stock_list_spider():
    # 默认添加三个全局指数
    stock_list = pd.DataFrame(
        data={"symbol": ["sh000001", "sz399001", "sh000300"], "name": ["上证指数", "深证成指", "沪深300"]})
    # stock_list = [{'symbol': 'sh000001', 'name': '上证指数'}, {
    #     'symbol': 'sz399001', 'name': '深证成指'}, {'symbol': 'sh000300', 'name': '沪深300'}]
    stock_list_url_base = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php'
    print("爬取股票列表中...")
    cnt = 0

    # 循环爬取股票
    while(True):
        cnt += 1
        # 该接口的参数列表，500为该接口一次支持的最大爬取数量
        r_params = {'__s': '[["hq","hs_a","",0,' + str(cnt) + ',500]]'}
        response = requests.get(stock_list_url_base, r_params)
        # 如果爬取到的数据数量为空，则说明已经没有更多股票，退出。
        if(len(response.json()[0]['items']) == 0):
            break
        # 向列表添加该股票
        for item in response.json()[0]['items']:
            stock_list = stock_list.append(
                {'symbol': item[0], 'name': item[2]}, ignore_index=True)

    print(f"爬取 {stock_list.shape[0]} 支股票")

    # Review: 需要保存嘛？
    # 保存股票列表至./stock_list.csv
    stock_list.to_csv("./stock_list.csv", index=False)

    return stock_list


def stock_data_spider(stock: str):
    stock_data_url_base = 'http://data.gtimg.cn/flashdata/hushen/latest/daily/'
    stock_data_dir = "./data"
    # 我们的交易数据将以如下的美股通用ohlc数据格式存储为csv文件
    # DOHLCV：日期 开盘 最高 最低 收盘 交易量
    stock_data_header = ["date", "open", "high", "low", "close", "volume"]

    url = stock_data_url_base + stock + ".js"
    response = requests.get(url)
    data_list = response.text.split("\\n\\")[2:-1]  # 剔除标题信息以及最后一行垃圾信息

    print(f"完成爬取股票{stock}")

    # 保存至./data/[股票代码].csv
    file = open(stock_data_dir+'/'+stock+".csv",
                'w', newline='', encoding='utf-8')
    file_writer = csv.writer(file)
    file_writer.writerow(stock_data_header)
    for data in data_list:
        data_array = data.strip().split(' ')
        # 接口的数据格式为 日期 开盘 收盘 最高 最低 交易量
        # 这里需要手动修改格式
        file_writer.writerow([datetime.strptime(data_array[0], "%y%m%d").date(), data_array[1], data_array[3],
                              data_array[4], data_array[2], data_array[5]])
    file.close()

    # 输出获得的首个交易日期及数据长度（默认100个）
    data_lens = len(data_list)
    if data_lens > 0:  # 检查以避免刚上市无交易数据的新股导致程序崩溃
        first_date = datetime.strptime(
            data_list[0].strip().split(' ')[0], "%y%m%d").date()
        return {"first_date": pd.Timestamp(first_date), "data_lens": data_lens}
    else:
        return {"first_date": pd.Timestamp(datetime.today()), "data_lens": data_lens}


stock_list = stock_list_spider()

stock_list = stock_list[~stock_list["name"].str.contains("ST")]
stock_list.reset_index()
print(f"清洗ST股后剩余 {stock_list.shape[0]} 支")

stock_data_dir = "./data"
if not os.path.exists(stock_data_dir):
    os.makedirs(stock_data_dir)
mapfunc = partial(stock_data_spider)
pool = Pool(6) # 在核特别多的机器上可能会被接口ban
# pool = Pool(os.cpu_count())
stock_data_dict = pool.map(mapfunc, stock_list["symbol"])   # 多线程执行下载工作
pool.close()
pool.join()
print(f"完成爬取 {len(stock_data_dict)} 支")

stock_list = stock_list.join(pd.DataFrame(data=stock_data_dict))
stock_list = stock_list[stock_list["data_lens"] == 100]
print(f"清洗交易日不满一百的股票后剩余 {stock_list.shape[0]} 支")
first_date = stock_list.loc[stock_list["symbol"]
                            == "sh000001"].at[0, "first_date"]
stock_list = stock_list[stock_list["first_date"] == first_date]
print(f"清洗首个交易日与大盘数据不同的股票后剩余 {stock_list.shape[0]} 支")
# print(stock_list.head(20))
