# -*- coding: utf-8 -*-
import scrapy
import re
from qyer.items import QyerItem

class QyerbotSpider(scrapy.Spider):
    name = "qyerbot"
    allowed_domains = ["qyer.com"]
    start_urls = (
        'http://place.qyer.com/',
    )

    def parse(self, response):
        for url in response.xpath('//li[@class="item"]/a/@href').extract():
            yield scrapy.Request(url + 'travel-notes/', callback=self.parse_links)

    def parse_links(self, response):
        country_name = self._extract_text(response, '//div[@class="clearfix"]/p/a/text()')[0]
        posts_count = int(re.findall('\"beentocounts\":(\d+)', response.body)[0])
        for url in self._extract_text(response, '//ul[@class="pla_travellist clearfix"]//h3//a/@href'):
            yield scrapy.Request(url,
                                 callback=self.parse_item,
                                 meta={'country_name': country_name, 'posts_count': posts_count})

    def parse_item(self, response):
        item = QyerItem()
        item['publish_time'] = response.xpath(
            '//*[@class="infos"]/text()').extract()[3].strip()[4:]
        print response.xpath('//*[@class="views"]/text()').extract()[0]
        item['view_count'] = self._int(
            response.xpath('//*[@class="views"]/text()').extract()[0])
        print response.xpath('//*[@class="sum"]/text()').extract()[0]
        item['comment_count'] = self._int(
            response.xpath('//*[@class="sum"]/text()').extract()[0])
        item['like_count'] = self._int(
            response.xpath('//*[@class="like"]/text()').extract()[0])
        item['text'] = ''.join(s.strip() for s in self._extract_text(
            response, '//*[@class="mainbox viewthread bbs_viewthread"]//*[not(self::script or self::style)]/text()'))
        item['country_name'] = response.meta['country_name']
        item['posts_count'] = response.meta['posts_count']
        yield item

    def _extract_text(self, response, query):
        return [s.strip() for s in response.xpath(query).extract()]

    def _int(self, string):
        if string.endswith(u'万'):
            return int(string[:-1]) * 10000
        else:
            return int(string)
