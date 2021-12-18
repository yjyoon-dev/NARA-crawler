# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NaraItem(scrapy.Item):
    NAID = scrapy.Field()
    URL = scrapy.Field()
    Title = scrapy.Field()
    Local_Identifier = scrapy.Field()
    Creators = scrapy.Field()
    From = scrapy.Field()
    Level_of_Description = scrapy.Field()
    Types_of_Archival_Materials = scrapy.Field()
    The_creator_compiled_or_maintained_the_series_between = scrapy.Field()
    Access_Restrictions = scrapy.Field()
    Use_Restrictions = scrapy.Field()
    Shot_List = scrapy.Field()
    Scope_and_Content = scrapy.Field()
    
    # Download images
    image_urls = scrapy.Field()
    images = scrapy.Field()
