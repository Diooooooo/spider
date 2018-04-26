# -*- coding: utf-8 -*-
import datetime
import json
import urllib

import scrapy
from bs4 import BeautifulSoup

from final_spider.items import SeasonRealItem


# ****************************************
#       处理比分，赛时，状态
# ****************************************

class SeasonTypeDemoSpider(scrapy.Spider):
    name = 'season_status'
    allowed_domains = ['500.com']
    start_urls = ['http://live.500.com/2h1.php']

    def parse(self, response):
        jsonInfo = json.loads(str(BeautifulSoup(urllib.request.urlopen(urllib.request.Request(
            'https://www.liangqiujiang.com/api/internal/getPlayingSeason?manager=12345qwert')).read(),
                                                "html.parser")))
        txt = json.loads(str(BeautifulSoup(
            urllib.request.urlopen('http://live.500.com/static/info/bifen/xml/livedata/all/Full.txt').read(),
            "html.parser")))
        jsoninfos = []
        for j in jsonInfo['datalist']:
            jsoninfos.append('a' + str(j['season_fid']))
        for tr in response.xpath('//table[@class="bf_tablelist01"]/tbody/tr'):
            if tr.xpath('@id').extract_first() in jsoninfos:
                season = SeasonRealItem()
                time = tr.xpath('td[4]/text()').extract_first().split(' ')
                status_name = tr.xpath('@status').extract_first()
                if '2' == status_name:
                    status = 7
                    playing = 45
                elif '0' == status_name:
                    status = 1
                    playing = 0
                elif '1' == status_name:
                    for s in txt:
                        if s[0] == int(tr.xpath('@id').extract_first()[1:]):
                            status = 3
                            playing = int((datetime.datetime.now() -
                                           datetime.datetime.strptime(s[4], '%Y-%m-%d %H:%M:%S')).seconds / 60)
                            break
                elif '3' == status_name:
                    for s in txt:
                        if s[0] == int(tr.xpath('@id').extract_first()[1:]):
                            status = 3
                            playing = int((datetime.datetime.now() -
                                           datetime.datetime.strptime(s[4], '%Y-%m-%d %H:%M:%S')).seconds / 60) + 45
                            break
                elif '4' == status_name:
                    status = 4
                    playing = 90

                sa = tr.xpath('td[7]/div/a[1]/text()').extract_first()
                sb = tr.xpath('td[7]/div/a[3]/text()').extract_first()
                if not sa:
                    sa = 0
                if not sb:
                    sb = 0
                season['start_time'] = str(datetime.date.today().year) + '-' + time[0] + ' ' + time[1] + ':00'
                season['team_a'] = tr.xpath('td[6]/a/text()').extract_first()
                season['team_b'] = tr.xpath('td[8]/a/text()').extract_first()
                season['score_a'] = sa
                season['score_b'] = sb
                season['status'] = status
                season['fid'] = tr.xpath('@id').extract_first()[1:]
                season['playing'] = playing
                yield season
