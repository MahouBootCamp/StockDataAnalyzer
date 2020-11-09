# 股票信息分析

该程序爬取股市信息并对股票数据进行分析。

**使用方法**：`python.exe main.py`即可（更多命令行参数将在后续开发中引入）。

**⚠️注意事项⚠️**：如果将本项目代码复制入Jupyter NoteBook执行，一定要在每次执行前重置运行时，以避免加载过多twisted库造成的性能负担。（如果需要DEBUG级别的Scrapy Log信息，可以再main.py中配置。）

## 环境与依赖

### 开发环境

开发使用`Anaconda 2020.7`版本（集成`Python 3.8`）。

### 第三方包

- `Scrapy`：https://scrapy.org/

## 爬虫

使用Scrapy爬虫爬取股票相关数据：

- `stock_list_spider.py`通过新浪API爬取股票列表。
- `stock_data_spider.py`通过腾讯API爬取各股票数据（开发中）。

## 数据分析

（开发中）

## TODOs

- 数据分析部分开发。
- 加入更多的命令行参数供用户选择。

### ISSUEs

#### Twisted无法重新启动

使用CrawlProcess调用start()函数将调用一个名为twisted的库。该库仅能在运行时启动一次，无法重启。我们的代码试图运行两个CrawlProcess，将会引发异常`twisted.internet.error.ReactorNotRestartable`。解决方案见参考资料2、3。

## 参考资料

1. 命令行选项：https://docs.python.org/3/library/optparse.html#module-optparse
2. 通过脚本语句启动Scrapy爬虫：https://docs.scrapy.org/en/latest/topics/practices.html
3. 避免脚本只能启动一个CrawlProcess的方法：https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable/43661172
4. 股票接口：https://blog.csdn.net/luanpeng825485697/article/details/78442062