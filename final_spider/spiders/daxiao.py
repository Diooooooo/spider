# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from final_spider.items import OddsItem


class DaxiaoSpider(scrapy.Spider):
    name = 'daxiao'
    allowed_domains = ['500.com']
    start_urls = ['http://liansai.500.com/']

    def parse(self, response):
        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[1:]:
            for li in t.xpath('li'):
                for d in li.xpath('div/a'):
                    yield Request(response.urljoin(d.xpath('@href').extract_first()), self.parse_info)

        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[:1]:
            for li in t.xpath('li'):
                yield Request(response.urljoin(li.xpath('a/@href').extract_first()), self.parse_info)

    def parse_info(self, response):
        for t in response.xpath('//ul[@class="ldrop_list"]/li')[:2]:
            yield Request(response.urljoin(t.xpath('a/@href').extract_first()), self.parse_item_info)

    def parse_item_info(self, response):
        yield Request(response.urljoin(response.xpath('//div[@class="lcol_tit_r"][1]/a/@href').extract_first()),
                      self.parse_detail_info)

    def parse_detail_info(self, response):
        # 遍历选项卡（联赛赛程，联赛赛制）
        for r in response.xpath('//div[@class="ltab_hd lmb2 clearfix"]/a'):
            if r.xpath('@href').extract_first() != 'javascript:void(0);':
                yield Request(response.urljoin(r.xpath('@href').extract_first()), callback=self.parse_season_history, dont_filter=True)

        # 遍历选项卡（资格赛，附加赛，圈赛）
        for r in response.xpath('//div[@class="ltab_hd lmb3 clearfix"]/a'):
            if r.xpath('@href').extract_first() != 'javascript:void(0);':
                yield Request(response.urljoin(r.xpath('@href').extract_first()),
                              callback=self.parse_season_history_tab, dont_filter=True)

    def parse_season_history(self, response):
        if response.xpath('//ul[@id="match_group"]'):
            # 遍历赛程 JSON格式
            for s in response.xpath('//ul[@class="lsaiguo_round_list clearfix"]/li'):
                url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid=%s&round=%s' % (
                    str(response.url).split("-")[2][:-1], s.xpath('a/@data-group').extract_first())
                infoJson = json.loads(
                    str(BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url=url)).read(), "html.parser")))
                for t in infoJson:
                    t_u = 'http://odds.500.com/fenxi/yazhi-%s.shtml' % t['fid']
                    yield Request(response.urljoin(t_u), callback=self.parse_season_history_ouzhi, dont_filter=True)
        elif response.xpath('//div[@id="season_match_list"]'):
            for s in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
                yield Request(response.urljoin('http://odds.500.com/fenxi/yazhi-%s.shtml' % s.xpath('@data-fid').extract_first()),
                              callback=self.parse_season_history_ouzhi, dont_filter=True)
        else:
            for s in response.xpath('//div[@class="lmb3"]'):
                for t in s.xpath('table/tbody/tr'):
                    yield Request(response.urljoin('http://odds.500.com/fenxi/yazhi-%s.shtml' % t.xpath('@data-fid').extract_first()),
                                  callback=self.parse_season_history_ouzhi, dont_filter=True)

    def parse_season_history_tab(self, response):
        # 遍历赛程 非JSON格式
        for t in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
            yield Request(response.urljoin('http://odds.500.com/fenxi/yazhi-%s.shtml' % t.xpath('@data-fid').extract_first()),
                          callback=self.parse_season_history_ouzhi, dont_filter=True)

    def parse_season_history_ouzhi(self, response):
        odds = ['威廉希尔', '澳门', '立博', 'Bet365', 'SNAI', '皇冠', '易胜博', '伟德', 'Bwin', 'Pinncale平博',
                '108bet', '10BET', 'Coral', '利记', 'Unibet (优胜客)', 'SportingBet (博天堂)', 'Mansion88 (明升)',
                '香港马会', '金宝博', 'Eurobet']
        for t in response.xpath('//table[@id="datatb"]/tr'):
            if t.xpath('td[@class="tb_plgs"]/p/a/@title').extract_first() in odds:
                ods = OddsItem()
                ods['season_fid'] = str(response.url).split('-')[1].split('.')[0]
                ods['group_name'] = '大小球'
                ods['league_name'] = t.xpath('td[@class="tb_plgs"]/p/a/@title').extract_first()
                ods['league_win'] = t.xpath('td[5]/table/tbody/tr[1]/td[1]/text()').extract_first()
                ods['league_deuce'] = t.xpath('td[5]/table/tbody/tr[1]/td[2]/text()').extract_first()
                ods['league_lose'] = t.xpath('td[5]/table/tbody/tr[1]/td[3]/text()').extract_first()
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
