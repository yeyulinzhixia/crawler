# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import logging
import os
from urllib.parse import urlparse
from scrapy.utils.project import get_project_settings
import datetime
class PixivPipeline(ImagesPipeline):

    EXPIRES = 0

    def get_media_requests(self, item, info):
        for i in item['img_urls']:
            yield scrapy.Request(i,headers={'Referer': 'https://www.pixiv.net/artworks/'+item['id']},meta={'item':item,'download_timeout':300})
    #bookmark
    def file_path(self, request, response=None, info=None):
        logging.warning(os.path.basename(urlparse(request.url).path))
        return os.path.basename(urlparse(request.url).path)

    # #rank_list
    # def file_path(self, request, response=None, info=None):
    #     logging.warning('test/'+datetime.date.today().strftime('%y_%m_%d')+(str)(request['meta']['rank']) +'_'+os.path.basename(urlparse(request.url).path))
    #     return 'test/'+datetime.date.today().strftime('%y_%m_%d')+(str)(request['meta']['rank']) +'_'+os.path.basename(urlparse(request.url).path)
