import scrapy
import json

from scrapy.selector import Selector

from nara.items import NaraItem

class NaraitemSpider(scrapy.Spider):
    name = 'naraitem'
    allowed_domains = ['catalog.archives.gov/id']
    base_url = 'https://catalog.archives.gov/OpaAPI/iapi/v1/id/'

    # Columns which need to be crawled
    columns = [
        'Local Identifier:',
        'Creator(s):',
        'From:',
        'Level of Description:',
        'Type(s) of Archival Materials:',
        'The creator compiled or maintained the series between:',
        'Use Restriction(s):',
        'Access Restriction(s):'
    ]

    special_chars = '():'

    def start_requests(self):
        na_id = 1

        while na_id <= 100000:
            if na_id % 100 == 0: print('Current ID: ', na_id)
            yield scrapy.Request(url=self.base_url+str(na_id), callback=self.parse)
            na_id += 1

    def parse(self, response):
        if response.status != 200: return

        json_response = json.loads(response.text)
        html = Selector(text=json_response['opaResponse']['content']['description'])

        item = NaraItem()

        # Natianl Archives Identifier
        naid = json_response['opaResponse']['@naId']
        item['NAID'] = naid

        # URL
        url = 'https://catalog.archives.gov/id/' + naid
        item['URL'] = url

        # Title
        title = json_response['opaResponse']['@title']
        item['Title'] = title

        # Additional Information
        info_column = [el.get() for el in html.css('div#additionalInfo span.text-right *::text')]

        info_data = {}

        for i in range(len(info_column)):
            elements = html.css('div#additionalInfo tr:nth-child('+str(i+1)+') td:nth-child(2) *::text')
            data = [' '.join(el.get().split()) for el in elements]
            info_data[info_column[i]] = ' '.join(data)
        
        for column in NaraitemSpider.columns:
            if column in info_data:
                value = info_data[column]
                column = ''.join(c for c in column if c not in NaraitemSpider.special_chars)
                column = column.replace(' ','_')
                item[column] = value

        # Details
        detail_column = [el.get() for el in html.css('div#details div.col-xs-4.text-right *::text')]

        detail_data = {}

        for i in range(len(detail_column)):
            elements = html.css('div#details div.content-row:nth-child('+str(i+1)+') div.col-xs-8 *::text')
            data = [' '.join(el.get().split()) for el in elements]
            detail_data[detail_column[i]] = ' '.join(data)

        for column in NaraitemSpider.columns:
            if column in detail_data:
                value = detail_data[column]
                column = ''.join(c for c in column if c not in NaraitemSpider.special_chars)
                column = column.replace(' ','_')
                item[column] = value

        # Shot list
        shot_list = [el.get() for el in html.css('div#shotList span.text-left::text')]
        if len(shot_list) > 0: item['Shot_List'] = shot_list[0]

        # Scope & Content
        scope_content = [el.get() for el in html.css('div#scopeContent span.text-left::text')]
        if len(scope_content) > 0: item['Scope_and_Content'] = scope_content[0]

        yield item
