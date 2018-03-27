# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from final_spider.items import EventItem


class EventSpider(scrapy.Spider):
    name = 'event'
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
                    yield Request(response.urljoin('http://odds.500.com/fenxi/stat-' + t['fid'] + '.shtml'),
                                  callback=self.parse_team, dont_filter=True)
        elif response.xpath('//div[@id="season_match_list"]'):
            for s in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
                yield Request(response.urljoin(
                    'http://odds.500.com/fenxi/stat-' + s.xpath('@data-fid').extract_first() + '.shtml'),
                              callback=self.parse_team, dont_filter=True)
        else:
            for s in response.xpath('//div[@class="lmb3"]'):
                for t in s.xpath('table/tbody/tr'):
                    yield Request(response.urljoin(
                        'http://odds.500.com/fenxi/stat-' + t.xpath('@data-fid').extract_first() + '.shtml'),
                                  callback=self.parse_team, dont_filter=True)

    def parse_season_history_tab(self, response):
        # 遍历赛程 非JSON格式
        for t in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
            yield Request(
                response.urljoin('http://odds.500.com/fenxi/stat-' + t.xpath('@data-fid').extract_first() + '.shtml'),
                callback=self.parse_team, dont_filter=True)

    def parse_team(self, response):
        yield Request(response.urljoin('http://odds.500.com/fenxi1/inc/stat_ajax.php?act=event&id=%s'%response.url.split('-')[1].split('.')[0]), callback=self.parse_team_detail, dont_filter=True)


    def parse_team_detail(self, response):
        infoJson = json.loads(response.body)
        season_fids = response.url.split('=')
        for t in infoJson['eventlist']:
            event = EventItem()
            event['season_fid'] = season_fids[len(season_fids) - 1]
            event['is_home'] = t['is_home']
            event['time'] = t['time']
            event['type'] = t['type']
            contentHtml = BeautifulSoup(t['content'])
            if t['type'] == 'player-change':
                aObj = contentHtml.find_all('a')
                if aObj:
                    sportsmanId = aObj[0].attrs['href']
                    if '-' in sportsmanId:
                        sportsmanId = sportsmanId.split('-')[1][:-1]

                    sportsmanName = aObj[0].text

                    sportsmanId2 = aObj[1].attrs['href']
                    if '-' in sportsmanId2:
                        sportsmanId2 = sportsmanId2.split('-')[1][:-1]

                    sportsmanName2 = aObj[1].text
                    contentHtml = sportsmanId + '-' + sportsmanName + '~' + sportsmanId2 + '-' + sportsmanName2
                else:
                    sportsmanName = contentHtml.text.split('(')[1].split(')')[0]
                    sportsmanName2 = contentHtml.text.split('(')[2].split(')')[0]
                    contentHtml = sportsmanName + '~' + sportsmanName2
            else:
                target = contentHtml.find('a')
                sportsmanId = None
                if target:
                    if '-' in target.attrs['href']:
                        sportsmanId = target.attrs['href'][1][:-1]

                    sportsmanName = target.text

                    if sportsmanId:
                        contentHtml = sportsmanId + '-' + sportsmanName
                    else:
                        contentHtml = sportsmanName
                else:
                    contentHtml = contentHtml.text

            event['content'] = contentHtml
            yield event

