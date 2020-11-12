import scrapy
import scrapy.http
import urllib.parse
import json
import os
import csv


class StockListSpider(scrapy.Spider):
    """
    爬虫类：用于爬取股票列表
    """

    def __init__(self):
        """根据相关参数初始化"""

        # 新浪股票列表API地址
        self.stock_url_base = urllib.parse.urlunparse(
            ("http", "money.finance.sina.com.cn", "/d/api/openapi_proxy.php", "", "", ""))
        # 用一个list存储获取的股票列表
        self.stock_list = [{"symbol": "sh000001", "name": "上证指数"}, {
            "symbol": "sz399001", "name": "深证成指"}, {"symbol": "sh000300", "name": "沪深300"}]
        self.cnt = 0  # 从1开始
        print("开始爬取股票列表...")

    def stock_url_builder(self, cnt: int) -> str:
        """
        返回补全后的新浪股票列表API\n
        每一个cnt含500个股票\n
        cnt不得小于等于0\n
        """
        r_params = {'__s': '[["hq","hs_a","",0,' + str(cnt) + ',500]]'}
        return self.stock_url_base + '?' + urllib.parse.urlencode(r_params)

    def start_requests(self):
        self.cnt += 1
        tmp_url = self.stock_url_builder(
            self.cnt)
        yield scrapy.http.Request(url=tmp_url, callback=self.parse, dont_filter=True)

    def parse(self, response: scrapy.http.Response, **kwargs):
        """
        解析爬取的json数据\n
        如数据为空，则没有更多股票，退出\n
        如不为空，则重复调用scrapy.http.Request()函数\n
        """
        text_in_json = json.loads(response.text)
        stock_items = text_in_json[0]["items"]
        if(len(stock_items) == 0):
            pass  # 没有更多股票，退出
        else:
            for item in stock_items:
                self.stock_list.append({"symbol": item[0], "name": item[2]})
            # 继续查找
            self.cnt += 1
            tmp_url = self.stock_url_builder(
                self.cnt)
            yield scrapy.http.Request(url=tmp_url, callback=self.parse, dont_filter=True)

    def closed(self, reason):
        """
        在完成爬虫后将数据写入列表文件
        """
        print("完成爬取股票列表...")
        print(f"共获得 {len(self.stock_list)} 家股票代号信息")

        file = open('stock_list.csv', 'w', newline='', encoding='utf-8')
        file_writer = csv.writer(file, delimiter=',',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(["symbol", "name"])
        for stock in self.stock_list:
            file_writer.writerow([stock["symbol"], stock["name"]])

        file.close()
