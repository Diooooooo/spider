# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from final_spider.items import EventItem


class BifenSpider(scrapy.Spider):
    name = 'bifen'
    allowed_domains = ['500.com']
    start_urls = ['http://liangqiujiang.com:8080/api/internal/getPlayingSeason?manager=12345qwert']

    def parse(self, response):
        jsonInfo = json.loads(response.body.decode())
        for j in jsonInfo['datalist']:
            yield Request('http://live.500.com/detail.php?fid=%s' % j['season_fid'], self.parse_detail,
                          dont_filter=True)

    def parse_detail(self, response):
        firstTd = response.xpath('//table[@class="mtable"]/tr')[1].xpath('td')
        if firstTd[0].xpath('img') or firstTd[4].xpath('img'):
            season_fids = response.url.split('=')
            for r in response.xpath('//table[@class="mtable"]/tr')[1:]:
                td = r.xpath('td')
                if td[0].xpath('img') or td[4].xpath('img'):
                    t1 = td[0].xpath('img/@src').extract_first()
                    is_home = 0
                    play_type = None
                    event = EventItem()
                    event['season_fid'] = season_fids[len(season_fids) - 1]
                    if t1:
                        t1 = str.split(t1, '/')
                        t1 = t1[len(t1) - 1].split('.')[0]
                        is_home = 1
                    t3 = td[2].xpath('text()').extract_first()
                    if t3:
                        t3 = t3[:-1]
                    t5 = td[4].xpath('img/@src').extract_first()
                    if t5:
                        t5 = str.split(t5, '/')
                        t5 = t5[len(t5) - 1].split('.')[0]
                    if t1 == '1' or t5 == '1':
                        play_type = 'goal'
                    if t1 == '2' or t5 == '2':
                        play_type = 'goal-own'
                    if t1 == '3' or t5 == '3':
                        play_type = 'goal-kick'
                    if t1 == '4' or t5 == '4':
                        play_type = 'yellow-card'
                    if t1 == '5' or t5 == '5':
                        play_type = 'red-card'
                    if t1 == '6' or t5 == '6':
                        play_type = 'yellow-card2'
                    if t1 == '7' or t5 == '7':
                        play_type = 'goal-void'
                    if t1 == '8' or t5 == '8':
                        play_type = 'player-change'
                    event['is_home'] = is_home
                    event['time'] = t3
                    event['type'] = play_type
                    if is_home == 1:
                        if event['type'] == 'player-change':
                            if td[1].xpath('text()'):
                                f = str(td[1].xpath('text()').extract()[0])
                                s = str(td[1].xpath('text()').extract()[1])
                                if f and s:
                                    content = f + '~' + s
                                elif f and not s:
                                    content = f + '~'
                                elif not f and s:
                                    content = '~' + s
                                else:
                                    content = ''
                        else:
                            if td[1]:
                                content = td[1].xpath('text()').extract_first()
                                if not content:
                                    content = ''
                            else:
                                content = ''
                    else:
                        if event['type'] == 'player-change':
                            if td[3].xpath('text()'):
                                f = str(td[3].xpath('text()').extract()[0])
                                s = str(td[3].xpath('text()').extract()[1])
                                if f and s:
                                    content = f + '~' + s
                                elif f and not s:
                                    content = f + '~'
                                elif not f and s:
                                    content = '~' + s
                                else:
                                    content = ''
                            else:
                                content = ''
                        else:
                            if td[3]:
                                content = td[3].xpath('text()').extract_first()
                                if not content:
                                    content = ''
                            else:
                                content = ''
                    content.replace('(', '').replace(')', '').replace(' ', '')
                    event['content'] = content
                    yield event
