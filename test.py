import urllib.parse
import json
import csv
import requests
import os
from multiprocessing.dummy import Pool
from functools import partial


def stock_data_spider(stock, stock_data_url_base, stock_data_dir, stock_data_header):

    symbol = stock["symbol"]
    url = stock_data_url_base + symbol + ".js"
    response = requests.get(url)
    data_list = response.text.split("\\n\\")[2:]
    print(f"完成爬取股票{symbol}")
    file = open(stock_data_dir+'/'+symbol+".csv",
                'w', newline='', encoding='utf-8')
    file_writer = csv.writer(file, delimiter=',',
                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(stock_data_header)
    for data in data_list:
        file_writer.writerow(data.strip().split(' '))
    file.close()


stock_list = [{'symbol': 'sh000001', 'name': '上证指数'}, {
    'symbol': 'sz399001', 'name': '深证成指'}, {'symbol': 'sh000300', 'name': '沪深300'}]
stock_list_url_base = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php'

print("downloading stock list...")
cnt = 0
while(True):
    cnt += 1
    r_params = {'__s': '[["hq","hs_a","",0,' + str(cnt) + ',500]]'}
    response = requests.get(stock_list_url_base, r_params)
    if(len(response.json()[0]['items']) == 0):
        break

    for item in response.json()[0]['items']:
        stock_list.append({'symbol': item[0], 'name': item[2]})

print(f"get {len(stock_list)} stocks")
test_list_file = open("test_list.csv", 'w', encoding='utf-8')
test_list_file_writer = csv.writer(test_list_file)
test_list_file_writer.writerow(["symbol", "name"])
for stock in stock_list:
    test_list_file_writer.writerow([stock["symbol"], stock["name"]])
print(f"save stocks to file")

stock_data_url_base = 'http://data.gtimg.cn/flashdata/hushen/latest/daily/'
stock_data_dir = "./test_data"
if not os.path.exists(stock_data_dir):
    os.makedirs(stock_data_dir)
stock_data_header = ["date", "open", "close", "high", "low", "volumn"]
print("downloading stock data...")
mapfunc = partial(stock_data_spider, stock_data_url_base=stock_data_url_base,
                  stock_data_dir=stock_data_dir, stock_data_header=stock_data_header)
pool = Pool(os.cpu_count())
pool.map(mapfunc, stock_list)   # 多线程执行下载工作
pool.close()
pool.join()
