# -*- coding: utf-8 -*-
import datetime
import json
import urllib

import scrapy
from bs4 import BeautifulSoup

from final_spider.items import SeasonRealItem


class SeasonTypeDemoSpider(scrapy.Spider):
    name = 'season_status'
    allowed_domains = ['500.com']
    start_urls = ['http://live.500.com/2h1.php']

    def parse(self, response):
        jsonInfo = json.loads(str(BeautifulSoup(urllib.request.urlopen(urllib.request.
        Request('http://api.liangqiujiang.com:8080/api/internal/getOldSeason?manager=12345qwert')).read(), "html.parser")))
        jsoninfos = []
        for j in jsonInfo['datalist']:
            jsoninfos.append('a'+j['season_fid'])
        for tr in response.xpath('//table[@class="bf_tablelist01"]/tbody/tr'):
            if tr.xpath('@id') in jsoninfos:
                season = SeasonRealItem()
                time = tr.xpath('td[4]/text()').extract_first().split(' ')
                status_name = tr.xpath('td[5]/text()').extract_first()[:-1]
                if '中' == status_name:
                    status = 7
                elif int(status_name):
                    status = 3
                else:
                    status = 1
                season['start_time'] = str(datetime.date.today().year) + '-' + time[0] + ' ' + time[1] + ':00'
                season['team_a'] = tr.xpath('td[6]/a/text()').extract_first()
                season['team_b'] = tr.xpath('td[8]/a/text()').extract_first()
                season['score_a'] = tr.xpath('td[7]/div/a[1]/text()').extract_first()
                season['score_b'] = tr.xpath('td[7]/div/a[3]/text()').extract_first()
                season['status'] = status
                season['fid'] = tr.xpath('@id').extract_first()[1:]
                yield season