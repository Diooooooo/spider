# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from final_spider.items import PlanItem, PlanRelationItem


def parse_team(response):
    if response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="l"]'):
        plan = PlanItem()
        plan['season_fid'] = str(response.url).split('-')[1].split('.')[0]
        plan['type'] = 'left'
        plan['plan'] = str(response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="l"]/text()').extract_first()).split("：")[1]
        yield plan
        p = PlanItem()
        p['season_fid'] = str(response.url).split('-')[1].split('.')[0]
        p['type'] = 'right'
        p['plan'] = str(response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="r"]/text()').extract_first()).split("：")[1]
        yield p

        if '暂无' not in plan['plan']:
            for l in response.xpath('//div[@class="statis-l "]/table/tbody/tr')[1:]:
                if l.xpath('td[3]/a').extract_first():
                    sp = l.xpath('td[3]/a/@href').extract_first()
                    if '-' in sp:
                        prl = PlanRelationItem()
                        prl['season_fid'] = str(response.url).split('-')[1].split('.')[0]
                        prl['type'] = 'left'
                        prl['sports_fid'] = str.split(sp, '-')[1][:-1]
                        s = l.xpath('td[2]/span/text()').extract_first()
                        statusId = '1'
                        if '替' == s:
                            statusId = '2'
                        prl['status_id'] = statusId
                        yield prl

        if '暂无' not in p['plan']:
            for r in response.xpath('//div[@class="statis-r "]/table/tbody/tr')[1:]:
                if r.xpath('td[3]/a').extract_first():
                    sp = r.xpath('td[3]/a/@href').extract_first()
                    if '-' in sp:
                        prl = PlanRelationItem()
                        prl['season_fid'] = str(response.url).split('-')[1].split('.')[0]
                        prl['type'] = 'right'
                        prl['sports_fid'] = str.split(sp, '-')[1][:-1]
                        s = r.xpath('td[2]/span/text()').extract_first()
                        statusId = '1'
                        if '替' == s:
                            statusId = '2'
                        prl['status_id'] = statusId
                        yield prl


def parse_season_history_tab(response):
    # 遍历赛程 非JSON格式
    for t in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
        yield Request(
            response.urljoin('http://odds.500.com/fenxi/stat-%s.shtml' % t.xpath('@data-fid').extract_first()),
            callback=parse_team, dont_filter=True)


def parse_season_history(response):
    if response.xpath('//ul[@id="match_group"]'):
        # 遍历赛程 JSON格式
        for s in response.xpath('//ul[@class="lsaiguo_round_list clearfix"]/li'):
            url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid=%s&round=%s' % (
                str(response.url).split("-")[2][:-1], s.xpath('a/@data-group').extract_first())
            infoJson = json.loads(
                str(BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url=url)).read(), "html.parser")))
            for t in infoJson:
                yield Request(response.urljoin('http://odds.500.com/fenxi/stat-%s.shtml' % t['fid']),
                              callback=parse_team, dont_filter=True)
    elif response.xpath('//div[@id="season_match_list"]'):
        for s in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
            yield Request(response.urljoin(
                'http://odds.500.com/fenxi/stat-%s.shtml' % s.xpath('@data-fid').extract_first()),
                          callback=parse_team, dont_filter=True)
    else:
        for s in response.xpath('//div[@class="lmb3"]'):
            for t in s.xpath('table/tbody/tr'):
                yield Request(response.urljoin(
                    'http://odds.500.com/fenxi/stat-%s.shtml' % t.xpath('@data-fid').extract_first()),
                              callback=parse_team, dont_filter=True)


def parse_detail_info(response):
    # 遍历选项卡（联赛赛程，联赛赛制）
    for r in response.xpath('//div[@class="ltab_hd lmb2 clearfix"]/a'):
        if r.xpath('@href').extract_first() != 'javascript:void(0);':
            yield Request(response.urljoin(r.xpath('@href').extract_first()), callback=parse_season_history, dont_filter=True)

    # 遍历选项卡（资格赛，附加赛，圈赛）
    for r in response.xpath('//div[@class="ltab_hd lmb3 clearfix"]/a'):
        if r.xpath('@href').extract_first() != 'javascript:void(0);':
            yield Request(response.urljoin(r.xpath('@href').extract_first()),
                          callback=parse_season_history_tab)


def parse_item_info(response):
    yield Request(response.urljoin(response.xpath('//div[@class="lcol_tit_r"][1]/a/@href').extract_first()),
                  parse_detail_info)


def parse_info(response):
    for t in response.xpath('//ul[@class="ldrop_list"]/li')[:2]:
        yield Request(response.urljoin(t.xpath('a/@href').extract_first()), parse_item_info)


class ZhenxSpider(scrapy.Spider):
    name = 'zhenx'
    allowed_domains = ['500.com']
    start_urls = ['http://liansai.500.com/']

    def parse(self, response):
        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[1:]:
            for li in t.xpath('li'):
                for d in li.xpath('div/a'):
                    yield Request(response.urljoin(d.xpath('@href').extract_first()), parse_info)

        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[:1]:
            for li in t.xpath('li'):
                yield Request(response.urljoin(li.xpath('a/@href').extract_first()), parse_info)
