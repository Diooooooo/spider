# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request

from final_spider.items import SeasonSubTypeItem


class SeasonSubTypeSpider(scrapy.Spider):
    name = 'season_sub_type'
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
        # for r in response.xpath('//div[@class="ltab_hd lmb3 clearfix"]/a'):
        #     yield Request(response.urljoin(r.xpath('@href').extract_first()), self.parse_season_history_tab)
        for r in response.xpath('//div[@class="ltab_hd lmb2 clearfix"]/a'):
            yield Request(response.urljoin(r.xpath('@href').extract_first()), self.parse_season_history)

    def parse_season_history(self, response):
        if response.xpath('//ul[@id="match_group"]'):
            pass
        elif response.xpath('//div[@id="season_match_list"]'):
            pass
        else:
            for s in response.xpath('//div[@class="lmb3"]'):
                subType = SeasonSubTypeItem()
                subType['sub_type'] = str.strip(s.xpath('h4/text()').extract_first())
                yield subType

    # def parse_season_history_tab(self, response):
    #     pass
