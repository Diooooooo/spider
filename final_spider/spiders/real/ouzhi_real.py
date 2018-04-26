# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from final_spider.items import OddsItem


# ******************************************
#                   欧赔
# ******************************************

class OuzhiSpider(scrapy.Spider):
    name = 'ouzhi_real'
    allowed_domains = ['500.com']
    start_urls = ['https://www.liangqiujiang.com/api/internal/getFutureSeason?manager=12345qwert']

    def parse(self, response):
        jsonInfo = json.loads(response.body.decode())
        for j in jsonInfo['datalist']:
            yield Request('http://odds.500.com/fenxi/ouzhi-%s.shtml' % j['season_fid'], self.parse_season_history_ouzhi,
                          dont_filter=True)

    def parse_season_history_ouzhi(self, response):
        odds = ['澳门', '立博', '伟德', '易胜博', 'Bet365', '竞彩官方', '威廉希尔', '皇冠', 'Interwetten', 'SNAI',
                'Oddset', 'Bwin', 'Gamebookers', 'Pinnacle平博', '10BET', 'Unibet (优胜客)', 'Smarkets',
                '利记', '香港马会', 'SportingBet (博天堂)']
        for t in response.xpath('//table[@id="datatb"]/tr'):
            if t.xpath('td[@class="tb_plgs"]/@title').extract_first() in odds:
                ods = OddsItem()
                ods['season_fid'] = str(response.url).split('-')[1].split(".")[0]
                ods['group_name'] = '欧赔'
                ods['league_name'] = t.xpath('td[@class="tb_plgs"]/@title').extract_first()
                win = t.xpath('td[3]/table/tbody/tr[1]/td[1]/text()').extract_first()
                deuce = t.xpath('td[3]/table/tbody/tr[1]/td[2]/text()').extract_first()
                lose = t.xpath('td[3]/table/tbody/tr[1]/td[3]/text()').extract_first()
                final_win = t.xpath('td[3]/table/tbody/tr[2]/td[1]/text()').extract_first()
                final_lose = t.xpath('td[3]/table/tbody/tr[2]/td[3]/text()').extract_first()
                final_deuce = t.xpath('td[3]/table/tbody/tr[2]/td[2]/text()').extract_first()
                if win:
                    if '↑' in win or '↓' in win:
                        win = win[:-1]
                else:
                    win = ''
                if lose:
                    if '↑' in lose or '↓' in lose:
                        lose = lose[:-1]
                else:
                    lose = ''
                if deuce:
                    if '↑' in deuce or '↓' in deuce:
                        deuce = deuce[:-1]
                else:
                    deuce = ''
                if final_win:
                    if '↑' in final_win or '↓' in final_win:
                        final_win = final_win[:-1]
                else:
                    final_win = ''
                if final_lose:
                    if '↑' in final_lose or '↓' in final_lose:
                        final_lose = final_lose[:-1]
                else:
                    final_lose = ''
                if final_deuce:
                    if '↑' in final_deuce or '↓' in final_deuce:
                        final_deuce = final_deuce[:-1]
                else:
                    final_deuce = ''
                ods['league_win'] = win
                ods['league_deuce'] = deuce
                ods['league_lose'] = lose
                ods['league_final_win'] = final_win
                ods['league_final_deuce'] = final_deuce
                ods['league_final_lose'] = final_lose
                yield ods
