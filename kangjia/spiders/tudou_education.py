# -*- coding: utf-8 -*-
import sys
import time

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule, Request

from kangjia.items import TuDouItem

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class TudouEducationSpider(CrawlSpider):
    name = 'tudou_education'
    allowed_domains = ['edu.tudou.com', 'v.youku.com', 'list.youku.com']
    start_urls = ['http://edu.tudou.com/category/c_87.html']

    rules = (
        Rule(LinkExtractor(allow=("/category/c_87_p_\d+\.html",)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=("/category/c_87.html",)), callback='parse_item'),

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
        self.logger.info('当前正在抓取的列表页是：{url}'.format(url=response.url))
        item_list = Selector(response).xpath(
            "//div[@class='td-col']/div[@class='v-pack--p']/div[@class='v-thumb']/a/@href")
        self.logger.info('当前列表页的数量{0}'.format(len(item_list)))
        for item in item_list:
            yield Request(url='http:' + item.extract(), headers=self.headers, callback=self.parse_play)

    def parse_play(self, response):
        self.logger.info('当前正在抓取的播放页是：%s' % response.url)
        sel = Selector(response).xpath("//div[@class='base_info']/a[@class='desc-link']/@href")
        for s in sel:
            yield Request(url='http:' + s.extract(), headers=self.headers, callback=self.parse_detail)

    def parse_detail(self, response):
        self.logger.info('当前正在抓取的详情页是：%s' % response.url)

        items = ItemLoader(TuDouItem(), response=response)

        items.add_xpath("program", "//div[@class='p-thumb']/a/@title")
        items.add_xpath("program_alias", "//div[@class='p-base']/ul/li[@class='p-alias']/text()")
        items.add_xpath("image", "//div[@class='p-thumb']/img/@src")
        items.add_xpath("presenter", "//div[@class='p-base']/ul/li[3]/a/text()")
        items.add_xpath("episodes", "//li[@class='p-row p-renew']/text()")
        items.add_xpath("tag", "//div[@class='p-base']/ul/li[5]/a/text()")
        items.add_xpath("play_cnt", "//div[@class='p-base']/ul/li[7]/text()")
        items.add_xpath("comment_cnt", "//div[@class='p-base']/ul/li[8]/text()")
        items.add_xpath("voteup_cnt", "//div[@class='p-base']/ul/li[9]/text()")
        items.add_xpath("introduction", "//div[@class='p-base']/ul/li[@class='p-row p-intro']/span/text()")

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        items.add_value("_in_time", current_time)
        items.add_value("_utime", current_time)

        items.add_value("_record_id", self.name)
        # return items
        yield items.load_item()
