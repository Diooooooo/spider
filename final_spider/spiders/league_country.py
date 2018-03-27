# -*- coding: utf-8 -*-
import scrapy

from final_spider.items import CountryItem


class LeagueCountrySpider(scrapy.Spider):
    name = 'league_country'
    allowed_domains = ['liansai.500.com']
    start_urls = ['http://liansai.500.com/']

    def parse(self, response):
        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[1:]:
            for li in t.xpath('li'):
                country = CountryItem()
                country['country'] = str.strip(li.xpath('a/span/text()').extract_first())
                yield country
