# -*- coding: utf-8 -*-
import json

import scrapy


class BifenSpider(scrapy.Spider):
    name = 'ip_filefab'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.baidu.com']

    def parse(self, response):
        print(response.body)

