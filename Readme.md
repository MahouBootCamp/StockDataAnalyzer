# 股票信息分析

该程序爬取股市信息并对股票数据进行分析。

**使用方法**：`python.exe main.py`即可（更多命令行参数将在后续开发中引入）。

## 依赖

- `Scrapy`：https://scrapy.org/

## 爬虫

使用Scrapy爬虫爬取股票相关数据：

- `stock_list_spider.py`通过新浪API爬取股票列表。
- `stock_data_spider.py`通过腾讯API爬取各股票数据（开发中）。

## 数据分析

（开发中）

## TODOs

- 爬取各股票数据部分功能开发。
- 数据分析部分开发。
- 加入更多的命令行参数供用户选择。

### ISSUEs

## 参考资料

- 命令行选项：https://docs.python.org/3/library/optparse.html#module-optparse
- 通过脚本语句启动Scrapy爬虫：https://docs.scrapy.org/en/latest/topics/practices.html
- 股票接口：https://blog.csdn.net/luanpeng825485697/article/details/78442062