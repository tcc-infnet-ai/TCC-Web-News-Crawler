# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re

# Cleans up a text, removing undisired 'garbage' resulted of the crawling
def clean_text(text):
    if text is not None:
        # Replace the ISO 8859-1 blank space with a standard utf-8 blank space
        text = text.replace('\xa0', ' ')

        # Remove the line breaks from the string
        text = text.strip('\r\n').strip('\n')

        # Remove the extra white spaces from the string and cast it to lower case
        text = text.strip().lower()

        # Replace the single quotes with double quotes, avoiding the NLTK to think quotations are english words
        text = text.replace("'", '"')

        # Remove extra spaces
        text = text.replace('  ', ' ')

        return text
    else:
        return text


def clear_categories(categories):
    clean_categories = []
    # Clean all the category names
    for category in categories:
        clean_category = clean_text(category).replace(' ', '_')
        clean_categories.append(clean_category)
    
    return clean_categories

def clear_authors(authors):
    clean_authors = []

    # If there's no specified author, sets it to 'NO AUTHOR', else cleans up the authors
    if len(authors) == 0:
        clean_authors.append('NO AUTHOR')
    else:
        for author in authors :
            clean_authors.append(clean_text(author))
    
    return clean_authors

# Remove extra breaklines from the location, and then split it in different locations
def clear_location(location):
    clean_locations = []
    if(location is not None):
        
        # Separate the locations, using 'E', \n and ',' as delimiters
        separated_locations = re.sub(r'\bE\b', ',', clean_text(location)).replace('\n', ',').replace('|\n', ',').split(',')

        for separate_location in separated_locations:
            # If theres the state/country in a pattern ([accronimn]), remove it
            if separate_location.find('(') != -1:
                separate_location = separate_location[0:separate_location.find('(')]
            
            # Remove possible empty spaces from location options
            if(separate_location != ' ' and separate_location != '' and separate_location != '|'):
                formatted_location = clean_text(separate_location).replace(' ', '_')
                clean_locations.append(formatted_location)
    else:
        clean_locations.append('NO LOCATION')
    
    return clean_locations
    

def clear_news_body(paragraphs):
    # Cleans up the paragraphs of the text and then concatenate them
    clean_paragraphs = []
    for paragrapgh in paragraphs:
        clean_paragraph = clean_text(paragrapgh)

        if clean_paragraph != '':
            clean_paragraphs.append(clean_paragraph)
    
    return ' '.join(clean_paragraphs)

# Pre process the news, cleanning and formatting all the data
def pre_process_news(news):
    clean_news = {
        'categories': clear_categories(news['categories']),
        'link': news['link'],
        'title': clean_text(news['title']),
        'sub_title': clean_text(news['sub_title']),
        'date_published': news['date_published'],
        'authors': clear_authors(news['authors']),
        'locations': clear_location(news['location']), 
        'news_body': clear_news_body(news['paragraphs'])
    }

    return clean_news

class TccNewsCrawlerPipeline(object):
    def open_spider(self, spider):
        self.pre_processed_news = { 'news': [] }

    def close_spider(self, spider):
        file = open('folha_de_sao_paulo_news.json', 'w')
        json.dump(self.pre_processed_news, file)
        file.close()

    def process_item(self, item, spider):

        # Drops blog news as they have bias
        if 'blogfolha' in item['link']:
            raise DropItem("Blog item: %s" % item)
        else:
            pre_processed_item = pre_process_news(item)
            self.pre_processed_news['news'].append(pre_processed_item)

            return pre_processed_item