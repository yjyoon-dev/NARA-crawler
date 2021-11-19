import scrapy
import json

from scrapy.selector import Selector
from nara.items import NaraItem

class ColumnSpider(scrapy.Spider):
    name = 'column'
    allowed_domains = ['catalog.archives.gov/id']
    base_url = 'https://catalog.archives.gov/OpaAPI/iapi/v1/id/'

    def start_requests(self):
        na_id = 1

        while True:
            if na_id % 100 == 0: print('Current ID: ', na_id)
            yield scrapy.Request(url=self.base_url+str(na_id), callback=self.parse)
            na_id += 1

    def parse(self, response):
        if response.status != 200: return
        
        json_response = json.loads(response.text)

        html = Selector(text=json_response['opaResponse']['content']['description'])

        info_columns = [el.get() for el in html.css('div#additionalInfo span.text-right *::text')]
        detail_columns = [el.get() for el in html.css('div#details div.col-xs-4.text-right *::text')]

        for column in info_columns:
            item = NaraItem()
            item['info_columns'] = column[:-1].replace('\n                           ','')
            yield item

        for column in detail_columns:
            item = NaraItem()
            item['detail_columns'] = column[:-1].replace('\n                           ','')
            yield item

    

