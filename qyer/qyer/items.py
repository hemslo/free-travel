# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QyerItem(scrapy.Item):
    publish_time = scrapy.Field()
    view_count = scrapy.Field()
    comment_count = scrapy.Field()
    like_count = scrapy.Field()
    text = scrapy.Field()
    country_name = scrapy.Field()
    posts_count = scrapy.Field()

