import scrapy
import json

from scrapy.selector import Selector

class NaraitemSpider(scrapy.Spider):
    name = 'naraitem'
    allowed_domains = ['catalog.archives.gov/id']
    base_url = 'https://catalog.archives.gov/OpaAPI/iapi/v1/id/'

    def start_requests(self):
        yield scrapy.Request(url=self.base_url+'30001', callback=self.parse)

    def parse(self, response):
        json_response = json.loads(response.text)
        html = Selector(text=json_response['opaResponse']['content']['description'])

        # Title
        title = json_response['opaResponse']['@title']

        # Additional Information
        info_column = [el.get() for el in html.css('div#additionalInfo span.text-right *::text')]

        info_data = []
        for i in range(len(info_column)):
            elements = html.css('div#additionalInfo tr:nth-child('+str(i+1)+') td:nth-child(2) *::text')
            data = [' '.join(el.get().split()) for el in elements]
            info_data.append(' '.join(data))
        
        # Details
        detail_column = [el.get() for el in html.css('div#details div.col-xs-4.text-right *::text')]

        detail_data = []
        for i in range(len(detail_column)):
            elements = html.css('div#details div.content-row:nth-child('+str(i+1)+') div.col-xs-8 *::text')
            data = [' '.join(el.get().split()) for el in elements]
            detail_data.append(' '.join(data))

        # Shot list
        shot_list = [el.get() for el in html.css('div#shotList span.text-left::text')]

        print(detail_data)
