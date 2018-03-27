# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from final_spider.items import TechniqueItem


class JishuSpider(scrapy.Spider):
    name = 'jishu'
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
                yield Request(response.urljoin(r.xpath('@href').extract_first()), callback=self.parse_season_history)

        # 遍历选项卡（资格赛，附加赛，圈赛）
        for r in response.xpath('//div[@class="ltab_hd lmb3 clearfix"]/a'):
            if r.xpath('@href').extract_first() != 'javascript:void(0);':
                yield Request(response.urljoin(r.xpath('@href').extract_first()),
                              callback=self.parse_season_history_tab)

    def parse_season_history(self, response):
        if response.xpath('//ul[@id="match_group"]'):
            # 遍历赛程 JSON格式
            for s in response.xpath('//ul[@class="lsaiguo_round_list clearfix"]/li'):
                url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid=%s&round=%s' % (
                    str(response.url).split("-")[2][:-1], s.xpath('a/@data-group').extract_first())
                infoJson = json.loads(
                    str(BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url=url)).read(), "html.parser")))
                for t in infoJson:
                    yield Request(response.urljoin('http://odds.500.com/fenxi/stat-%s.shtml' % t['fid']),
                                  callback=self.parse_team, dont_filter=True)
        elif response.xpath('//div[@id="season_match_list"]'):
            for s in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
                yield Request(
                    response.urljoin('http://odds.500.com/fenxi/stat-%s.shtml' % s.xpath('@data-fid').extract_first()),
                    callback=self.parse_team, dont_filter=True)
            for s in response.xpath('//div[@class="lmb3"]'):
                for t in s.xpath('table/tbody/tr'):
                    yield Request(response.urljoin(
                        'http://odds.500.com/fenxi/stat-%s.shtml' % t.xpath('@data-fid').extract_first()),
                                  callback=self.parse_team, dont_filter=True)

    def parse_season_history_tab(self, response):
        # 遍历赛程 非JSON格式
        for t in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
            yield Request(
                response.urljoin('http://odds.500.com/fenxi/stat-%s.shtml' % t.xpath('@data-fid').extract_first()),
                callback=self.parse_team, dont_filter=True)

    def parse_team(self, response):
        for k in response.xpath('//div[@class="team-statis"]/table/tbody/tr'):
            if len(k.xpath('@def').extract()) > 0:
                jishu = TechniqueItem()
                jishu['season_fid'] = str(response.url).split('-')[1].split('.')[0]
                jishu['league_jishu_name'] = k.xpath('td[3]/text()').extract_first()
                jishu['league_jishu_team_a_fs'] = k.xpath('td[2]/text()').extract_first()
                jishu['league_jishu_team_b_fs'] = k.xpath('td[4]/text()').extract_first()
                jishu['league_jishu_team_a'] = response.xpath('//ul[@class="odds_hd_list"]')[0].xpath(
                    'li/a/text()').extract_first()
                jishu['league_jishu_team_b'] = response.xpath('//ul[@class="odds_hd_list"]')[1].xpath(
                    'li/a/text()').extract_first()
                yield jishu
