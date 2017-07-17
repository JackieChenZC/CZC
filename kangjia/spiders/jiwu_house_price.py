#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2017/7/15 上午11:10
@Author: CZC
@File: jiwu_house_price.py
"""
import sys
import time

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from kangjia.items import JiwuHousePrice

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class JiwuHousePriceSpider(CrawlSpider):
    name = 'jiwu_house_price'
    allowed_domains = ['jiwu.com']
    start_urls = ['http://www.jiwu.com/']

    rules = (
        Rule(LinkExtractor(allow=("\w+\.jiwu\.com/fangjia/$",), deny=('www\.jiwu',)), callback='parse_item',
             follow=True),
    )

    custom_settings = {
        'MONGODB_COLLECTION': name,
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

    def parse_item(self, response):
        self.logger.info('当前正在抓取的内容页是：{url}'.format(url=response.url))

        region_list = Selector(response).xpath("//a/@id/parent::*/text()")
        self.logger.info('当前行政市的片区数量为{0}'.format(len(region_list) - 1))

        for region in region_list:
            region = region.extract()
            region_items = ItemLoader(JiwuHousePrice(), response=response)
            region_items.add_xpath("province", "*", re="province=(.*?);")
            # items.add_xpath("province", "//meta[4]/@content", re="province=(.*?);")
            region_items.add_xpath("city", "*", re="city=(.*?);coord")

            region_items.add_xpath("update_date",
                                   u"//td/a[@title='%s新房房价']/parent::*/following-sibling::*[1]/text()" % region)
            region_items.add_xpath("new_house_price",
                                   u"//td/a[@title='%s新房房价']/parent::*/following-sibling::*[2]/text()" % region)
            region_items.replace_xpath("update_date",
                                       u"//td/a[@title='%s二手房房价']/parent::*/following-sibling::*[1]/text()" % region)
            region_items.add_xpath("second_house_price",
                                   u"//td/a[@title='%s二手房房价']/parent::*/following-sibling::*[2]/text()" % region)
            city = region_items.get_collected_values("city")[0]
            if not city == region:
                region_items.add_value("region", region)

            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            region_items.add_value("_in_time", current_time)
            region_items.add_value("_utime", current_time)

            region_items.add_value("_record_id", self.name)

            yield region_items.load_item()
