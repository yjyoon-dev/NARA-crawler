import os
from urllib.parse import urlparse
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class ImageFilesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return request.url.split('/')[5] + '/' + os.path.basename(urlparse(request.url).path)