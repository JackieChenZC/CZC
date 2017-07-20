# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging


class KangjiaPipeline(object):
    def __init__(self, mongo_collection):
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_collection=crawler.settings.get('MONGODB_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = self.client[settings['MONGODB_DB']]
        db.authenticate(settings['MONGO_USER'], settings['MONGO_PSW'])
        self.collection = db[self.mongo_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        for key, data in item.iteritems():
            item[key] = ','.join(filter(lambda x: x != u'/', data))
        self.collection.insert(dict(item))
        # valid = True
        # for data in item:
        #     if not data:
        #         valid = False
        #         raise DropItem('Missing{0}!'.format(data))
        # if valid:
        #     self.collection.insert(dict(item))
        #     log.msg('question added to mongodb database!',
        #             level=log.DEBUG, spider=spider)
        return item
