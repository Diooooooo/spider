# -*- coding: utf-8 -*-

import scrapy


class SportteryResultSpider(scrapy.Spider):
    name = 'sporttery_result'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://info.sporttery.cn/football/match_result.php']

    def parse(self, response):
        pass
