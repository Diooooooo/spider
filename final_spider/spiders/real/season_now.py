# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from final_spider.items import SeasonItem


# ******************************
#           DELETE
# ******************************

class LqjSpider(scrapy.Spider):
    name = 'season_now'
    allowed_domains = ['500.com']
    start_urls = ['http://liansai.500.com/']

    def parse(self, response):
        types = ['英超', '西甲', '意甲', '德甲', '法甲', '欧冠', '欧罗巴', '世界杯', '中超', '英乙', '英足总杯', '英联杯',
                 '英甲', '西乙', '西班牙杯', '马来足总', '意乙', '意杯', '日联杯', '德乙', '德国杯', '巴西杯', '法国杯',
                 '法乙', '韩联盟', '欧超杯', '美职联', '智甲', '亚洲杯', '亚冠杯', '解放者杯', '友谊赛', '亚挑杯', '世青赛',
                 '亚协杯', '比甲', '比杯', '丹超', '俄超', 'K1联赛', '荷甲', '荷乙', '马来超', '日职', '挪超', '葡超',
                 '日职乙', '瑞士超', '瑞典超', '苏超', '苏挑杯', '土超', '爱联杯', '以超', '阿超杯', '巴圣锦', '墨超杯', '澳超']
        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[1:]:
            for li in t.xpath('li'):
                for d in li.xpath('div/a'):
                    if d.xpath('text()').extract_first() in types:
                        yield Request(response.urljoin(d.xpath('@href').extract_first()),
                                      self.parse_item_info, dont_filter=True)

        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[:1]:
            for li in t.xpath('li'):
                if li.xpath('a/text()').extract_first() in types:
                    yield Request(response.urljoin(li.xpath('a/@href').extract_first()),
                                  self.parse_item_info, dont_filter=True)

        for t in response.xpath('//table[@class="lrace_bei"]'):
            for tr in t.xpath('tr'):
                for td in tr.xpath("td"):
                    if td.xpath('a/text()').extract_first() in types:
                        yield Request(response.urljoin(td.xpath('a/@href').extract_first()),
                                      self.parse_item_info, dont_filter=True)
    # def parse_info(self, response):
    #     for t in response.xpath('//ul[@class="ldrop_list"]/li')[1:4]:
    #         yield Request(response.urljoin(t.xpath('a/@href').extract_first()), self.parse_item_info)

    def parse_item_info(self, response):
        yield Request(response.urljoin(response.xpath('//div[@class="lcol_tit_r"][1]/a/@href').extract_first()),
                      self.parse_detail_info, dont_filter=True)

    def parse_detail_info(self, response):
        for r in response.xpath('//div[@class="ltab_hd lmb3 clearfix"]/a'):
            if r.xpath('@data-id'):
                yield Request(response.urljoin(r.xpath('@href').extract_first()), self.parse_line_info2, dont_filter=True)
        for r in response.xpath('//div[@class="ltab_hd lmb2 clearfix"]/a'):
            if r.xpath('@data-id'):
                yield Request(response.urljoin(r.xpath('@href').extract_first()), self.parse_line_info, dont_filter=True)

    def parse_line_info(self, response):
        if response.xpath('//ul[@id="match_group"]'):
            # 遍历赛程 JSON格式
            year = response.xpath('//span[@class="ldrop_tit_txt"]/text()').extract_first()[:-2]
            if '/' in year:
                year = year.split('/')[0] + '-00-00'
            else:
                year = year + '-00-00'
            for s in response.xpath('//ul[@class="lsaiguo_round_list clearfix"]/li'):
                url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid=%s&round=%s' % (
                str(response.url).split("-")[2][:-1], s.xpath('a/@data-group').extract_first())
                infoJson = json.loads(str(BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url)).read(), "html.parser")))
                for t in infoJson:
                    season = SeasonItem()
                    season['league_name'] = response.xpath(
                        '//ul[@class="lpage_race_nav clearfix"]/li[1]/a/text()').extract_first()[:-2]
                    season['type_name'] = response.xpath(
                        '//div[@id="match_stage"]/a[@class="ltab_btn on"]/text()').extract_first()
                    season['sub_type_name'] = ''
                    season['game_week'] = t['round']
                    season['start_time'] = t['stime']
                    season['team_a'] = t['hname']
                    season['team_b'] = t['gname']
                    if t['status'] == '5':
                        season['score_a'] = t['hscore']
                        season['score_b'] = t['gscore']
                    else:
                        season['score_a'] = 0
                        season['score_b'] = 0

                    statusId = 1
                    if t['status'] in ['-1', '2', '4', '6', '7', '11']:
                        statusId = 6
                    if t['status'] == '5':
                        statusId = 4
                    season['status'] = statusId
                    season['fid'] = t['fid']
                    season['year'] = year
                    yield season
        elif response.xpath('//div[@id="season_match_list"]'):
            for s in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
                yield self.buildSeasonItem(response, s)
        else:
            for s in response.xpath('//div[@class="lmb3"]'):
                for t in s.xpath('table/tbody/tr'):
                    yield self.buildSeasonItem(response, t)

    def buildSeasonItem(self, response, s):
        year = response.xpath('//span[@class="ldrop_tit_txt"]/text()').extract_first()[:-2]
        if '/' in year:
            year = year.split('/')[0] + '-00-00'
        else:
            year = year + '-00-00'
        season = SeasonItem()
        season['league_name'] = response.xpath('//ul[@class="lpage_race_nav clearfix"]/li[1]/a/text()').extract_first()[
                                :-2]
        season['type_name'] = response.xpath('//div[@id="match_stage"]/a[@class="ltab_btn on"]/text()').extract_first()
        if s.xpath('h4/text()').extract_first():
            season['sub_type_name'] = s.xpath('h4/text()').extract_first()
        else:
            season['sub_type_name'] = ''
        season['game_week'] = ''
        season['start_time'] = s.xpath('td[@class="td_time"]/text()').extract_first()
        season['team_a'] = s.xpath('td[@class="td_lteam"]/a/@title').extract_first()
        season['team_b'] = s.xpath('td[@class="td_rteam"]/a/@title').extract_first()
        if s.xpath('@data-status').extract_first() == '5':
            season['score_a'] = s.xpath('td[3]/span[1]/text()').extract_first()
            season['score_b'] = s.xpath('td[3]/span[2]/text()').extract_first()
        else:
            season['score_a'] = 0
            season['score_b'] = 0
        statusId = 1
        status = s.xpath('@data-status').extract_first()
        if status in ['-1', '2', '4', '6', '7', '11']:
            statusId = 6
        if status == '5':
            statusId = 4
        season['status'] = statusId
        season['fid'] = s.xpath('@data-fid').extract_first()
        season['year'] = year
        yield season

    def parse_line_info2(self, response):
        year = response.xpath('//span[@class="ldrop_tit_txt"]/text()').extract_first()[:-2]
        if '/' in year:
            year = year.split('/')[0] + '-00-00'
        else:
            year = year + '-00-00'
        # 遍历赛程 非JSON格式
        for t in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
            season = SeasonItem()
            season['league_name'] = response.xpath(
                '//ul[@class="lpage_race_nav clearfix"]/li[1]/a/text()').extract_first()[:-2]
            season['type_name'] = response.xpath(
                '//div[@id="match_stage"]/a[@class="ltab_btn on"]/text()').extract_first()
            season['sub_type_name'] = ''
            season['game_week'] = ''
            season['start_time'] = t.xpath('td[@class="td_time"]/text()').extract_first()
            season['team_a'] = t.xpath('td[@class="td_lteam"]/a/@title').extract_first()
            season['team_b'] = t.xpath('td[@class="td_rteam"]/a/@title').extract_first()
            if t.xpath('@data-status').extract_first() == '5':
                season['score_a'] = t.xpath('td[3]/span[1]/text()').extract_first()
                season['score_b'] = t.xpath('td[3]/span[2]/text()').extract_first()
            else:
                season['score_a'] = 0
                season['score_b'] = 0

            statusId = 1
            status = t.xpath('@data-status').extract_first()
            if status in ['-1', '2', '4', '6', '7', '11']:
                statusId = 6
            if status == '5':
                statusId = 4
            season['status'] = statusId
            season['fid'] = t.xpath('@data-fid').extract_first()
            season['year'] = year
            yield season