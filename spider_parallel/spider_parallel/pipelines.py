# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo


class SpiderParallelPipeline(object):
	def __init__(self):
		host = '127.0.0.1'
		port = 27017
		db_name = 'xsmile'
		sheet_name = 'bilibili'
		client = pymongo.MongoClient(host=host, port=port)
		db = client[db_name]
		self.post = db[sheet_name]

	def process_item(self, item, spider):
		item['spider'] = spider.name
		data = dict(item)
		self.post.insert(data)

# 	def spider_closed(self, spider):
# 		self.file.close()
#
# class InfoPipeline(object):
# 	def process_item(self, item, spider):
# 		item['spider'] = spider.name