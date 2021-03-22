'''
Descripttion: 
version: 
Author: yeyu
Date: 2020-10-29 11:45:50
LastEditors: yeyu
LastEditTime: 2020-10-29 15:30:08
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WallhavenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    img_urls =  scrapy.Field()
    url = scrapy.Field()