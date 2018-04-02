# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request

from final_spider.items import OddsItem


class YazhiSpider(scrapy.Spider):
    name = 'yazhi_real'
    allowed_domains = ['500.com']
    start_urls = ['http://liangqiujiang.com:8080/api/internal/getOddsSeason?manager=12345qwert']

    def parse(self, response):
        jsonInfo = json.loads(response.body.decode())
        for j in jsonInfo['datalist']:
            yield Request('http://odds.500.com/fenxi/yazhi-%s.shtml' % j['season_fid'], parse_season_history_ouzhi)

    def parse_season_history_ouzhi(self, response):
        odds = ['澳门', '伟德', '易胜博', 'Bet365', '立博', '皇冠', 'Pinnacle平博', '10BET', '利记',
                'Unibet (优胜客)', 'Mansion88 (明升)', '金宝博', '香港马会', '必发', '1xBet']
        for t in response.xpath('//table[@id="datatb"]/tr'):
            if t.xpath('td[@class="tb_plgs"]/p/a/@title').extract_first() in odds:
                ods = OddsItem()
                ods['season_fid'] = str(response.url).split('-')[1].split('.')[0]
                ods['group_name'] = '亚盘'
                ods['league_name'] = t.xpath('td[@class="tb_plgs"]/p/a/@title').extract_first()
                win = t.xpath('td[5]/table/tbody/tr[1]/td[1]/text()').extract_first()
                deuce = t.xpath('td[5]/table/tbody/tr[1]/td[2]/text()').extract_first()
                lose = t.xpath('td[5]/table/tbody/tr[1]/td[3]/text()').extract_first()
                final_win = t.xpath('td[3]/table/tbody/tr/td[1]/text()').extract_first()
                final_lose = t.xpath('td[3]/table/tbody/tr/td[3]/text()').extract_first()
                final_deuce = t.xpath('td[3]/table/tbody/tr/td[2]/text()').extract_first()
                if '↑' in win or '↓' in win:
                    win = win[:-1]
                if '↑' in lose or '↓' in lose:
                    lose = lose[:-1]
                if '↑' in deuce or '↓' in deuce:
                    deuce = deuce[:-1]
                if '↑' in final_win or '↓' in final_win:
                    final_win = final_win[:-1]
                if '↑' in final_lose or '↓' in final_lose:
                    final_lose = final_lose[:-1]
                if '↑' in final_deuce or '↓' in final_deuce:
                    final_deuce = final_deuce[:-1]
                ods['league_win'] = win
                ods['league_deuce'] = deuce
                ods['league_lose'] = lose
                ods['league_final_win'] = final_win
                ods['league_final_deuce'] = final_deuce
                ods['league_final_lose'] = final_lose
                yield ods

