# -*- coding: utf-8 -*-
import scrapy
from TCC_News_Crawler.items import NewsHeadline

class FolhaSpider(scrapy.Spider):
    name = 'Folha'
    allowed_domains = ['folha.uol.com.br']
    start_urls = ['https://www1.folha.uol.com.br/especial/2018/governo-bolsonaro/']

    def parse(self, response):
        for article in response.css("li.c-headline"):
            label          = article.css("div.c-headline__head h3.c-headline__kicker a::text").extract_first()
            link           = article.css("div.c-headline__content a::attr(href)").extract_first()
            title          = article.css("div.c-headline__content a h2.c-headline__title::text").extract_first()
            standFirst     = article.css("div.c-headline__content a p.c-headline__standfirst::text").extract_first()
            datePublished  = article.css("div.c-headline__content a time.c-headline__dateline::attr(datetime)").extract_first()

            newsHeadline = NewsHeadline(
                label = label, 
                link = link, 
                title = title, 
                standFirst = standFirst, 
                datePublished = datePublished
            )

            yield newsHeadline
