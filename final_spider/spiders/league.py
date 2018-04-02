# -*- coding: utf-8 -*-
import scrapy

from final_spider.items import LeagueItem


class LeagueSpider(scrapy.Spider):
    name = 'league'
    allowed_domains = ['liansai.500.com']
    start_urls = ['http://liansai.500.com/']

    def parse(self, response):
        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[1:]:
            for li in t.xpath('li'):
                country = str.strip(li.xpath('a/span/text()').extract_first())
                for d in li.xpath('div/a'):
                    league = LeagueItem()
                    league['fid'] = str.split(d.xpath('@href').extract_first(), '-')[1][:-1]
                    league['country'] = country
                    league['full_name'] = str.strip(d.xpath('@title').extract_first())
                    league['league'] = str.strip(d.xpath('text()').extract_first())
                    yield league

        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[:1]:
            for li in t.xpath('li'):
                league = LeagueItem()
                league['league'] = str.strip(li.xpath('a/span/text()').extract_first())
                league['full_name'] = str.strip(li.xpath('a/span/text()').extract_first())
                league['fid'] = str.split(li.xpath('a/@href').extract_first(), '-')[1][:-1]
                league['country'] = '0'
                yield league

        for t in response.xpath('//table[@class="lrace_bei"]/tr'):
            for d in t.xpath('td'):
                league = LeagueItem()
                league['league'] = str.strip(d.xpath('a/text()').extract_first())
                league['full_name'] = str.strip(d.xpath('a/text()').extract_first())
                league['fid'] = str.split(d.xpath('a/@href').extract_first(), '-')[1][:-1]
                league['country'] = '0'
                yield league
