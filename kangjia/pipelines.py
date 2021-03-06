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
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        db.authenticate(settings['MONGO_USER'], settings['MONGO_PSW'])
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for key, data in item.iteritems():
            item[key] = ','.join(data)
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
