# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderParallelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 用户昵称
    uname = scrapy.Field()

    # 评论内容
    message = scrapy.Field()

    # 发表时间
    ctime = scrapy.Field()

    # 爬虫名
    spider = scrapy.Field()
