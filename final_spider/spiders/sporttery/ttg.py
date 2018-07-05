# -*- coding: utf-8 -*-
import json

import scrapy

from final_spider.items import SportteryItem, InfoItem, MatchInfoItem


class TtgSpider(scrapy.Spider):
    name = 'ttg'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://i.sporttery.cn/odds_calculator/get_odds?i_format=json&poolcode[]=ttg']

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
                if k == 'ttg':
                    ttg = InfoItem()
                    expand = ''
                    ttg['id'] = infos[i]['id']
                    for h in infos[i]['ttg']:
                        if h == 'p_code':
                            hcode = infos[i]['ttg'][h]
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
                            ttg['p_code'] = hcode
                            ttg['type_id'] = htypeId
                            continue
                        if h == 'goalline':
                            ttg['goalline'] = infos[i]['ttg'][h]
                            continue
                        if h == 'o_type':
                            ttg['o_type'] = infos[i]['ttg'][h]
                            continue
                        if h == 'p_id':
                            ttg['p_id'] = infos[i]['ttg'][h]
                            continue
                        if h == 'p_status':
                            ttg['p_status'] = infos[i]['ttg'][h]
                            continue
                        if h == 'single':
                            ttg['single'] = infos[i]['ttg'][h]
                            continue
                        if h == 'allup':
                            ttg['allup'] = infos[i]['ttg'][h]
                            continue
                        if h == 'fixedodds':
                            ttg['fixedodds'] = infos[i]['ttg'][h]
                            continue
                        if h == 'cbt':
                            ttg['cbt'] = infos[i]['ttg'][h]
                            continue
                        if h == 'int':
                            ttg['int'] = infos[i]['ttg'][h]
                            continue
                        if h == 'vbt':
                            ttg['vbt'] = infos[i]['ttg'][h]
                            continue
                        if h == 'h_trend':
                            ttg['h_trend'] = infos[i]['ttg'][h]
                            continue
                        if h == 'a_trend':
                            ttg['a_trend'] = infos[i]['ttg'][h]
                            continue
                        if h == 'd_trend':
                            ttg['d_trend'] = infos[i]['ttg'][h]
                            continue
                        if h == 'l_trend':
                            ttg['l_trend'] = infos[i]['ttg'][h]
                            continue
                        if h == 's0' or h == 's1' or h == 's2' or h == 's3' or h == 's4' \
                                or h == 's5' or h == 's6' or h == 's7':
                            expand += h + ':' + infos[i]['ttg'][h] + ','
                            continue
                    ttg['a'] = ''
                    ttg['d'] = ''
                    ttg['h'] = ''
                    ttg['expand'] = expand
                    yield ttg
            yield sporttery
