# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TccNewsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsBody(scrapy.Item):
    categories = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    sub_title = scrapy.Field()
    date_published = scrapy.Field()
    authors = scrapy.Field()
    location = scrapy.Field()
    paragraphs = scrapy.Field()