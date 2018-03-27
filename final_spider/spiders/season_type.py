# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request

from final_spider.items import SeasonTypeItem


class SeasonTypeSpider(scrapy.Spider):
    name = 'season_type'
    allowed_domains = ['500.com']
    start_urls = ['http://liansai.500.com/']

    def parse(self, response):
        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[1:]:
            for li in t.xpath('li'):
                for d in li.xpath('div/a'):
                    yield Request(response.urljoin(d.xpath('@href').extract_first()), self.parse_info)

        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[:1]:
            for li in t.xpath('li'):
                yield Request(response.urljoin(li.xpath('a/@href').extract_first()), self.parse_info)

    def parse_info(self, response):
        for t in response.xpath('//ul[@class="ldrop_list"]/li')[:4]:
            yield Request(response.urljoin(t.xpath('a/@href').extract_first()), self.parse_item_info)

    def parse_item_info(self, response):
        yield Request(response.urljoin(response.xpath('//div[@class="lcol_tit_r"][1]/a/@href').extract_first()),
                      self.parse_detail_info)

    def parse_detail_info(self, response):
        for r in response.xpath('//div[@class="ltab_hd lmb3 clearfix"]/a'):
            yield Request(response.urljoin(r.xpath('@href').extract_first()), self.parse_line_info)
        for r in response.xpath('//div[@class="ltab_hd lmb2 clearfix"]/a'):
            yield Request(response.urljoin(r.xpath('@href').extract_first()), self.parse_line_info)

    def parse_line_info(self, response):
        # 遍历选项卡（联赛赛程，联赛赛制）
        for r in response.xpath('//div[@class="ltab_hd lmb2 clearfix"]/a'):
            if r.xpath('@href').extract_first() != 'javascript:void(0);':
                type = SeasonTypeItem()
                type['type'] = str.strip(r.xpath('text()').extract_first())
                yield type

        # 遍历选项卡（资格赛，附加赛，圈赛）
        for r in response.xpath('//div[@class="ltab_hd lmb3 clearfix"]/a'):
            if r.xpath('@href').extract_first() != 'javascript:void(0);':
                type = SeasonTypeItem()
                type['type'] = str.strip(r.xpath('text()').extract_first())
                yield type

