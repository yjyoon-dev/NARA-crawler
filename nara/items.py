# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NaraItem(scrapy.Item):
    info_columns = scrapy.Field();
    detail_columns = scrapy.Field();