# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from random import choice

from scrapy import signals
from scrapy.exceptions import NotConfigured
from final_spider.settings import USER_AGENT_CHOICES


class FinalSpiderSpiderMiddleware(object):
    """Rotate user-age for each request
        """

    def __init__(self, user_agents):
        self.enabled = False
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        # s = cls()
        # crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        # return s
        print('init user agents')
        user_agents = choice(USER_AGENT_CHOICES)

        if not user_agents:
            raise NotConfigured("USER_AGENT_CHOICES not set or empty")

        o = cls(user_agents)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

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
        self.enabled = getattr(spider, 'rotate_user_agent', self.enabled)

    def process_request(self, request, spider):
        userAgents = choice(self.user_agents)
        request.headers['user-agent'] = userAgents
        print('working user agents : ' + self.user_agents)


class ProxyMiddleware(object):

    def get_random_proxy(self):
        while 1:
            with open('/root/test_spider/final_spider/proxy') as f:
                proxies = f.readlines()
            if proxies:
                break
        proxy = choice(proxies).strip()
        return proxy

    def process_request(self, request, spider):
        proxy = 'http://' + self.get_random_proxy()
        request.meta['proxy'] = proxy
        print('working proxy : ' + proxy)

    def proxcess_response(self, request, response, spider):
        print('working status : ' + response.status)
        if response.stauts != 200:
            proxy = self.get_random_proxy()
            request.meta['proxy'] = proxy
            return request
        return response
