'''
Descripttion: 
version: 
Author: yeyu
Date: 2020-10-29 11:45:50
LastEditors: yeyu
LastEditTime: 2020-10-29 19:39:21
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
import logging
import scrapy
from scrapy.utils.project import get_project_settings
import os
import datetime

class WallhavenPipeline(ImagesPipeline):
    EXPIRES = 0
    #bookmark
    def get_media_requests(self, item, info):
        logging.warning(item)
        for url in item['img_urls']:
            yield scrapy.Request(url = url,meta={'item':item,'download_timeout':20})
    #bookmark
    def file_path(self, request, response=None, info=None):
        logging.warning(request.url)
        if os.path.isdir('C:/Users/WXL/Desktop/test/'+datetime.date.today().strftime('%y_%m_%d'))==False:
            os.mkdir('C:/Users/WXL/Desktop/test/'+datetime.date.today().strftime('%y_%m_%d'))
        return datetime.date.today().strftime('%y_%m_%d')+'/'+os.path.basename(urlparse(request.url).path)
