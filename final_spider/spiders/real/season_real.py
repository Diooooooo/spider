# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from final_spider.items import SeasonItem, SeasonRealItem


class SeasonTypeDemoSpider(scrapy.Spider):
    name = 'season_real'
    allowed_domains = ['500.com']
    start_urls = ['http://liangqiujiang.com:8080/api/internal/getOddsSeason?manager=12345qwert']

    def parse(self, response):
        jsonInfo = json.loads(response.body.decode())
        for j in jsonInfo['datalist']:
            yield Request('http://live.500.com/detail.php?fid=%s' % j['season_fid'], self.parse_item_info, dont_filter=True)

    def parse_item_info(self, response):
        tds = response.xpath('//div[@class="t1"]/table/tr/td')
        if tds:
            source = tds[2].xpath('span/text()').extract_first()
            season = SeasonRealItem()
            # season['league_name'] = response.xpath('//div[@class="h"]/a/text()').extract_first().split(' ')[-1:][0].split('第')[:1][0]
            # season['type_name'] = ''
            # season['sub_type_name'] = ''
            # season['game_week'] = response.xpath('//div[@class="h"]/a/text()').extract_first().split(' ')[-1:][0].split('第')[1:][0][:-1]
            season['start_time'] = response.xpath('//div[@class="h"]/a/text()').extract_first().split(' ')[:1][0] + ' ' + response.xpath('//div[@class="h"]/a/text()').extract_first().split(' ')[1:2][0]
            season['team_a'] = tds[0].xpath('h2/a/text()').extract_first()
            season['team_b'] = tds[4].xpath('h2/a/text()').extract_first()
            season['score_a'] = str.strip(source.split('-')[0])
            season['score_b'] = str.strip(source.split('-')[1])
            season['status'] = 3
            season['fid'] = response.url.split('=')[1]
            yield season