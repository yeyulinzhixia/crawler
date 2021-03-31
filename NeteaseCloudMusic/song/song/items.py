'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-01-29 16:24:20
LastEditors: yeyu
LastEditTime: 2021-01-29 23:13:29
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    artists = scrapy.Field()
    al_id = scrapy.Field()
    al_name = scrapy.Field()
    al_type = scrapy.Field()
    al_company = scrapy.Field()
    al_picUrl = scrapy.Field()
    alias = scrapy.Field()
    fee = scrapy.Field()
    popularity = scrapy.Field()
    score = scrapy.Field()
    duration = scrapy.Field()
    transName = scrapy.Field()
    copyrightId = scrapy.Field()
    mvid = scrapy.Field()
    playTime = scrapy.Field()

class Song2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    ar = scrapy.Field()
    alia = scrapy.Field()
    pop = scrapy.Field()
    fee = scrapy.Field()
    v = scrapy.Field()
    al_id = scrapy.Field()
    al_name = scrapy.Field()
    al_picUrl = scrapy.Field()
    dt = scrapy.Field()
    cd = scrapy.Field()
    mark = scrapy.Field()
    mv = scrapy.Field()
    cp = scrapy.Field()
    publishTime = scrapy.Field()


