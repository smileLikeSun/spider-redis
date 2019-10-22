# -*- coding: utf-8 -*-
import scrapy
import time
import json
import math
from spider_parallel.items import SpiderParallelItem
from scrapy_redis.spiders import RedisSpider


class BilibiliSpider(RedisSpider):
    name = 'bilibili'
    # name = 'blbl'
    # allowed_domains = ['bilibili.com']
    # start_urls = ['https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=67456873&sort=2']

    redis_key = 'bilibili:start_urls'
    url = 'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid=329437&sort=2'


    def parse(self, response):
        content = response.text
        dict_content = json.loads(content)
        num_reply = dict_content['data']['page']['count']
        page_size = dict_content['data']['page']['size']
        totle_pages = math.ceil(num_reply / page_size) + 1
        for i in range(1, totle_pages):
            url = self.url.format(i)
            yield scrapy.Request(url=url, callback=self.get_content)

    def get_content(self, response):
        content = response.text
        dict_content = json.loads(content)
        item = SpiderParallelItem()
        # 每页回复数
        num_reply = len(dict_content['data']['replies'])
        for i in range(num_reply):
            item['uname'] = dict_content['data']['replies'][i]['member']['uname']
            item['message'] = dict_content['data']['replies'][i]['content']['message']
            ctime = dict_content['data']['replies'][i]['ctime']
            ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))
            item['ctime'] = ctime
            yield item
