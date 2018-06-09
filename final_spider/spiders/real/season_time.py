# -*- coding: utf-8 -*-
import datetime
import json

import requests
import scrapy


# ****************************************
#       处理比分，赛时，状态
# ****************************************
from final_spider.items import SeasonTime


class SeasonTypeDemoSpider(scrapy.Spider):
    name = 'season_time'
    allowed_domains = ['500.com']
    start_urls = ['http://live.500.com/static/info/bifen/xml/livedata/all/Full.txt']

    def parse(self, response):
        txt = json.loads(response.body)
        # jsonInfo = json.loads(requests.get('http://www.liangqiujiang.com/api/internal/getPlayingSeason?manager=12345qwert').text)
        jsonInfo = [724050]
        for t in txt:
            if t[0] in jsonInfo:
                time = SeasonTime()
                if 2 == t[1]:
                    playing = 45
                elif 0 == t[1]:
                    playing = 0
                elif 1 == t[1]:
                    playing = int((datetime.datetime.now() - datetime.datetime.strptime(t[4], '%Y-%m-%d %H:%M:%S')).seconds / 60)
                elif 3 == t[1]:
                    playing = int((datetime.datetime.now() - datetime.datetime.strptime(t[4], '%Y-%m-%d %H:%M:%S')).seconds / 60)
                elif 4 == t[1]:
                    playing = 90
                time['fid'] = t[0]
                time['playing'] = playing
                yield time

