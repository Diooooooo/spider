# -*- coding: utf-8 -*-
import json

import scrapy

from final_spider.items import SportteryItem, InfoItem, MatchInfoItem


class HhadAndHadSpider(scrapy.Spider):
    name = 'hhad_had'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://i.sporttery.cn/odds_calculator/get_odds?i_format=json&poolcode[]=hhad&poolcode[]=had']

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
                if k == 'hhad':
                    Hhad = InfoItem()
                    for hh in infos[i]['hhad']:
                        if hh == 'p_code':
                            code = infos[i]['hhad']['p_code']
                            typeId = 1
                            if code == 'HAD':
                                typeId = 1
                            elif code == 'HHAD':
                                typeId = 2
                            elif code == 'CRS':
                                typeId = 3
                            elif code == 'TTG':
                                typeId = 4
                            elif code == 'HAFU':
                                typeId = 5
                            elif code == 'UNSEL':
                                typeId = 6
                            elif code == 'SEL':
                                typeId = 7
                            Hhad['p_code'] = code
                            Hhad['type_id'] = typeId
                            continue
                        Hhad['id'] = infos[i]['id']
                        if hh == 'a':
                            Hhad['a'] = infos[i]['hhad']['a']
                            continue
                        if hh == 'd':
                            Hhad['d'] = infos[i]['hhad']['d']
                            continue
                        if hh == 'h':
                            Hhad['h'] = infos[i]['hhad']['h']
                            continue
                        if hh == 'goalline':
                            Hhad['goalline'] = infos[i]['hhad']['goalline']
                            continue
                        if hh == 'o_type':
                            Hhad['o_type'] = infos[i]['hhad']['o_type']
                            continue
                        if hh == 'p_id':
                            Hhad['p_id'] = infos[i]['hhad']['p_id']
                            continue
                        if hh == 'p_status':
                            Hhad['p_status'] = infos[i]['hhad']['p_status']
                            continue
                        if hh == 'single':
                            Hhad['single'] = infos[i]['hhad']['single']
                            continue
                        if hh == 'allup':
                            Hhad['allup'] = infos[i]['hhad']['allup']
                            continue
                        if hh == 'fixedodds':
                            Hhad['fixedodds'] = infos[i]['hhad']['fixedodds']
                            continue
                        if hh == 'cbt':
                            Hhad['cbt'] = infos[i]['hhad']['cbt']
                            continue
                        if hh == 'int':
                            Hhad['int'] = infos[i]['hhad']['int']
                            continue
                        if hh == 'vbt':
                            Hhad['vbt'] = infos[i]['hhad']['vbt']
                            continue
                        if hh == 'h_trend':
                            Hhad['h_trend'] = infos[i]['hhad']['h_trend']
                            continue
                        if hh == 'a_trend':
                            Hhad['a_trend'] = infos[i]['hhad']['a_trend']
                            continue
                        if hh == 'd_trend':
                            Hhad['d_trend'] = infos[i]['hhad']['d_trend']
                            continue
                        if hh == 'l_trend':
                            Hhad['l_trend'] = infos[i]['hhad']['l_trend']
                            continue
                    Hhad['expand'] = ''
                    yield Hhad
                if k == 'had':
                    had = InfoItem()
                    for h in infos[i]['had']:
                        if h == 'p_code':
                            hcode = infos[i]['had']['p_code']
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
                            had['p_code'] = hcode
                            had['type_id'] = htypeId
                            continue
                        had['id'] = infos[i]['id']
                        if h == 'a':
                            had['a'] = infos[i]['had']['a']
                            continue
                        if h == 'd':
                            had['d'] = infos[i]['had']['d']
                            continue
                        if h == 'h':
                            had['h'] = infos[i]['had']['h']
                            continue
                        if h == 'goalline':
                            had['goalline'] = infos[i]['had']['goalline']
                            continue
                        if h == 'o_type':
                            had['o_type'] = infos[i]['had']['o_type']
                            continue
                        if h == 'p_id':
                            had['p_id'] = infos[i]['had']['p_id']
                            continue
                        if h == 'p_status':
                            had['p_status'] = infos[i]['had']['p_status']
                            continue
                        if h == 'single':
                            had['single'] = infos[i]['had']['single']
                            continue
                        if h == 'allup':
                            had['allup'] = infos[i]['had']['allup']
                            continue
                        if h == 'fixedodds':
                            had['fixedodds'] = infos[i]['had']['fixedodds']
                            continue
                        if h == 'cbt':
                            had['cbt'] = infos[i]['had']['cbt']
                            continue
                        if h == 'int':
                            had['int'] = infos[i]['had']['int']
                            continue
                        if h == 'vbt':
                            had['vbt'] = infos[i]['had']['vbt']
                            continue
                        if h == 'h_trend':
                            had['h_trend'] = infos[i]['had']['h_trend']
                            continue
                        if h == 'a_trend':
                            had['a_trend'] = infos[i]['had']['a_trend']
                            continue
                        if h == 'd_trend':
                            had['d_trend'] = infos[i]['had']['d_trend']
                            continue
                        if h == 'l_trend':
                            had['l_trend'] = infos[i]['had']['l_trend']
                            continue
                    had['expand'] = ''
                    yield had
                if k == 'match_info':
                    for m in range(len(infos[i]['match_info'])):
                        match = MatchInfoItem()
                        for mk in infos[i]['match_info'][m]:
                            if mk == 'id':
                                match['id'] = infos[i]['match_info'][0]['id']
                                continue
                            if mk == 'm_id':
                                match['m_id'] = infos[i]['match_info'][0]['m_id']
                                continue
                            if mk == 'i_id':
                                match['i_id'] = infos[i]['match_info'][0]['i_id']
                                continue
                            if mk == 'prompt':
                                match['prompt'] = infos[i]['match_info'][0]['prompt']
                                continue
                            if mk == 'checked':
                                match['checked'] = infos[i]['match_info'][0]['checked']
                                continue
                        yield match
            yield sporttery
