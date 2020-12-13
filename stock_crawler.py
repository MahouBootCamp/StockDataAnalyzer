import urllib.parse
import json
import csv
import requests
import os
from datetime import datetime
from multiprocessing.dummy import Pool
from functools import partial


def stock_list_spider():
    # 默认添加三个全局指数
    stock_list = [{'symbol': 'sh000001', 'name': '上证指数'}, {
        'symbol': 'sz399001', 'name': '深证成指'}, {'symbol': 'sh000300', 'name': '沪深300'}]
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
            stock_list.append({'symbol': item[0], 'name': item[2]})

    print(f"爬取 {len(stock_list)} 支股票")

    # 保存股票列表至./stock_list.csv
    stock_list_file = open("stock_list.csv", 'w', encoding='utf-8', newline='')
    stock_list_file_writer = csv.writer(stock_list_file)
    stock_list_file_writer.writerow(["symbol", "name"])
    for stock in stock_list:
        stock_list_file_writer.writerow([stock["symbol"], stock["name"]])

    stock_list_file.close()

    return stock_list


def stock_data_spider(stock):
    stock_data_url_base = 'http://data.gtimg.cn/flashdata/hushen/latest/daily/'
    stock_data_dir = "./data"
    # DOHLCV：日期 开盘 最高 最低 收盘 交易量
    stock_data_header = ["date", "open", "high", "low", "close", "volume"]
    symbol = stock["symbol"]
    url = stock_data_url_base + symbol + ".js"
    response = requests.get(url)
    data_list = response.text.split("\\n\\")[2:-1]

    print(f"完成爬取股票{symbol}")

    # 保存至./data/[股票代码].csv
    file = open(stock_data_dir+'/'+symbol+".csv",
                'w', newline='', encoding='utf-8')
    file_writer = csv.writer(file)
    file_writer.writerow(stock_data_header)
    for data in data_list:
        data_array = data.strip().split(' ')
        # 接口的数据格式为 日期 开盘 收盘 最高 最低 交易量
        # 这里需要手动修改格式
        file_writer.writerow([datetime.strptime(data_array[0], "%y%m%d").date, data_array[1], data_array[3],
                              data_array[4], data_array[2], data_array[5]])

    file.close()


stock_list = stock_list_spider()



stock_data_dir = "./data"
if not os.path.exists(stock_data_dir):
    os.makedirs(stock_data_dir)
mapfunc = partial(stock_data_spider)
pool = Pool(os.cpu_count())
pool.map(mapfunc, stock_list)   # 多线程执行下载工作
pool.close()
pool.join()
