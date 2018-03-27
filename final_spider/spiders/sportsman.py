# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from final_spider.items import SportsmanItem


class SportsmanSpider(scrapy.Spider):
    name = 'sportsman'
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
        for t in response.xpath('//ul[@class="ldrop_list"]/li')[:4]:
            yield Request(response.urljoin(t.xpath('a/@href').extract_first()), self.parse_item_info)

    def parse_item_info(self, response):
        yield Request(response.urljoin(response.xpath('//div[@class="lcol_tit_r"][1]/a/@href').extract_first()),
                      self.parse_detail_info)

    def parse_detail_info(self, response):
        for r in response.xpath('//div[@class="ltab_hd lmb3 clearfix"]/a'):
            if r.xpath('@href').extract_first() != 'javascript:void(0);':
                yield Request(response.urljoin(r.xpath('@href').extract_first()), self.parse_season_history_tab)
        for r in response.xpath('//div[@class="ltab_hd lmb2 clearfix"]/a'):
            if r.xpath('@href').extract_first() != 'javascript:void(0);':
                yield Request(response.urljoin(r.xpath('@href').extract_first()), self.parse_season_history, dont_filter=True)

    def parse_season_history(self, response):
        if response.xpath('//ul[@id="match_group"]'):
            # 遍历赛程 JSON格式
            for s in response.xpath('//ul[@class="lsaiguo_round_list clearfix"]/li'):
                url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid=%s&round=%s' % (
                str(response.url).split("-")[2][:-1], s.xpath('a/@data-group').extract_first())
                infoJson = json.loads(str(BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url)).read(), "html.parser")))
                for t in infoJson:
                    yield Request(response.urljoin('http://liansai.500.com/team/%s/teamlineup/'%t['hid']), self.parse_sportsman_iteration)
                    yield Request(response.urljoin('http://liansai.500.com/team/%s/teamlineup/'%t['gid']), self.parse_sportsman_iteration)
        elif response.xpath('//div[@id="season_match_list"]'):
            for s in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
                yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%s.xpath('td[@class="td_lteam"]/a/@href').extract_first()), self.parse_sportsman_iteration)
                yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%s.xpath('td[@class="td_rteam"]/a/@href').extract_first()), self.parse_sportsman_iteration)
        else:
            for s in response.xpath('//div[@class="lmb3"]'):
                for t in s.xpath('table/tbody/tr'):
                    yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%t.xpath('td[@class="td_lteam"]/a/@href').extract_first()), self.parse_sportsman_iteration)
                    yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%t.xpath('td[@class="td_rteam"]/a/@href').extract_first()), self.parse_sportsman_iteration)


    def parse_season_history_tab(self, response):
        # 遍历赛程 非JSON格式
        for t in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
            yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%t.xpath('td[@class="td_lteam"]/a/@href').extract_first()), self.parse_sportsman_iteration)
            yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%t.xpath('td[@class="td_rteam"]/a/@href').extract_first()), self.parse_sportsman_iteration)


    def parse_sportsman_iteration(self, response):
        for qf in response.xpath('//table[@class=" lqiuy_list lqiuy_list_qf  ltable ltable_auto lmb jTrHover"]/tbody/tr'):
            yield Request(response.urljoin(qf.xpath('td[@class="td_qiuy"]/span/a/@href').extract_first()),
                          self.parse_sportsman)
        for zc in response.xpath('//table[@class=" lqiuy_list lqiuy_list_zc  ltable ltable_auto lmb jTrHover"]/tbody/tr'):
            yield Request(response.urljoin(zc.xpath('td[@class="td_qiuy"]/span/a/@href').extract_first()),
                          self.parse_sportsman)
        for hw in response.xpath('//table[@class=" lqiuy_list lqiuy_list_hw  ltable ltable_auto lmb jTrHover"]/tbody/tr'):
            yield Request(response.urljoin(hw.xpath('td[@class="td_qiuy"]/span/a/@href').extract_first()),
                          self.parse_sportsman)
        for smy in response.xpath('//table[@class=" lqiuy_list lqiuy_list_smy  ltable ltable_auto lmb jTrHover"]/tbody/tr'):
            yield Request(response.urljoin(smy.xpath('td[@class="td_qiuy"]/span/a/@href').extract_first()),
                          self.parse_sportsman)

    def parse_sportsman(self, response):
        man_info = SportsmanItem()
        man_info['league_sports_name'] = response.xpath('//div[@class="itm_img"]/img/@title').extract_first()
        man_info['league_sports_name_en'] = response.xpath('//div[@class="itm_name_en"]/text()').extract_first()
        fid_ls = str.split(response.url, '-')
        man_info['sports_fid'] = fid_ls[1][:-1]
        if "notfound" not in response.xpath('//div[@class="itm_img"]/img/@src').extract_first():
            man_info['league_sports_img'] = \
            response.xpath('//div[@class="itm_img"]/img/@src').extract_first().split("_")[1].split(".")[0]
            man_info['icon_url'] = response.xpath('//div[@class="itm_img"]/img/@src').extract_first()
        else:
            man_info['league_sports_img'] = ""
            man_info['icon_url'] = ""

        if len(response.xpath('//div[@class="itm_bd"]/table/tr[4]/td[2]/text()').extract_first().split("：")) > 1:
            man_info['league_sports_number'] = \
            response.xpath('//div[@class="itm_bd"]/table/tr[4]/td[2]/text()').extract_first().split("：")[1]
        else:
            man_info['league_sports_number'] = ""
        if len(response.xpath('//div[@class="itm_bd"]/table/tr[3]/td[2]/text()').extract_first().split("：")) > 1:
            man_info['league_sports_role'] = \
            response.xpath('//div[@class="itm_bd"]/table/tr[3]/td[2]/text()').extract_first().split("：")[1]
        else:
            man_info['league_sports_role'] = ""
        if len(response.xpath('//div[@class="itm_bd"]/table/tr[1]/td[2]/text()').extract_first().split("：")) > 1:
            man_info['league_sports_country'] = \
            response.xpath('//div[@class="itm_bd"]/table/tr[1]/td[2]/text()').extract_first().split("：")[1]
        else:
            man_info['league_sports_country'] = ""
        if len(response.xpath('//div[@class="itm_bd"]/table/tr[2]/td[1]/text()').extract_first().split("：")) > 1:
            man_info['league_sports_birthday'] = \
            response.xpath('//div[@class="itm_bd"]/table/tr[2]/td[1]/text()').extract_first().split("：")[1]
        else:
            man_info['league_sports_birthday'] = ""
        if len(response.xpath('//div[@class="itm_bd"]/table/tr[3]/td[1]/text()').extract_first().split("：")) > 1:
            man_info['league_sports_stature'] = \
            response.xpath('//div[@class="itm_bd"]/table/tr[3]/td[1]/text()').extract_first().split("：")[1][:-2]
        else:
            man_info['league_sports_stature'] = ""
        if len(response.xpath('//div[@class="itm_bd"]/table/tr[4]/td[1]/text()').extract_first().split("：")) > 1:
            man_info['league_sports_weight'] = \
            response.xpath('//div[@class="itm_bd"]/table/tr[4]/td[1]/text()').extract_first().split("：")[1][:-2]
        else:
            man_info['league_sports_weight'] = ""
        if len(response.xpath('//div[@class="itm_bd"]/table/tr[1]/td[3]/text()').extract_first().split("：")) > 1:
            man_info['league_sports_price'] = \
            response.xpath('//div[@class="itm_bd"]/table/tr[1]/td[3]/text()').extract_first().split("：")[1]
        else:
            man_info['league_sports_price'] = ""
        yield man_info

