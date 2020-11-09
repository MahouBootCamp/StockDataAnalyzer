import scrapy
import scrapy.http
import os
import csv
import threading


class StockDataSpider(scrapy.Spider):
    """
    爬虫类：用于爬取股票数据
    """

    def __init__(self):
        """根据相关参数初始化"""

        # self.stock_data_file = open(
        #     "stock_data.csv", 'w', newline='', encoding='utf-8')
        # self.stock_data_writer = csv.writer(self.stock_data_file, delimiter=',',
        #                                     quotechar='|', quoting=csv.QUOTE_MINIMAL)

        self.stock_list_file = open(
            "stock_list.csv", 'r', newline='', encoding='utf-8')
        self.stock_list_reader = csv.DictReader(self.stock_list_file)

        self.stock_list = []
        for row in self.stock_list_reader:
            self.stock_list.append(
                {"symbol": row["symbol"], "name": row["name"]})

        self.stock_list_file.close()

        self.url_base = "http://data.gtimg.cn/flashdata/hushen/latest/daily/"

        self.stock_data_dir = "./data"
        if not os.path.exists(self.stock_data_dir):
            os.makedirs(self.stock_data_dir)

        # 日期 开盘 收盘 最高 最低 成交量
        self.csv_header = ["date", "open", "close", "high", "low", "volumn"]

    def start_requests(self):
        for stock in self.stock_list:
            url = self.url_base + stock["symbol"] + ".js"
            yield scrapy.http.Request(url=url, callback=self.parse, dont_filter=True, cb_kwargs={"symbol": stock["symbol"]})

    def parse(self, response: scrapy.http.Response, **kwargs):
        symbol = kwargs["symbol"]  # Get the stock symbol
        data_list = response.text.split('\\n\\')[2:]
        print(f"完成爬取股票{symbol}\n")
        file = open(self.stock_data_dir+'/'+symbol+".csv",
                    'w', newline='', encoding='utf-8')
        file_writer = csv.writer(file, delimiter=',',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(self.csv_header)
        for data in data_list:
            file_writer.writerow(data.strip().split(' '))
        file.close()

    # def parse(self, response: scrapy.http.Response, **kwargs):
    #     symbol = kwargs["symbol"]  # Get the stock symbol
    #     t = threading.Thread(
    #         target=save_data, name='SaveDataThread', symbol=symbol, text=response.text)
    #     t.start()

    # def save_data(self, symbol, text):
    #     print(f"完成爬取股票{symbol}\n")
    #     data_list = text.split('\\n\\')[2:]
    #     file = open(self.stock_data_dir+'/'+symbol+".csv",
    #                 'w', newline='', encoding='utf-8')
    #     file_writer = csv.writer(file, delimiter=',',
    #                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     file_writer.writerow(self.csv_header)
    #     for data in data_list:
    #         file_writer.writerow(data.strip().split(' '))
    #     file.close()
