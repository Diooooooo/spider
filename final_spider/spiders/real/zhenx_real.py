# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from final_spider.items import PlanItem, PlanRelationItem


class ZhenxSpider(scrapy.Spider):
    name = 'zhenx_real'
    allowed_domains = ['500.com']
    start_urls = ['http://liangqiujiang.com:8080/api/internal/getPlanSeason?manager=12345qwert']

    def parse(self, response):
        jsonInfo = json.loads(response.body.decode())
        for j in jsonInfo['datalist']:
            yield Request('http://odds.500.com/fenxi/stat-%s.shtml' % j['season_fid'], parse_team)


def parse_team(response):
    if response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="l"]'):
        plan = PlanItem()
        plan['season_fid'] = str(response.url).split('-')[1].split('.')[0]
        plan['type'] = 'left'
        plan['plan'] = \
        str(response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="l"]/text()').extract_first()).split("：")[1]
        p = PlanItem()
        p['season_fid'] = str(response.url).split('-')[1].split('.')[0]
        p['type'] = 'right'
        p['plan'] = \
        str(response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="r"]/text()').extract_first()).split("：")[1]

        if '暂无' not in plan['plan']:
            yield plan
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
            yield p
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
