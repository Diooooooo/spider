# -*- coding: utf-8 -*-
import scrapy

from final_spider.items import LottoResult


class LottoSpider(scrapy.Spider):
    name = 'lotto'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18080',
                  'http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18079',
                  'http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18078',
                  'http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18077',
                  'http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18076',
                  'http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18075',
                  'http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18074',
                  'http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18073',
                  'http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18072',
                  'http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18071',
                  'http://info.sporttery.cn/digital/dlt.php?&type=1&issue=18070']

    def parse(self, response):
        letou_kj = response.xpath('//div[@class="letou_kj"]')
        a = str.strip(letou_kj.xpath('h2/text()').extract_first()[1:7])
        if a == response.url[55:]:
            lotto = LottoResult()
            lotto['no'] = a
            lotto['type_id'] = 1
            lotto['date'] = str(response.xpath('//div[@class="letou_ttop"]')[0].xpath('text()')[0].extract()[5:])\
                .replace('年', '-').replace('月', '-').replace('日', '')
            lotto['plan'] = response.xpath('//div[@class="letou_ttop"]/b')[1].xpath('text()')[0].extract()
            lotto['sale'] = str.strip(response.xpath('//div[@class="letou_ttop"]/b')[0].xpath('text()')[0].extract())
            lotto['serial'] = str(response.xpath('//div[@class="letou_ttop"]/div')[1].xpath('span/text()')[0]
                                  .extract()).replace('    ', ',') + '-' \
                              + str(response.xpath('//div[@class="letou_ttop"]/div')[1].xpath('span/text()')[1]
                                    .extract()).replace('    ', ',')
            lotto['number'] = str(response.xpath('//div[@class="letou_ttop"]/div')[2].xpath('span/text()')[0]
                                  .extract()).replace('    ', ',') + '-' \
                              + str(response.xpath('//div[@class="letou_ttop"]/div')[2].xpath('span/text()')[1]
                                    .extract()).replace('    ', ',')
            s = response.xpath('//div[@class="letou_kj"]/table/tr')
            lotto['prize'] = s[len(s) - 1].xpath('td')[3].xpath('b')[0].xpath('text()')[0].extract()[:-2]
            yield lotto
