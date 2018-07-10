# -*- coding: utf-8 -*-
import scrapy

from final_spider.items import LottoResult, LottoResultItem


class QiXingCaiSpider(scrapy.Spider):
    name = 'qixingcai'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18080',
                  'http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18079',
                  'http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18078',
                  'http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18077',
                  'http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18076',
                  'http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18075',
                  'http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18074',
                  'http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18073',
                  'http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18072',
                  'http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18071',
                  'http://info.sporttery.cn/digital/dlt.php?&type=2&issue=18070']

    def parse(self, response):
        letou_kj = response.xpath('//div[@class="letou_kj"]')
        a = str.strip(letou_kj.xpath('h2/text()').extract_first()[1:7])
        if a == response.url[55:]:
            lotto = LottoResult()
            lotto['no'] = a
            lotto['type_id'] = 2
            lotto['date'] = str(response.xpath('//div[@class="letou_ttop"]')[0].xpath('text()')[0].extract()[5:])\
                .replace('年', '-').replace('月', '-').replace('日', '')
            lotto['plan'] = ''
            lotto['sale'] = str.strip(response.xpath('//div[@class="letou_ttop"]/b')[0].xpath('text()')[0].extract())
            lotto['serial'] = ''
            lotto['number'] = str(response.xpath('//div[@class="letou_ttop"]/div')[0].xpath('span/text()')[0]
                                  .extract()).replace('    ', ',')
            s = response.xpath('//div[@class="letou_kj"]/table/tr')
            lotto['prize'] = s[len(s) - 1].xpath('td')[3].xpath('b')[0].xpath('text()')[0].extract()[:-2]
            for tr in response.xpath('//div[@class="letou_kj"]/table/tr')[1:-1]:
                item = LottoResultItem()
                item['lt_id'] = 2
                item['no'] = a
                item['type_id'] = 1
                item['level'] = tr.xpath('td')[0].xpath('text()')[0].extract()
                item['count'] = tr.xpath('td')[1].xpath('text()')[0].extract()[:-2]
                item['prize'] = tr.xpath('td')[2].xpath('text()')[0].extract()[:-2]
                item['description'] = ''
                yield item
            yield lotto
