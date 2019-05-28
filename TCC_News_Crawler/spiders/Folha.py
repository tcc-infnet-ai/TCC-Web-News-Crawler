# -*- coding: utf-8 -*-
import scrapy
from TCC_News_Crawler.items import NewsBody

# This Spider is going to crawl for news related to the Bolsonaro's government in Folha de São Paulo newspaper
class FolhaSpider(scrapy.Spider):
    name = 'Folha'
    allowed_domains = ['folha.uol.com.br']
    # Looking for news related to Bolsonaro's government
    start_urls = ['https://search.folha.uol.com.br/search?q=governo+bolsonaro&periodo=personalizado&sd=01%2F07%2F2018&ed=28%2F05%2F2019&site=sitefolha&site%5B%5D=online%2Fpaineldoleitor&site%5B%5D=online%2Fdinheiro&site%5B%5D=online%2Fmundo']

    # Main parse function which crawls the first page to get the list of the news links
    def parse(self, response):
        # Get's the other news
        for article in response.css("ol.c-search li.c-headline--newslist"):
            link = article.css("div.c-headline__content a::attr(href)").extract_first()

            yield response.follow(link, self.parse_news_body)

        next_page = response.css('nav.c-pagination ul.c-pagination__list li.c-pagination__arrow:last-child a::attr(href)').extract_first()
        
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    # Parse function of the news individual page. This one get's the news detailed information
    def parse_news_body(self, response):
        link           = response.url
        categories     = response.css("header.l-header div.l-header__nav nav.c-site-nav__group ul.c-site-nav__list li.c-site-nav__item a::text").extract()
        title          = response.css("header.c-content-head div.c-content-head__wrap h1.c-content-head__title::text").extract_first()
        sub_title      = response.css("header.c-content-head div.c-content-head__wrap h2.c-content-head__subtitle::text").extract_first()
        date_published = response.css("article div.c-more-options div.c-more-options__header time.c-more-options__published-date::attr(datetime)").extract_first()
        authors        = response.css("article div.c-news__wrap div.c-signature strong.c-signature__author::text").extract()
        location       = response.css("article div.c-news__content div.c-signature strong.c-signature__location::text").extract_first()
        paragraphs     = response.css("article div.c-news__content div.c-news__body p::text").extract()

        newsBody = NewsBody(
            categories = categories,
            link = link,
            title = title,
            sub_title = sub_title,
            date_published = date_published,
            authors = authors,
            location = location,
            paragraphs = paragraphs
        )
        yield newsBody

