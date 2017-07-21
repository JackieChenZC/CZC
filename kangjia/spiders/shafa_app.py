# -*- coding: utf-8 -*-
from kangjia.items import ShafaItem
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
import time
import hashlib


class ShafaSpider(CrawlSpider):
    name = 'shafa_app'
    allowed_domains = ["app.shafa.com"]
    start_urls = ["http://app.shafa.com/archives/1.html"]
    rules = (
        Rule(LinkExtractor(allow=("/apk/\w+\.html", )), callback='parse_item'),
    )

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': allowed_domains[0],
        # 'Referer': start_urls[0],
        'Upgrade-Insecure-Requests': '1',
        # '': '',
    }
    custom_settings = {
        'MONGODB_COLLECTION': name,
        'DEFAULT_REQUEST_HEADERS': headers,
    }

    # def parse_item(self, response):
    #     self.logger.info('当前正在抓取的列表页是：%s' % response.url)
    #     apps = Selector(response).xpath("//div[@class='container']/div[@class='row'][3]/div[@class='col-sm-6']/a/@href")
    #     # for a in apps:
    #     #     print a.extract()
    #     #     yield Request(url=a.extract(), callback=self.parse_ear_app)
    #     yield Request(url=apps[3].extract(), callback=self.parse_ear_app)

    def parse_item(self, response):
        self.logger.info('当前正在抓取的内容页是：%s' % response.url)

        sel = Selector(response)
        items = ShafaItem()
        items['app_name'] = sel.xpath("//div[@class='view-header-title']/h1/text()").extract()
        items['cat'] = sel.xpath("//ol[@class='breadcrumb']/li[4]/a/text()|//ol[@class='breadcrumb']/li[5]/a/text()|//ol[@class='breadcrumb']/li[6]/a/text()").extract()
        items['comments'] = sel.xpath("//section[@class='app-view-section app-view-comment']/h2/small/a/text()").extract()
        items['control_type'] = sel.xpath("//div[@class='view-header-middle']/div[@class='view-header-rating']/span[3]/text()").extract()
        items['download_link'] = sel.xpath('//*[@id="downloadModal"]/div/div/div[3]/div/a[2]/@data-url').extract()
        items['downloads'] = sel.xpath(u"//ul[@class='view-info-list list-unstyled']/li/div[contains(text(),'下载')]/../span/text()").extract()
        items['introduction'] = sel.xpath("//section[@class='app-view-desc app-view-section']/p[1]/text()").extract()
        items['language'] = sel.xpath(u"//ul[@class='view-info-list list-unstyled']/li/div[contains(text(),'语言')]/../span/text()").extract()
        items['package_name'] = sel.re("'send', 'event', 'Downloads', '\d+', '(.+)'\);\"")
        items['resolution'] = sel.xpath("//div[@class='view-header-middle']/div[@class='view-header-rating']/span[5]/text()").extract()
        items['score'] = sel.xpath('//meta[@itemprop="ratingValue"]/@content').extract()
        items['system'] = sel.xpath(u"//ul[@class='view-info-list list-unstyled']/li/div[contains(text(),'系统')]/../span/text()").extract()
        items['tag'] = sel.xpath("//div[@class='view-header-tags']/ul[@class='list-inline']/li/span[@class='btn btn-sm btn-default']/text()").extract()
        items['type'] = sel.xpath(u"//ul[@class='view-info-list list-unstyled']/li/div[contains(text(),'类型')]/../a/span/text()").extract()
        items['update'] = sel.xpath(u"//ul[@class='view-info-list list-unstyled']/li/div[contains(text(),'更新')]/../span/text()").extract()
        items['version'] = sel.xpath(u"//ul[@class='view-info-list list-unstyled']/li/div[contains(text(),'版本')]/../span/text()").extract()
        items['picture'] = sel.xpath("//div[@class='view-header-left']/img[@class='view-header-icon']/@src").extract()
        items['package_size'] = sel.xpath(u"//ul[@class='view-info-list list-unstyled']/li/div[contains(text(),'大小')]/../span/text()").extract()
        items['mark_distribution'] = sel.xpath("//div[@class='reviews-element']/div[@class='review-chart']//span[@class='review-chart-percentage']/text()").extract()
        items['mark_count'] = sel.re(u"（(\d+) 个评分）")

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        items['_in_time'] = [current_time]
        items['_utime'] = [current_time]

        m = hashlib.md5()
        m.update('{0}{1}'.format(self.name, items['app_name']))
        record_id = m.hexdigest()
        items['_record_id'] = [record_id]
        yield items
        # return items
