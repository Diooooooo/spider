# -*- coding: utf-8 -*-
import json
from urllib.parse import unquote

import scrapy
from scrapy import Request

from final_spider.items import ScoreItem


class ScoreSpider(scrapy.Spider):
    name = 'score_real'
    allowed_domains = ['500.com']
    start_urls = ['http://liansai.500.com/']

    def parse(self, response):
        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[1:]:
            for li in t.xpath('li'):
                for d in li.xpath('div/a'):
                    yield Request(response.urljoin(d.xpath('@href').extract_first()), self.parse_item_info, dont_filter=True)

        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[:1]:
            for li in t.xpath('li'):
                yield Request(response.urljoin(li.xpath('a/@href').extract_first()), self.parse_item_info, dont_filter=True)

    def parse_item_info(self, response):
        yield Request(response.urljoin(response.xpath('//div[@class="lcol_tit_r"][1]/a/@href').extract_first()),
                      self.parse_item_url_info, dont_filter=True)

    def parse_item_url_info(self, response):
        types = ['总榜单', '主场', '客场', '上半场', '下半场']
        leagueName = response.xpath('//ul[@class="lpage_race_nav clearfix"]/li[1]/a/text()').extract_first()[:-2]
        year = response.xpath('//span[@class="ldrop_tit_txt"]/text()').extract_first()[:-2]
        if '/' in year:
            year = year.split('/')[1] + '-00-00'
        else:
            year = year + '-00-00'
        for u in response.xpath('//div[@id="match_hot_div"]/a'):
            if u.xpath('text()').extract_first() in types:
                tid = response.url.split('-')[-1]
                if '/' in tid:
                    tid = tid[:len(tid) - 1]
                yield Request(
                    response.urljoin('/index.php?c=score&a=getHotScore&stid=%s&type=%s&leagueName=%s&year=%s'%
                                     (tid, u.xpath('@data-type').extract_first(), leagueName, year)),
                    self.parse_detail_info, dont_filter=True)

    def parse_detail_info(self, response):
        typeName = response.url.split('=')[-3].split('&')[0]
        if 'all' == typeName:
            typeName = '积分榜'
        elif 'half' == typeName:
            typeName = '上半场'
        elif 'second_half' == typeName:
            typeName = '下半场'
        elif 'home' == typeName:
            typeName = '主场'
        elif 'away' == typeName:
            typeName = '客场'
        jsonInfo = json.loads(response.body.decode())
        score = ScoreItem()
        score['type_name'] = unquote(typeName)
        score['league_name'] = unquote(response.url.split('=')[-2].split('&')[0])
        score['league_year'] = response.url.split('=')[-1]
        for j in jsonInfo:
            score['team_name'] = str(j['teamname'])
            score['season_count'] = str(j['total'])
            score['season_vicotry'] = str(j['win'])
            score['season_deuce'] = str(j['draw'])
            score['season_lose'] = str(j['lost'])
            score['season_in'] = str(j['jq'])
            score['season_out'] = str(j['sq'])
            score['season_win'] = str(j['js'])
            score['avg_vicotry'] = str(j['ain'])
            score['avg_lose'] = str(j['aln'])
            if 0 == j['total']:
                score['probability_vicotry'] = ''
                score['probability_deuce'] = ''
                score['probability_lose'] = ''
            else:
                score['probability_vicotry'] = str(j['win']*100/j['total'])[:5] + '%'
                score['probability_deuce'] = str(j['draw']*100/j['total'])[:5] + '%'
                score['probability_lose'] = str(j['lost']*100/j['total'])[:5] + '%'
            score['season_source'] = str(j['score'])
            yield score
