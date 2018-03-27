# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from final_spider.items import OddsItem


class OuzhiSpider(scrapy.Spider):
    name = 'daxiao_real'
    allowed_domains = ['500.com']
    start_urls = ['http://liangqiujiang.com:8080/api/internal/getOddsSeason?manager=12345qwert']

    def parse(self, response):
        jsonInfo = json.loads(response.body.decode())
        for j in jsonInfo['datalist']:
            yield Request('http://odds.500.com/fenxi/daxiao-%s.shtml' % j['season_fid'],
                          parse_season_history_ouzhi)


def parse_season_history_ouzhi(response):
    odds = ['威廉希尔', '澳门', '立博', 'Bet365', 'SNAI', '皇冠', '易胜博', '伟德', 'Bwin', 'Pinncale平博',
            '108bet', '10BET', 'Coral', '利记', 'Unibet (优胜客)', 'SportingBet (博天堂)', 'Mansion88 (明升)',
            '香港马会', '金宝博', 'Eurobet']
    for t in response.xpath('//table[@id="datatb"]/tr'):
        if t.xpath('td[@class="tb_plgs"]/p/a/@title').extract_first() in odds:
            ods = OddsItem()
            ods['season_fid'] = str(response.url).split('-')[1].split(".")[0]
            ods['group_name'] = '大小球'
            ods['league_name'] = t.xpath('td[@class="tb_plgs"]/p/a/@title').extract_first()
            ods['league_win'] = t.xpath('td[3]/table/tbody/tr[1]/td[1]/text()').extract_first()
            ods['league_deuce'] = t.xpath('td[3]/table/tbody/tr[1]/td[2]/text()').extract_first()
            ods['league_lose'] = t.xpath('td[3]/table/tbody/tr[1]/td[3]/text()').extract_first()
            final_win = t.xpath('td[3]/table/tbody/tr/td[1]/text()').extract_first()
            final_lose = t.xpath('td[3]/table/tbody/tr/td[3]/text()').extract_first()
            if '↑' in final_win or '↓' in final_win:
                final_win = final_win[:-1]
            if '↑' in final_lose or '↓' in final_lose:
                final_lose = final_lose[:-1]
            ods['league_final_win'] = final_win
            ods['league_final_deuce'] = t.xpath('td[3]/table/tbody/tr/td[2]/text()').extract_first()
            ods['league_final_lose'] = final_lose
            yield ods
