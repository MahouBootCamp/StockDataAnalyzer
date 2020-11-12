import stock_data_spider
import stock_list_spider
import scrapy
import time

from multiprocessing import Process, Queue
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


def f(q, spider):
    try:
        runner = CrawlerRunner()
        # runner = CrawlerRunner(settings={
        #     "CONCURRENT_REQUESTS_PER_DOMAIN": 8,
        #     "CONCURRENT_REQUESTS": 16,
        #     "CONCURRENT_ITEMS": 100,
        #     "AUTOTHROTTLE_TARGET_CONCURRENCY": 100
        # })
        deferred = runner.crawl(spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


def run_spider(spider):
    q = Queue()
    p = Process(target=f, args=(q, spider))
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result


def main():
    """
    主函数\n
    先获取股票列表，再查询各股票的详细数据\n
    """
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    print("启动股票爬虫...")
    print("爬取股票列表...")

    strat_time = time.time()
    run_spider(stock_list_spider.StockListSpider)
    end_time = time.time()
    print(f'爬取股票列表消耗 {end_time-strat_time} s')

    print("爬取股票详细信息...")

    strat_time = time.time()
    run_spider(stock_data_spider.StockDataSpider)
    end_time = time.time()
    print(f'爬取股票信息消耗 {end_time-strat_time} s')


if __name__ == "__main__":
    main()
