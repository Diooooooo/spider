# -*- coding: utf-8 -*-
import scrapy

from final_spider.items import LottoResult


class PailieFiveSpider(scrapy.Spider):
    name = 'pailie5'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18189',
                  'http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18188',
                  'http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18187',
                  'http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18186',
                  'http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18185',
                  'http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18184',
                  'http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18183',
                  'http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18182',
                  'http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18181',
                  'http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18180',
                  'http://info.sporttery.cn/digital/dlt.php?&type=6&issue=18179']

    def parse(self, response):
        letou_kj = response.xpath('//div[@class="letou_kj"]')
        a = str.strip(letou_kj.xpath('h2/text()').extract_first()[1:7])
        if a == response.url[55:]:
            lotto = LottoResult()
            lotto['no'] = a
            lotto['type_id'] = 4
            lotto['date'] = str(response.xpath('//div[@class="letou_ttop"]')[0].xpath('text()')[0].extract()[5:])\
                .replace('年', '-').replace('月', '-').replace('日', '')
            lotto['plan'] = ''
            lotto['sale'] = str.strip(response.xpath('//div[@class="letou_ttop"]/b')[0].xpath('text()')[0].extract())
            lotto['serial'] = ''
            lotto['number'] = str(response.xpath('//div[@class="letou_ttop"]/div')[0].xpath('span/text()')[0]
                                  .extract()).replace('    ', ',')
            s = response.xpath('//div[@class="letou_kj"]/table/tr')
            lotto['prize'] = s[len(s) - 1].xpath('td')[3].xpath('b')[0].xpath('text()')[0].extract()[:-2]
            yield lotto
