#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2017/7/17 下午6:23
@Author: CZC
@File: weather_kj.py
@run:docker run -p 8050:8050 scrapinghub/splash
"""
import logging
import re
import time

from scrapy.loader import ItemLoader
from scrapy.spiders import SitemapSpider, Request

from kangjia.items import WeatherItem

logger = logging.getLogger(__name__)


class WeatherSpider(SitemapSpider):
    name = 'weather_kj'
    allowed_domains = ['tianqi.2345.com']
    sitemap_urls = ['http://tianqi.2345.com/baidu/today.xml', 'http://tianqi.2345.com/baidu/tomorrow.xml']
    sitemap_rules = [
        ('/today-\d+', 'parse_today'),
        ('/tomorrow-\d+', 'parse_tomorrow')
    ]

    meta = {
        'splash': {
            'endpoint': 'render.html',
            'args': {
                'wait': 1,
                'render_all': 1
            }
        }
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Host': 'v.youku.com',
        # 'Referer': start_urls[0],
        'If-Modified-Since': 'Sun, 16 Jul 2017 03:46:39 GMT',
        'If-None-Match': '"11b0a-55467213465c0"',

        'Upgrade-Insecure-Requests': '1',
        # '': '',
    }
    custom_settings = {
        'MONGODB_COLLECTION': name,
        'DEFAULT_REQUEST_HEADERS': headers,
    }
    splash_url = "http://localhost:8050/render.html"

    # def make_requests_from_url(self, url):
    #     url = self.splash_url + "?url=" + url
    #     body = json.dumps({"url": url, "wait": 5, 'images': 0, 'allowed_content_types': 'text/html; charset=utf-8'})
    #     return Request(url, body=body, headers=self.headers, dont_filter=True)
    #
    # def start_requests(self):
    #     for url in self.sitemap_urls:
    #         yield Request(url, self._parse_sitemap, meta=self.meta)

    # 复写SitemapSpider _parse_sitemap方法，主要是请求部分加上splash参数
    # def _parse_sitemap(self, response):
    #     if response.url.endswith('/robots.txt'):
    #         for url in sitemap_urls_from_robots(response.text, base_url=response.url):
    #             # url = self.splash_url + "?url=" + url
    #             yield SplashRequest(url, callback=self._parse_sitemap, args=self.meta, dont_filter=True)
    #     else:
    #         body = self._get_sitemap_body(response)
    #         if body is None:
    #             logger.warning("Ignoring invalid sitemap: %(response)s",
    #                            {'response': response}, extra={'spider': self})
    #             return
    #
    #         s = Sitemap(body)
    #         if s.type == 'sitemapindex':
    #             for loc in iterloc(s, self.sitemap_alternate_links):
    #                 if any(x.search(loc) for x in self._follow):
    #                     # loc = self.splash_url + "?url=" + loc
    #                     yield SplashRequest(loc, callback=self._parse_sitemap, args=self.meta, dont_filter=True)
    #         elif s.type == 'urlset':
    #             for loc in iterloc(s):
    #                 for r, c in self._cbs:
    #                     if r.search(loc):
    #                         r = SplashRequest(loc, callback=c, args=self.meta, dont_filter=True)
    #                         print r.headers
    #                         yield r
    #                         # loc = self.splash_url + "?url=" + loc
    #                         break

    def parse_today(self, response):
        self.logger.info('当前正在抓取的天气页面是：{url}'.format(url=response.url))

        today_items = ItemLoader(WeatherItem(), response=response)
        today_items.add_xpath("province", "//div[@class='path_lf']/a[2]/text()")
        today_items.add_xpath("date", "//span[@class='date']/text()")
        today_items.add_xpath("high_temp", "//dl[@class='day']//span[@class='temperature']/text()")
        today_items.add_xpath("low_temp", "//dl[@class='night']//span[@class='temperature']/text()")
        today_items.add_xpath("weather",
                              "//dl[@class='day']//span[@class='phrase']/text()|//dl[@class='night']//span[@class='phrase']/text()")
        today_items.add_xpath("wind",
                              "//ul[@class='parameter']/li[3]/i/text()|//ul[@class='parameter']/li[4]/i/text()")

        air_url_id = re.findall('today-(\d+)', response.url)[0]
        # air_url = Selector(response).xpath("//ul[@class='parameter']/li[1]/a/@href").extract()
        if air_url_id:
            air_url = 'http://tianqi.2345.com/air-{air_url_id}.htm'.format(air_url_id=air_url_id)
            yield Request(url=air_url, meta={'today_items': today_items}, callback=self.today_air)

    def today_air(self, response):
        self.logger.info('当前正在抓取的空气质量页面是：{url}'.format(url=response.url))
        today_items = response.meta['today_items']
        air_items = ItemLoader(WeatherItem(), response=response)
        air_items.add_value("province", today_items.get_collected_values("province"))
        air_items.add_value("date", today_items.get_collected_values("date"))
        air_items.add_value("high_temp", today_items.get_collected_values("high_temp"))
        air_items.add_value("low_temp", today_items.get_collected_values("low_temp"))
        air_items.add_value("wind", today_items.get_collected_values("wind"))

        air_items.add_xpath("region", "//*[@id='lastBread']/text()")
        air_items.add_xpath("city", "//div[@class='path_lf']/a[2]/text()")
        air_items.add_xpath("quality", "//dd[1]/div[@class='td td2']/i/text()")
        air_items.add_xpath("aqi", "//dd[1]/div[@class='td td3 tc']/span/text()")

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        air_items.add_value("_in_time", current_time)
        air_items.add_value("_utime", current_time)
        air_items.add_value("_record_id", '{0}{1}'.format(self.name, air_items.get_collected_values('region')))
        yield air_items.load_item()

    def parse_tomorrow(self, response):
        self.logger.info('当前正在抓取的天气页面是：{url}'.format(url=response.url))
        tomorrow_items = ItemLoader(WeatherItem(), response=response)
        tomorrow_items.add_xpath("province", "//div[@class='path_lf']/a[2]/text()")
        tomorrow_items.add_xpath("date", "//span[@class='date']/text()")
        tomorrow_items.add_xpath("high_temp", "//dl[@class='day']//span[@class='temperature']/text()")
        tomorrow_items.add_xpath("low_temp", "//dl[@class='night']//span[@class='temperature']/text()")
        tomorrow_items.add_xpath("weather",
                                 "//dl[@class='day']//span[@class='phrase']/text()|//dl[@class='night']//span[@class='phrase']/text()")
        tomorrow_items.add_xpath("wind", "//ul[@class='parameter line6-parameter']/li[2]/i/text()")

        air_url_id = re.findall('tomorrow-(\d+)', response.url)[0]
        # air_url = Selector(response).xpath("//ul[@class='parameter']/li[1]/a/@href").extract()
        if air_url_id:
            air_url = 'http://tianqi.2345.com/airtomorrow-{air_url_id}.htm'.format(air_url_id=air_url_id)
            yield Request(url=air_url, meta={'tomorrow_items': tomorrow_items}, callback=self.tomorrow_air)

    def tomorrow_air(self, response):
        self.logger.info('当前正在抓取的空气质量页面是：{url}'.format(url=response.url))
        tomorrow_items = response.meta['tomorrow_items']
        tomo_air_items = ItemLoader(WeatherItem(), response=response)
        tomo_air_items.add_value("province", tomorrow_items.get_collected_values("province"))
        tomo_air_items.add_value("date", tomorrow_items.get_collected_values("date"))
        tomo_air_items.add_value("high_temp", tomorrow_items.get_collected_values("high_temp"))
        tomo_air_items.add_value("low_temp", tomorrow_items.get_collected_values("low_temp"))
        tomo_air_items.add_value("wind", tomorrow_items.get_collected_values("wind"))

        tomo_air_items.add_xpath("region", "//*[@id='lastBread']/text()")
        tomo_air_items.add_xpath("city", "//div[@class='path_lf']/a[2]/text()")
        tomo_air_items.add_xpath("quality", "//dd[2]/div[@class='td td2']/i/text()")
        tomo_air_items.add_xpath("aqi", "//dd[2]/div[@class='td td3 tc']/span/text()")

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        tomo_air_items.add_value("_in_time", current_time)
        tomo_air_items.add_value("_utime", current_time)
        tomo_air_items.add_value("_record_id", '{0}{1}'.format(self.name, tomo_air_items.get_collected_values('region')))
        yield tomo_air_items.load_item()
