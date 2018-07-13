# -*- coding: utf-8 -*-
import json

import requests
import scrapy

from final_spider.items import SportteryResult


class ResultSpider(scrapy.Spider):
    name = 'result'
    allowed_domains = ['sporttery.cn']
    start_urls = ['https://www.liangqiujiang.com/api/internal/getWaitSportteries?manager=12345qwert']

    def parse(self, response):
        items = json.loads(response.body)['datalist']
        status = json.loads(response.body)['status']
        if status['code'] == 0:
            for i in items:
                targetId = i['target_id']
                infos = json.loads(requests.get('http://i.sporttery.cn/api/fb_match_info/get_pool_rs/?mid='
                                                + str(targetId)).text)
                ios = infos['result']
                status = infos['status']
                if status['code'] == 0:
                    pool_rs = ios['pool_rs']
                    # 确保有数据数据,无数据无需处理
                    if len(pool_rs) > 0:
                        type_id = 1
                        for i in pool_rs:
                            if i == 'crs':
                                type_id = 3
                            if i == 'had':
                                type_id = 1
                            if i == 'hafu':
                                type_id = 5
                            if i == 'hhad':
                                type_id = 2
                            if i == 'ttg':
                                type_id = 4
                            sc = SportteryResult()
                            sc['target_id'] = targetId
                            sc['type_id'] = type_id
                            sc['pool_rs'] = pool_rs[i]['pool_rs']
                            sc['prs_name'] = pool_rs[i]['prs_name']
                            sc['goalline'] = pool_rs[i]['goalline']
                            sc['single'] = pool_rs[i]['single']
                            sc['odds'] = pool_rs[i]['odds']
                            sc['description'] = type_id
                            yield sc
