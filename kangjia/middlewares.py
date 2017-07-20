# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64

from scrapy import signals
import random
import linecache
import logging
import requests


class KangjiaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgent(object):
    """
    自定义的用户代理类
    """
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        # print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class ProxyMiddleware(object):
    """
    自定义的proxy代理类
    """

    def process_request(self, request, spider):
        proxy_url = 'http://112.74.163.187:23128/__static__/proxies.txt'
        proxy_requests = requests.get(proxy_url)
        proxy_list = proxy_requests.content.split('\n')

        proxy_entire = random.choice(proxy_list)

        user_pass = proxy_entire.split('@')[0]
        proxy = proxy_entire.split('@')[-1]
        encoded_user_pass = base64.encodestring(user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

        logging.info("**************ProxyMiddleware have pass************" + proxy)
        request.meta['proxy'] = "http://{proxy}".format(proxy=proxy)

        # if proxy['user_pass'] is not None:
        #     request.meta['proxy'] = "http://%s" % proxy['ip_port']
        #     encoded_user_pass = base64.encodestring(proxy['user_pass'])
        #     request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        #     print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        # else:
        #     print "**************ProxyMiddleware no pass************" + proxy['ip_port']
        #     request.meta['proxy'] = "http://%s" % proxy['ip_port']
