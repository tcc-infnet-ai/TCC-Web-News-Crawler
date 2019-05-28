# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

# Cleans up a text, removing undisired 'garbage' resulted of the crawling
def clean_text(text):
    if text is not None:
        # Replace the ISO 8859-1 blank space with a standard utf-8 blank space
        text = text.replace('\xa0', ' ')

        # Remove the line breaks from the string
        text = text.strip('\r\n').strip('\n')

        # Remove the extra white spaces from the string and cast it to upper case
        text = text.strip().upper()

        return text
    else:
        return text

# Pre process the news, cleanning and formatting all the data
def pre_process_news(news):
    clean_news = {
        'categories': [],
        'link': news['link'],
        'title': clean_text(news['title']),
        'sub_title': clean_text(news['sub_title']),
        'date_published': news['date_published'],
        'authors': [],
        'location': clean_text(news['location']), 
        'news_body': ''
    }
    for category in news['categories']:
        clean_news['categories'].append(clean_text(category))

    for author in news['authors'] :
        clean_news['authors'].append(clean_text(author))

    clean_paragraphs = []
    for paragrapgh in news['paragraphs']:
        clean_paragraph = clean_text(paragrapgh)

        if clean_paragraph != '':
            clean_paragraphs.append(clean_paragraph)
    
    clean_news['news_body'] = ' '.join(clean_paragraphs)
    
    return clean_news

class TccNewsCrawlerPipeline(object):
    def open_spider(self, spider):
        self.pre_processed_news = { 'news': [] }

    def close_spider(self, spider):
        file = open('folha_de_sao_paulo_news.json', 'w')
        json.dump(self.pre_processed_news, file)
        file.close()

    def process_item(self, item, spider):
        if 'blogfolha' in item['link']:
            raise DropItem("Blog item: %s" % item)
        else:
            pre_processed_item = pre_process_news(item)
            self.pre_processed_news['news'].append(pre_processed_item)

            return pre_processed_item