# -*- coding: utf-8 -*-
import json

import scrapy

from final_spider.items import SportteryItem, InfoItem, MatchInfoItem


class HafuSpider(scrapy.Spider):
    name = 'hafu'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://i.sporttery.cn/odds_calculator/get_odds?i_format=json&poolcode[]=hafu']

    def parse(self, response):
        infos = json.loads(response.body)['data']
        last = json.loads(response.body)['status']
        for i in infos:
            sporttery = SportteryItem()
            for k in infos[i]:
                if k == 'id':
                    sporttery['id'] = infos[i][k]
                    continue
                if k == 'num':
                    sporttery['week'] = infos[i][k][:2]
                    sporttery['num'] = infos[i][k][2:]
                    continue
                if k == 'date':
                    sporttery['date'] = infos[i][k]
                    continue
                if k == 'time':
                    sporttery['time'] = infos[i][k]
                    continue
                if k == 'b_date':
                    sporttery['b_date'] = infos[i][k]
                    continue
                if k == 'status':
                    status = infos[i][k]
                    sId = 2
                    if status == 'Selling':
                        sId = 2
                    elif status == '':
                        sId = 1
                    elif status == '':
                        sId = 3
                    elif status == '':
                        sId = 4
                    sporttery['status'] = sId
                    continue
                if k == 'hot':
                    sporttery['hot'] = infos[i][k]
                    continue
                if k == 'l_id':
                    sporttery['l_id'] = infos[i][k]
                    continue
                if k == 'l_cn':
                    sporttery['l_cn'] = infos[i][k]
                    continue
                if k == 'h_id':
                    sporttery['h_id'] = infos[i][k]
                    continue
                if k == 'h_cn':
                    sporttery['h_cn'] = infos[i][k]
                    continue
                if k == 'a_id':
                    sporttery['a_id'] = infos[i][k]
                    continue
                if k == 'a_cn':
                    sporttery['a_cn'] = infos[i][k]
                    continue
                if k == 'index_show':
                    sporttery['index_show'] = infos[i][k]
                    continue
                if k == 'show':
                    sporttery['show'] = infos[i][k]
                    continue
                if k == 'l_cn_abbr':
                    sporttery['l_cn_abbr'] = infos[i][k]
                    continue
                if k == 'h_cn_abbr':
                    sporttery['h_cn_abbr'] = infos[i][k]
                    continue
                if k == 'a_cn_abbr':
                    sporttery['a_cn_abbr'] = infos[i][k]
                    continue
                if k == 'h_order':
                    sporttery['h_order'] = infos[i][k]
                    continue
                if k == 'a_order':
                    sporttery['a_order'] = infos[i][k]
                    continue
                if k == 'h_id_dc':
                    sporttery['h_id_dc'] = infos[i][k]
                    continue
                if k == 'a_id_dc':
                    sporttery['a_id_dc'] = infos[i][k]
                    continue
                if k == 'l_background_color':
                    sporttery['l_background_color'] = infos[i][k]
                    continue
                if k == 'weather':
                    sporttery['weather'] = infos[i][k]
                    continue
                if k == 'weather_city':
                    sporttery['weather_city'] = infos[i][k]
                    continue
                if k == 'temperature':
                    sporttery['temperature'] = infos[i][k]
                    continue
                if k == 'weather_pic':
                    if infos[i]['weather_pic']:
                        sporttery['weather_pic'] = 'http://qsr-app.oss-cn-shenzhen.aliyuncs.com/weather/' + infos[i][k][51:]
                    continue
                sporttery['last_updated'] = last['last_updated']
                if k == 'hafu':
                    hafu = InfoItem()
                    expand = ''
                    hafu['id'] = infos[i]['id']
                    for h in infos[i]['hafu']:
                        if h == 'p_code':
                            hcode = infos[i]['hafu'][h]
                            htypeId = 1
                            if hcode == 'HAD':
                                htypeId = 1
                            elif hcode == 'HHAD':
                                htypeId = 2
                            elif hcode == 'CRS':
                                htypeId = 3
                            elif hcode == 'TTG':
                                htypeId = 4
                            elif hcode == 'HAFU':
                                htypeId = 5
                            elif hcode == 'UNSEL':
                                htypeId = 6
                            elif hcode == 'SEL':
                                htypeId = 7
                            hafu['p_code'] = hcode
                            hafu['type_id'] = htypeId
                            continue
                        if h == 'goalline':
                            hafu['goalline'] = infos[i]['hafu'][h]
                            continue
                        if h == 'o_type':
                            hafu['o_type'] = infos[i]['hafu'][h]
                            continue
                        if h == 'p_id':
                            hafu['p_id'] = infos[i]['hafu'][h]
                            continue
                        if h == 'p_status':
                            hafu['p_status'] = infos[i]['hafu'][h]
                            continue
                        if h == 'single':
                            hafu['single'] = infos[i]['hafu'][h]
                            continue
                        if h == 'allup':
                            hafu['allup'] = infos[i]['hafu'][h]
                            continue
                        if h == 'fixedodds':
                            hafu['fixedodds'] = infos[i]['hafu'][h]
                            continue
                        if h == 'cbt':
                            hafu['cbt'] = infos[i]['hafu'][h]
                            continue
                        if h == 'int':
                            hafu['int'] = infos[i]['hafu'][h]
                            continue
                        if h == 'vbt':
                            hafu['vbt'] = infos[i]['hafu'][h]
                            continue
                        if h == 'h_trend':
                            hafu['h_trend'] = infos[i]['hafu'][h]
                            continue
                        if h == 'a_trend':
                            hafu['a_trend'] = infos[i]['hafu'][h]
                            continue
                        if h == 'd_trend':
                            hafu['d_trend'] = infos[i]['hafu'][h]
                            continue
                        if h == 'l_trend':
                            hafu['l_trend'] = infos[i]['hafu'][h]
                            continue
                        if h == 'aa' or h == 'ad' or h == 'ah' or h == 'da' or h == 'dd' \
                                or h == 'dh' or h == 'ha' or h == 'hd' or h == 'hh':
                            expand += h + ':' + infos[i]['hafu'][h] + ','
                            continue
                    hafu['a'] = ''
                    hafu['d'] = ''
                    hafu['h'] = ''
                    hafu['expand'] = expand
                    yield hafu
            try:
                if not sporttery['weather_pic']:
                    sporttery['weather_pic'] = ''
            except KeyError:
                sporttery['weather_pic'] = ''
            yield sporttery
