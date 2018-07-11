# -*- coding: utf-8 -*-
import json

import scrapy

from final_spider.items import SportteryItem, InfoItem, MatchInfoItem


class GlobalSpider(scrapy.Spider):
    name = 'global'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://i.sporttery.cn/odds_calculator/get_odds?i_format=json&poolcode[]=hhad'
                  '&poolcode[]=had&poolcode[]=hafu&poolcode[]=crs&poolcode[]=ttg']

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
                        sporttery['weather_pic'] = 'http://qsr-app.oss-cn-shenzhen.aliyuncs.com/weather/' \
                                                   + infos[i]['weather_pic'][51:]
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
            try:
                if not sporttery['weather_pic']:
                    sporttery['weather_pic'] = ''
            except KeyError:
                sporttery['weather_pic'] = ''
            yield sporttery
