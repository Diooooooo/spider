# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from final_spider.items import TeamItem


class TeamSpider(scrapy.Spider):
    name = 'team'
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
            yield Request(response.urljoin(r.xpath('@href').extract_first()), self.parse_season_history_tab)
        for r in response.xpath('//div[@class="ltab_hd lmb2 clearfix"]/a'):
            yield Request(response.urljoin(r.xpath('@href').extract_first()), self.parse_season_history, dont_filter=True)

    def parse_season_history(self, response):
        if response.xpath('//ul[@id="match_group"]'):
            # 遍历赛程 JSON格式
            for s in response.xpath('//ul[@class="lsaiguo_round_list clearfix"]/li'):
                url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid=%s&round=%s' % (
                str(response.url).split("-")[2][:-1], s.xpath('a/@data-group').extract_first())
                infoJson = json.loads(str(BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url=url)).read(), "html.parser")))
                for t in infoJson:
                    yield Request(response.urljoin('http://liansai.500.com/team/' + t['hid']), callback=self.parse_team)
                    yield Request(response.urljoin('http://liansai.500.com/team/' + t['gid']), callback=self.parse_team)
        elif response.xpath('//div[@id="season_match_list"]'):
            for s in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
                yield Request(response.urljoin(s.xpath('td[@class="td_lteam"]/a/@href').extract_first()), callback=self.parse_team)
                yield Request(response.urljoin(s.xpath('td[@class="td_rteam"]/a/@href').extract_first()), callback=self.parse_team)
        else:
            for s in response.xpath('//div[@class="lmb3"]'):
                for t in s.xpath('table/tbody/tr'):
                    yield Request(response.urljoin(str(t.xpath('td[@class="td_lteam"]/a/@href').extract_first())), callback=self.parse_team)
                    yield Request(response.urljoin(str(t.xpath('td[@class="td_rteam"]/a/@href').extract_first())), callback=self.parse_team)


    def parse_team(self, response):
        team_info = TeamItem()
        team_info['team_name'] = str.strip(response.xpath('//div[@class="itm_logo"]/img/@alt').extract_first())
        team_info['team_nickname'] = str.strip(response.xpath('//div[@class="itm_tit"]/text()').extract_first())
        team_info['team_name_en'] = str.strip(response.xpath('//div[@class="itm_name_en"]/text()').extract_first())
        url_split = str.split(response.url, '/')
        team_info['team_fid'] = str.strip(url_split[len(url_split) - 2])
        # aTag = response.xpath('//div[@class="lcrumbs"]/a').extract()
        # team_info['league_name'] = response.xpath('//div[@class="lcrumbs"]/a/text()')[len(aTag) - 1].extract()
        if "500logo" not in response.xpath('//div[@class="itm_logo"]/img/@src').extract_first():
            team_info['team_icon'] = \
            response.xpath('//div[@class="itm_logo"]/img/@src').extract_first().split("_")[1].split(".")[0]
            team_info['icon_url'] = str.strip(response.xpath('//div[@class="itm_logo"]/img/@src').extract_first())
        else:
            team_info['team_icon'] = ""
            team_info['icon_url'] = ""

        if len(response.xpath('//div[@class="itm_bd"]/table/tr[2]/td[1]/text()').extract_first().split("：")) > 1:
            team_info['team_country'] = \
            str.strip(response.xpath('//div[@class="itm_bd"]/table/tr[2]/td[1]/text()').extract_first().split("：")[1])
        else:
            team_info['team_country'] = ""

        if len(response.xpath('//div[@class="itm_bd"]/table/tr[3]/td[1]/text()').extract_first().split("：")) > 1:
            team_info['team_city'] = \
            str.strip(response.xpath('//div[@class="itm_bd"]/table/tr[3]/td[1]/text()').extract_first().split("：")[1])
        else:
            team_info['team_city'] = ""

        if len(response.xpath('//div[@class="itm_bd"]/table/tr[2]/td[2]/text()').extract_first().split("：")) > 1:
            team_info['team_home'] = \
            str.strip(response.xpath('//div[@class="itm_bd"]/table/tr[2]/td[2]/text()').extract_first().split("：")[1])
        else:
            team_info['team_home'] = ""

        if len(response.xpath('//div[@class="itm_bd"]/table/tr[1]/td[2]/text()').extract_first().split("：")) > 1:
            team_info['team_home_count'] = \
            str.strip(response.xpath('//div[@class="itm_bd"]/table/tr[1]/td[2]/text()').extract_first().split("：")[1])
        else:
            team_info['team_home_count'] = 0

        if len(response.xpath('//div[@class="itm_bd"]/table/tr[3]/td[2]/text()').extract_first().split("：")) > 1:
            team_info['team_price'] = \
            str.strip(response.xpath('//div[@class="itm_bd"]/table/tr[3]/td[2]/text()').extract_first().split("：")[1])
        else:
            team_info['team_price'] = ""
        if len(response.xpath('//div[@class="itm_bd"]/table/tr[1]/td[1]/text()').extract_first().split("：")) > 1:
            team_info['team_createdate'] = \
            str.strip(response.xpath('//div[@class="itm_bd"]/table/tr[1]/td[1]/text()').extract_first().split("：")[1])
        else:
            team_info['team_createdate'] = ""
        yield team_info

    def parse_season_history_tab(self, response):
        # 遍历赛程 非JSON格式
        for t in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
            yield Request(response.urljoin(str(t.xpath('td[@class="td_lteam"]/a/@href').extract_first())), callback=self.parse_team)
            yield Request(response.urljoin(str(t.xpath('td[@class="td_rteam"]/a/@href').extract_first())), callback=self.parse_team)
