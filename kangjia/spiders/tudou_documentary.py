# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.selector import Selector
from kangjia.items import TuDouItem
import time
import hashlib
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class TudouDocumentarySpider(CrawlSpider):
    name = 'tudou_documentary'
    allowed_domains = ['tudou.com', 'v.youku.com', 'list.youku.com']
    start_urls = ['http://www.tudou.com/category/c_84.html']

    rules = (
        Rule(LinkExtractor(allow=("/category/c_84_p_\d+\.html",)), callback='parse_item', follow=True),
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
        self.logger.info('当前正在抓取的列表页是：{url}'.format(url=response.url))
        item_list = Selector(response).xpath(
            "//div[@class='td-col']/div[@class='v-pack--p']/div[@class='v-thumb']/a/@href")
        self.logger.info('******************************{0}'.format(len(item_list)))
        for item in item_list:
            yield Request(url='http:' + item.extract(), headers=self.headers, callback=self.parse_play)

    def parse_play(self, response):
        self.logger.info('当前正在抓取的播放页是：%s' % response.url)
        sel = Selector(response).xpath("//div[@class='base_info']/a[@class='desc-link']/@href")
        for s in sel:
            yield Request(url='http:' + s.extract(), headers=self.headers, callback=self.parse_detail)

    def parse_detail(self, response):
        self.logger.info('当前正在抓取的详情页是：%s' % response.url)

        sel = Selector(response).xpath("//div[@class='p-base']/ul")
        items = TuDouItem()
        items['program'] = Selector(response).xpath("//div[@class='p-thumb']/a/@title").extract()
        items['area'] = sel.xpath("./li[4]/a/text()").extract()
        items['image'] = Selector(response).xpath("//div[@class='p-thumb']/img/@src").extract()

        presenter_0 = sel.xpath("./li[3]/text()").extract()
        if presenter_0:
            presenter = [presenter_0[0].split('：')[1]]
        else:
            presenter = []
        items['presenter'] = presenter

        items['episodes'] = sel.xpath("//li[@class='p-row p-renew']/text()").extract()
        items['tag'] = sel.xpath("./li[5]/a/text()").extract()

        play_cnt_0 = sel.xpath("./li[7]/text()").extract()
        if play_cnt_0:
            play_cnt = [play_cnt_0[0].split('：')[1]]
        else:
            play_cnt = []
        items['play_cnt'] = play_cnt

        comment_cnt_0 = sel.xpath("./li[8]/text()").extract()
        if comment_cnt_0:
            comment_cnt = [comment_cnt_0[0].split('：')[1]]
        else:
            comment_cnt = []
        items['comment_cnt'] = comment_cnt

        voteup_cnt_0 = sel.xpath("./li[9]/text()").extract()
        if voteup_cnt_0:
            voteup_cnt = [voteup_cnt_0[0].split('：')[1]]
        else:
            voteup_cnt = []
        items['voteup_cnt'] = voteup_cnt

        introduction_0 = sel.xpath("./li[@class='p-row p-intro']/span/text()").extract()
        if introduction_0:
            introduction = [introduction_0[0].split('：')[1]]
        else:
            introduction = []
        items['introduction'] = introduction

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        items['_in_time'] = [current_time]
        items['_utime'] = [current_time]

        m = hashlib.md5()
        m.update(self.name + current_time)
        record_id = m.hexdigest()
        items['_record_id'] = [record_id]
        # return items
        yield items
