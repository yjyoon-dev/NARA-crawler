import scrapy
import json

from scrapy.selector import Selector
from nara.items import NaraItem

class SectionSpider(scrapy.Spider):
    name = 'section'
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
        
        sections = [' '.join(el.get().split()) for el in html.css('div.panel-heading span.panel-title a::text')]

        for section in sections:
            item = NaraItem()
            item['sections'] = section
            yield item
