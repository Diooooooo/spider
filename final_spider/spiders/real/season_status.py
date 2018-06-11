# -*- coding: utf-8 -*-
import datetime
import json

import requests
import scrapy


# ****************************************
#       处理比分，赛时，状态
# ****************************************
from final_spider.items import SeasonRealItem


class SeasonTypeDemoSpider(scrapy.Spider):
    name = 'season_status'
    allowed_domains = ['500.com']
    start_urls = ['https://live.500.com/2h1.php']

    def parse(self, response):
        jsonInfo = json.loads(requests.get('http://www.liangqiujiang.com/api/internal/getPlayingSeason?manager=12345qwert').text)
        jsoninfos = []
        for j in jsonInfo['datalist']:
            jsoninfos.append('a' + str(j['season_fid']))

        for tr in response.xpath('//table[@class="bf_tablelist01"]/tbody/tr'):
            if tr.xpath('@id').extract_first() in jsoninfos:
                season = SeasonRealItem()
                time = tr.xpath('td[4]/text()').extract_first()
                status_name = tr.xpath('@status').extract_first()
                if '2' == status_name:
                    status = 7
                elif '0' == status_name:
                    status = 1
                elif '1' == status_name:
                    status = 3
                elif '3' == status_name:
                    status = 3
                elif '4' == status_name:
                    status = 4

                sa = tr.xpath('td[7]/div/a[1]/text()').extract_first()
                sb = tr.xpath('td[7]/div/a[3]/text()').extract_first()
                if not sa:
                    sa = 0
                if not sb:
                    sb = 0
                season['start_time'] = str(datetime.date.today().year) + '-' + time[0:5] + ' ' + time[6:11] + ':00'
                season['team_a'] = tr.xpath('td[6]/a/text()').extract_first()
                season['team_b'] = tr.xpath('td[8]/a/text()').extract_first()
                season['score_a'] = sa
                season['score_b'] = sb
                season['status'] = status
                season['fid'] = tr.xpath('@id').extract_first()[1:]
                yield season
