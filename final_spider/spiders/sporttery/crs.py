# -*- coding: utf-8 -*-
import json

import scrapy

from final_spider.items import SportteryItem, InfoItem, MatchInfoItem


class CrsSpider(scrapy.Spider):
    name = 'crs'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://i.sporttery.cn/odds_calculator/get_odds?i_format=json&poolcode[]=crs']

    def parse(self, response):
        infos = json.loads(response.body)['data']
        last = json.loads(response.body)['status']
        for i in infos:
            sporttery = SportteryItem()
            for k in infos[i]:
                if k == 'id':
                    sporttery['id'] = infos[i]['id']
                    continue
                if k == 'num':
                    sporttery['week'] = infos[i]['num'][:2]
                    sporttery['num'] = infos[i]['num'][2:]
                    continue
                if k == 'date':
                    sporttery['date'] = infos[i]['date']
                    continue
                if k == 'time':
                    sporttery['time'] = infos[i]['time']
                    continue
                if k == 'b_date':
                    sporttery['b_date'] = infos[i]['b_date']
                    continue
                if k == 'status':
                    status = infos[i]['status']
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
                    sporttery['hot'] = infos[i]['hot']
                    continue
                if k == 'l_id':
                    sporttery['l_id'] = infos[i]['l_id']
                    continue
                if k == 'l_cn':
                    sporttery['l_cn'] = infos[i]['l_cn']
                    continue
                if k == 'h_id':
                    sporttery['h_id'] = infos[i]['h_id']
                    continue
                if k == 'h_cn':
                    sporttery['h_cn'] = infos[i]['h_cn']
                    continue
                if k == 'a_id':
                    sporttery['a_id'] = infos[i]['a_id']
                    continue
                if k == 'a_cn':
                    sporttery['a_cn'] = infos[i]['a_cn']
                    continue
                if k == 'index_show':
                    sporttery['index_show'] = infos[i]['index_show']
                    continue
                if k == 'show':
                    sporttery['show'] = infos[i]['show']
                    continue
                if k == 'l_cn_abbr':
                    sporttery['l_cn_abbr'] = infos[i]['l_cn_abbr']
                    continue
                if k == 'h_cn_abbr':
                    sporttery['h_cn_abbr'] = infos[i]['h_cn_abbr']
                    continue
                if k == 'a_cn_abbr':
                    sporttery['a_cn_abbr'] = infos[i]['a_cn_abbr']
                    continue
                if k == 'h_order':
                    sporttery['h_order'] = infos[i]['h_order']
                    continue
                if k == 'a_order':
                    sporttery['a_order'] = infos[i]['a_order']
                    continue
                if k == 'h_id_dc':
                    sporttery['h_id_dc'] = infos[i]['h_id_dc']
                    continue
                if k == 'a_id_dc':
                    sporttery['a_id_dc'] = infos[i]['a_id_dc']
                    continue
                if k == 'l_background_color':
                    sporttery['l_background_color'] = infos[i]['l_background_color']
                    continue
                if k == 'weather':
                    sporttery['weather'] = infos[i]['weather']
                    continue
                if k == 'weather_city':
                    sporttery['weather_city'] = infos[i]['weather_city']
                    continue
                if k == 'temperature':
                    sporttery['temperature'] = infos[i]['temperature']
                    continue
                if k == 'weather_pic':
                    if infos[i]['weather_pic']:
                        sporttery['weather_pic'] = 'http://qsr-app.oss-cn-shenzhen.aliyuncs.com/weather/' + infos[i]['weather_pic'][51:]
                    continue
                sporttery['last_updated'] = last['last_updated']
                if k == 'crs':
                    crs = InfoItem()
                    expand = ''
                    crs['id'] = infos[i]['id']
                    for h in infos[i]['crs']:
                        if h == 'p_code':
                            hcode = infos[i]['crs']['p_code']
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
                            crs['p_code'] = hcode
                            crs['type_id'] = htypeId
                            continue
                        if h == 'goalline':
                            crs['goalline'] = infos[i]['crs']['goalline']
                            continue
                        if h == 'o_type':
                            crs['o_type'] = infos[i]['crs']['o_type']
                            continue
                        if h == 'p_id':
                            crs['p_id'] = infos[i]['crs']['p_id']
                            continue
                        if h == 'p_status':
                            crs['p_status'] = infos[i]['crs']['p_status']
                            continue
                        if h == 'single':
                            crs['single'] = infos[i]['crs']['single']
                            continue
                        if h == 'allup':
                            crs['allup'] = infos[i]['crs']['allup']
                            continue
                        if h == 'fixedodds':
                            crs['fixedodds'] = infos[i]['crs']['fixedodds']
                            continue
                        if h == 'cbt':
                            crs['cbt'] = infos[i]['crs']['cbt']
                            continue
                        if h == 'int':
                            crs['int'] = infos[i]['crs']['int']
                            continue
                        if h == 'vbt':
                            crs['vbt'] = infos[i]['crs']['vbt']
                            continue
                        if h == 'h_trend':
                            crs['h_trend'] = infos[i]['crs']['h_trend']
                            continue
                        if h == 'a_trend':
                            crs['a_trend'] = infos[i]['crs']['a_trend']
                            continue
                        if h == 'd_trend':
                            crs['d_trend'] = infos[i]['crs']['d_trend']
                            continue
                        if h == 'l_trend':
                            crs['l_trend'] = infos[i]['crs']['l_trend']
                            continue
                        if h == '0000' or h == '0001' or h == '0002' \
                                or h == '0003' or h == '0004' or h == '0005' or h == '0100' or h == '0101' \
                                or h == '0102' or h == '0103' or h == '0104' or h == '0105' or h == '0200' \
                                or h == '0201' or h == '0202' or h == '0203' or h == '0204' or h == '0205' \
                                or h == '0300' or h == '0301' or h == '0302' or h == '0303' or h == '0400' \
                                or h == '0401' or h == '0402' or h == '0500' or h == '0501' or h == '0502':
                            expand += h + ':' + infos[i]['crs'][h] + ','
                            continue
                        if h == '-1-a':
                            crs['a'] = infos[i]['crs'][h]
                        if h == '-1-d':
                            crs['d'] = infos[i]['crs'][h]
                        if h == '-1-h':
                            crs['h'] = infos[i]['crs'][h]
                    crs['expand'] = expand
                    yield crs
            yield sporttery
