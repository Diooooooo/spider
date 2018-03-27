# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from final_spider.items import NewsItem


class NewsZhibo8Spider(scrapy.Spider):
    name = 'news_zhibo8'
    allowed_domains = ['http://news.zhibo8.cc']
    start_urls = ['https://news.zhibo8.cc/zuqiu/more.htm']

    def parse(self, response):
        i = 0
        provenances = ['马卡报', '独立报', '天空体育', '米兰体育报', '米兰新闻网', '每日邮报', '队报', '阿斯报', '曼彻斯特晚报', 'Goal.com', '世界体育报', '卫报']
        for r in response.xpath('//ul[@class="articleList"]/li'):
            if r.xpath('span[2]/text()').extract_first() in provenances and i < 100:
                i = i + 1
                yield Request(response.urljoin(r.xpath('span[1]/a/@href').extract_first()), self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        lesence = ['禁止转载', '转载请注明出处']
        news = NewsItem()
        news['title'] = response.xpath('//div[@class="title"]/h1/text()').extract_first()
        news['time'] = response.xpath('//div[@class="title"]/span/text()').extract_first()
        news['source'] = response.xpath('//div[@class="title"]/span/a[1]/text()').extract_first()
        news['st'] = response.xpath('//div[@class="title"]/span/a[2]/text()').extract_first()
        srContent = ''
        for sr in response.xpath('//div[@id="signals"]/p')[:-1]:
            srContent += sr.extract()
        if '直播吧' in srContent:
            srContent = srContent[0:246] + srContent[256:]

        news['content'] = srContent.replace('"', '\'').replace('直播吧', '')
        news['url'] = response.url
        news['description'] = None
        if response.xpath('//div[@id="signals"]/p[1]/img/@src'):
            if 'http' in response.xpath('//div[@id="signals"]/p[1]/img/@src').extract_first():
                news['img'] = response.xpath('//div[@id="signals"]/p[1]/img/@src').extract_first()
            else:
                news['img'] = response.xpath('//div[@id="signals"]/p[1]/img/@src').extract_first().replace('//', 'http://')
        else:
            news['img'] = response.xpath('//div[@id="signals"]/p[1]/img/@src').extract_first()

        saved = True
        for s in lesence:
            if s in news['content']:
                saved = False
                break

        if saved:
            yield news
