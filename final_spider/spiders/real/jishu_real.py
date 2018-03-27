# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from final_spider.items import TechniqueItem


class JishuSpider(scrapy.Spider):
    name = 'jishu_real'
    allowed_domains = ['500.com']
    start_urls = ['http://liangqiujiang.com:8080/api/internal/getPlayingSeason?manager=12345qwert']

    def parse(self, response):
        jsonInfo = json.loads(response.body.decode())
        for j in jsonInfo['datalist']:
            yield Request('http://odds.500.com/fenxi/stat-%s.shtml' % j['season_fid'], self.parse_team)

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
