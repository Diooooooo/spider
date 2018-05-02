# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from final_spider.items import PlanItem, PlanRelationItem


# ******************************
#            阵型
# ******************************

class ZhenxSpider(scrapy.Spider):
    name = 'zhenx_real'
    allowed_domains = ['500.com']
    start_urls = ['http://www.liangqiujiang.com/api/internal/getPlanSeason?manager=12345qwert']

    def parse(self, response):
        jsonInfo = json.loads(response.body.decode())
        for j in jsonInfo['datalist']:
            yield Request('http://odds.500.com/fenxi/stat-%s.shtml' % j['season_fid'], self.parse_team, dont_filter=True)

    def parse_team(self, response):
        if response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="l"]'):
            plan = PlanItem()
            plan['season_fid'] = str(response.url).split('-')[1].split('.')[0]
            plan['type'] = 'left'
            plan['plan'] = \
            str(response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="l"]/text()').extract_first()).split("：")[1]
            lt = str(response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="l"]/text()').extract_first()).split("：")[0]
            p = PlanItem()
            p['season_fid'] = str(response.url).split('-')[1].split('.')[0]
            p['type'] = 'right'
            p['plan'] = \
            str(response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="r"]/text()').extract_first()).split("：")[1]
            rt = str(response.xpath('//div[@class="zhenxing-t clearfix"]/p[@class="r"]/text()').extract_first()).split("：")[0]

            if '暂无' not in plan['plan'] and '上一场阵型' not in lt:
                yield plan
                for l in response.xpath('//div[@class="zhenxing-l"]/div'):
                    if l:
                        sp = l.xpath('a/@href').extract_first()
                        if '-' in sp:
                            prl = PlanRelationItem()
                            prl['season_fid'] = str(response.url).split('-')[1].split('.')[0]
                            prl['type'] = 'left'
                            prl['sports_fid'] = str.split(sp, '-')[1][:-1]
                            prl['status_id'] = '1'
                            yield prl
                for t in response.xpath('//div[@class="statis-l "]/table/tbody/tr')[1:]:
                    if t.xpath('td[3]/a').extract_first():
                        sp = t.xpath('td[3]/a/@href').extract_first()
                        if '-' in sp:
                            prl = PlanRelationItem()
                            prl['season_fid'] = str(response.url).split('-')[1].split('.')[0]
                            prl['type'] = 'left'
                            prl['sports_fid'] = str.split(sp, '-')[1][:-1]
                            s = t.xpath('td[2]/span/text()').extract_first()
                            if '替' == s:
                                prl['status_id'] = '2'
                                yield prl

            if '暂无' not in p['plan'] and '上一场阵型' not in rt:
                yield p
                for s in response.xpath('//div[@class="zhenxing-r"]/div'):
                    if s:
                        sp = s.xpath('a/@href').extract_first()
                        if '-' in sp:
                            prl = PlanRelationItem()
                            prl['season_fid'] = str(response.url).split('-')[1].split('.')[0]
                            prl['type'] = 'right'
                            prl['sports_fid'] = str.split(sp, '-')[1][:-1]
                            prl['status_id'] = '1'
                            yield prl
                for r in response.xpath('//div[@class="statis-r "]/table/tbody/tr')[1:]:
                    if r.xpath('td[3]/a').extract_first():
                        sp = r.xpath('td[3]/a/@href').extract_first()
                        if '-' in sp:
                            prl = PlanRelationItem()
                            prl['season_fid'] = str(response.url).split('-')[1].split('.')[0]
                            prl['type'] = 'right'
                            prl['sports_fid'] = str.split(sp, '-')[1][:-1]
                            s = r.xpath('td[2]/span/text()').extract_first()
                            if '替' == s:
                                prl['status_id'] = '2'
                                yield prl
