# spider-redis
分布式爬虫抓取 bilibili 视频评论


实属课程需要，不然早就放弃在半路了。维持了断续半个多月的 bug 调试，突然就实现了。很是欣慰。网上关于分布式爬虫的都是一些介绍，实战的不多并且都很相似，说的云来雾去的，只是项目的流程。可能是项目一路顺风，而我 bug 不断。也好 记录下来供大家参考。

关于 scrapy-redis 环境配置 以及框架流程就不进行叙述了。网上也是一大堆的内容。

主要内容有：

1. 如何去写一个分布式爬虫

首先创建一个普通的爬虫，在保证此爬虫能正常运行的基础上进行修改，然后成为分布式爬虫。我的项目是在linux上 redis 数据库存储分配 requests，我写的是 bilibili 评论抓取，项目路径如下：



a. 将 spiders --> bilibili.py 继承类 由 scrapy.Spider 改为 RedisSpider 。

注释掉： "allowed_domains"　　"start_urls" 
添加： redis_key = 'bilibili:start_urls'
b. setting.py 修改

redis 数据库连接参数
REDIS_HOST = '远程 ip'  # windows setting
REDIS_HOST = 'localhost' # linux setting
REDIS_PORT = 6379
REDIS_PARAMS = {
   'password': '123456' # redis 数据库设置密码情况下进行设置
}

指定使用 scrapy-redis 的调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

指定使用 scrapy-redis 的去重机制
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

指定排序爬取地址时的队列
使用先进先出（FIFO）排序
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

设置断点续传
SCHEDULER_PERSIST = False

DOWNLOADER_MIDDLEWARES = {   
　　'spider_parallel.middlewares.SpiderParallelDownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
   'spider_parallel.pipelines.SpiderParallelPipeline': 300,
   'scrapy_redis.pipelines.RedisPipeline': 400
}
2. 运行爬虫的顺序《此坑最深》

a. 先进入 linux 中 redis 数据库

redis-cli
auth 123456
b. 服务器端运行spider：

scrapy crawl bilibili
这时看到程序一直在等待 redis 中插入 start_url

c. redis 命令行中执行：

lpush bilibili:start_urls https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=329437&sort=2
此连接即评论包的地址，oid 为视频 av 号。你问我怎么知道的这个地址？？？ 爬虫基础在看看吧。（网页 F12 加载的内容中查找）

d. windows 中运行 spider：

scrapy crawl bilibili
顺序不对其中一个会一直处于等待监听的状态。还有就是我想让 两个spiders-->bilibili 中的 name 值不同，以此区分不同的评论是哪个爬虫抓取的。不行，一定要相同。我的区分就是服务器端爬虫存储在服务器端的mongodb数据库中，windows中爬虫就存储在windows中的mongodb数据库中。存储在同一个数据库中也是可以的。区分时记录爬虫类，写 __init__ () 函数继承父类等内容。

没问题就可以看到两个爬虫在共同抓取执行了。

项目已上传至 git 。

原创不易，尊重版权。转载请注明出处：http://www.cnblogs.com/xsmile/

 
