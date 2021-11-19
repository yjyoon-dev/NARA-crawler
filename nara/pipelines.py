# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class NaraPipeline:
    columns = []

    def process_item(self, item, spider):
        if item in self.columns:
            raise DropItem('Already exists')
        else:
            self.columns.append(item)
            print(item, ' added!')
            return item
