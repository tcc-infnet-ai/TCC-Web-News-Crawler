# -*- coding: utf-8 -*-
import scrapy
from TCC_News_Crawler.items import NewsBody

# This Spider is going to crawl for news related to the Bolsonaro's government in Folha de São Paulo newspaper
class FolhaSpider(scrapy.Spider):
    name = 'Folha'
    allowed_domains = ['folha.uol.com.br']
    # Looking for news related to Bolsonaro's government
    start_urls = ['https://www1.folha.uol.com.br/especial/2018/governo-bolsonaro/']

    # Main parse function which crawls the first page to get the list of the news links
    def parse(self, response):

        # Get's the news that is highlighted in the front page
        highlightNewsLink = response.css("div.c-main-headline__wrapper a.c-main-headline__url::attr(href)").extract_first()
        yield response.follow(highlightNewsLink, self.parse_news_body)

        # Get's the other news
        for article in response.css("li.c-headline"):
            link = article.css("div.c-headline__content a::attr(href)").extract_first()

            yield response.follow(link, self.parse_news_body)

    # Parse function of the news individual page. This one get's the news detailed information
    def parse_news_body(self, response):
        link           = response.url
        label          = response.css("header.c-content-head div.c-content-head__wrap div.c-labels span.c-labels__item a::text").extract_first()
        title          = response.css("header.c-content-head div.c-content-head__wrap h1.c-content-head__title::text").extract_first()
        subTitle       = response.css("header.c-content-head div.c-content-head__wrap h2.c-content-head__subtitle::text").extract_first()
        datePublished  = response.css("div.c-more-options div.c-more-options__header time.c-more-options__published-date::attr(datetime)").extract_first()
        authors        = response.css("div.c-news__wrap div.c-signature strong.c-signature__author::text").extract()
        location       = response.css("div.c-news__content div.c-signature strong.c-signature__location::text").extract_first()
        newsText   =  "".join(response.css("div.c-news__body p::text").extract())

        newsBody = NewsBody(
            label = label,
            link = link,
            title = title,
            subTitle = subTitle,
            datePublished = datePublished,
            authors = authors,
            location = location,
            newsText = newsText
        )
        yield newsBody

