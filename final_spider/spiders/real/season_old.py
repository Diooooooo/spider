# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from final_spider.items import SeasonOldItem


# ******************************
#           DELETE
# ******************************

class SeasonTypeDemoSpider(scrapy.Spider):
    name = 'season_old'
    allowed_domains = ['500.com']
    start_urls = ['http://www.liangqiujiang.com/api/internal/getOldSeason?manager=12345qwert']

    def parse(self, response):
        jsonInfo = json.loads(response.body.decode())
        for j in jsonInfo['datalist']:
            yield Request('http://live.500.com/detail.php?fid=%s' % j['season_fid'], self.parse_item_info, dont_filter=True)

    def parse_item_info(self, response):
        tds = response.xpath('//div[@class="t1"]/table/tr/td')
        if tds:
            source = tds[2].xpath('span/text()').extract_first()
            season = SeasonOldItem()
            season['score_a'] = str.strip(source.split('-')[0])
            season['score_b'] = str.strip(source.split('-')[1])
            season['status'] = 4
            season['fid'] = response.url.split('=')[1]
            yield season