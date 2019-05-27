# -*- coding: utf-8 -*-
import scrapy


class G1Spider(scrapy.Spider):
    name = 'G1'
    allowed_domains = ['g1.globo.com']
    start_urls = ['http://g1.globo.com/']

    def parse(self, response):
        pass
