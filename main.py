import stock_data_spider
import stock_list_spider
import scrapy

from scrapy.crawler import CrawlerProcess


def main():
    """
    主函数\n
    先获取股票列表，再查询各股票的详细数据\n
    """

    print("启动股票爬虫...\n")

    process_stock_list = CrawlerProcess(
        #     settings={
        #     "FEEDS": {
        #         "items.json": {"format": "json"},
        #     },
        # }
    )
    process_stock_list.crawl(stock_list_spider.StockListSpider)
    process_stock_list.start()

    # process_stock_data = CrawlerProcess(
    #     #     settings={
    #     #     "FEEDS": {
    #     #         "items.json": {"format": "json"},
    #     #     },
    #     # }
    # )
    # process_stock_data.crawl(stock_data_spider.StockDataSpider)
    # process_stock_data.start()


if __name__ == "__main__":
    main()
