#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2017/7/18 下午4:22
@Author: CZC
@File: baidu_news_kj.py
"""
import time

from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.spiders import Spider, Request
from kangjia.items import BaiduNewsItem
import logging
logger = logging.getLogger(__name__)


class BaiduNewsSpider(Spider):
    name = 'baidu_news_kj'
    start_urls = ['http://news.baidu.com/n?cmd=4&class=sportnews']

    custom_settings = {
        'MONGODB_COLLECTION': name
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Host': 'v.youku.com',
        # 'Referer': start_urls[0],
        'Upgrade-Insecure-Requests': '1',
        # '': '',
    }

    def parse(self, response):
        sel = Selector(response).xpath("//div[@class='p2']/div")
        for index, s in enumerate(sel):
            items = ItemLoader(BaiduNewsItem(), response=response)
            items.add_xpath("title", "//div[@class='p2']/div[%s]/a/text()" % index)
            items.add_xpath("url", "//div[@class='p2']/div[%s]/a/@href" % index)
            items.add_xpath("publish_time", "//div[@class='p2']/div[%s]/span[@class='c']" % index)

            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            items.add_value("_in_time", current_time)
            items.add_value("_utime", current_time)
            items.add_value("_record_id", self.name)
            yield items.load_item()
