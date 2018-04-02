# -*- coding: utf-8 -*-

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
                    yield Request(response.urljoin(d.xpath('@href').extract_first()), self.parse_item_info)

        for t in response.xpath('//ul[@class="lallrace_main_list clearfix"]')[:1]:
            for li in t.xpath('li'):
                yield Request(response.urljoin(li.xpath('a/@href').extract_first()), self.parse_item_info)

    # def parse_info(self, response):
    #     for t in response.xpath('//ul[@class="ldrop_list"]/li')[:4]:
    #         yield Request(response.urljoin(t.xpath('a/@href').extract_first()), self.parse_item_info)

    def parse_item_info(self, response):
        yield Request(response.urljoin(response.xpath('//div[@class="lcol_tit_r"][1]/a/@href').extract_first()),
                      self.parse_detail_info)

    def parse_item_url_info(self, response):
        types = ['总榜单', '主场', '客场', '上半场', '下半场']
        for u in response.xpath('//div[@id="match_hot_div"]/a'):
            if u in types:
                pass

    def parse_detail_info(self, response):
        for r in response.xpath('//tbody[@id="hot_score_tbody"]/tr'):
            score = ScoreItem()
            score['type_name'] = response.xpath('//div[@class="lcol_hd lcol_hd_nobd"]/h3/text()').extract()[1]
            score['league_name'] = response.xpath('//ul[@class="lpage_race_nav clearfix"]/li[1]/a/text()').extract_first()[:-2]
            year = response.xpath('//span[@class="ldrop_tit_txt"]/text()').extract_first()[:-2]
            if '/' in year:
                score['league_year'] = year.split('/')[1] + '-00-00'
            else:
                score['league_year'] = year + '-00-00'
            score['team_name'] = r.xpath('td[@class="td_qiud"]/span/a/@title').extract_first()
            score['season_count'] = r.xpath('td[4]/text()').extract_first()
            score['season_vicotry'] = r.xpath('td[5]/text()').extract_first()
            score['season_deuce'] = r.xpath('td[6]/text()').extract_first()
            score['season_lose'] = r.xpath('td[7]/text()').extract_first()
            score['season_in'] = r.xpath('td[8]/text()').extract_first()
            score['season_out'] = r.xpath('td[9]/text()').extract_first()
            score['season_win'] = r.xpath('td[10]/text()').extract_first()
            score['avg_vicotry'] = r.xpath('td[11]/text()').extract_first()
            score['avg_lose'] = r.xpath('td[12]/text()').extract_first()
            score['probability_vicotry'] = r.xpath('td[@class="td_shengl"]/span/text()').extract_first()
            score['probability_deuce'] = r.xpath('td[@class="td_pingl"]/span/text()').extract_first()
            score['probability_lose'] = r.xpath('td[@class="td_ful"]/span/text()').extract_first()
            score['season_source'] = r.xpath('td[@class="td_jif"]/text()').extract_first()
            yield score
