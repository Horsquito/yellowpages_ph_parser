# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class YellowpagesPhParserPipeline(object):
    def process_item(self, item, spider):
        self.conn = pymongo.MongoClient (
            'localhost',
            27017,
            maxPoolSize = None,
            connect = False
        )
        self.db = self.conn['yellowpages']
        self.collection = self.db['philippines']
        self.collection.insert(dict(item))
        return item
