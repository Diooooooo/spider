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
            yield Request('http://live.500.com/detail.php?fid=%s' % j['season_fid'], self.parse_team, dont_filter=True)

    def parse_team(self, response):
        names = ['射正', '射门', '进攻']
        names2 = ['威胁进攻']
        names3 = ['控球']
        team_a = response.xpath('//div[@class="t2"]/table/tr/td[1]/h2/a/text()').extract_first()
        team_b = response.xpath('//div[@class="t2"]/table/tr/td[3]/h2/a/text()').extract_first()
        for k in response.xpath('//div[@class="t2"]/div[2]/table/tr'):
            n = k.xpath('td[3]/text()').extract_first()
            if n in names:
                n += '次数'
            elif n in names2:
                n = '危险进攻'
            elif n in names3:
                n = '控球率'
            jishu = TechniqueItem()
            jishu['season_fid'] = str(response.url).split('=')[1]
            jishu['league_jishu_name'] = n
            jishu['league_jishu_team_a_fs'] = k.xpath('td[2]/text()').extract_first()
            jishu['league_jishu_team_b_fs'] = k.xpath('td[4]/text()').extract_first()
            jishu['league_jishu_team_a'] = team_a
            jishu['league_jishu_team_b'] = team_b
            yield jishu
