#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2017/7/18 下午4:46
@Author: CZC
@File: iqiyi_tvplay.py
"""
import sys
import time

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule, Request

from kangjia.items import IqiyiTVplayItem

reload(sys)
sys.setdefaultencoding('utf8')


class TudouDocumentarySpider(CrawlSpider):
    name = 'iqiyi_tvplay'
    allowed_domains = ['iqiyi.com']
    start_urls = ['http://www.iqiyi.com/lib/dianshiju/,,_11_1.html']

    rules = (
        Rule(LinkExtractor(allow=("/lib/m_\d+\.html",)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=("/category/c_84.html",)), callback='parse_item'),

    )

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

    def parse_item(self, response):
        self.logger.info('当前正在抓取的内容页是：{url}'.format(url=response.url))
        items = ItemLoader(IqiyiTVplayItem(), response=response)
        items.add_xpath("title", "//h1[@class='main_title']/a/text()")
        items.add_xpath("score", "//span[@class='score_font']")
        items.add_xpath("votetop", "//span[@id='widget-voteup']/text()")
        items.add_xpath("votedown", "//span[@id='widget-votedown']/text()")
        items.add_xpath("new_title", "//em[@rseat='alias']/text()")
        items.add_xpath("status", u"//em[@rseat='集数']/text()")
        items.add_xpath("pub_year", u"//em[@rseat='首播时间']/text()")
        items.add_xpath("update_time", u"//em[@rseat='updateInfo']/text()")
        items.add_xpath("type", "//div[@class='look_point']/a/text()")
        items.add_xpath("area", u"//em[@rseat='地区']/a/text()")
        items.add_xpath("director", u"//em[@rseat='导演']/a/text()")
        items.add_xpath("actor", u"//em[@rseat='主演']/a/text()")
        items.add_xpath("summary", "//p[@data-movlbshowmore-ele='whole']/text()")
        items.add_xpath("video_type", "//span[@class='source_detail']//em/text()")
        items.add_value("detail_url", response.url)
        items.add_value("video_id", response.url, re="/lib/(.*?)\.html")

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        items.add_value("_in_time", current_time)
        items.add_value("_utime", current_time)
        items.add_value("_record_id", self.name)
        yield items.load_item()




