'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-02-14 16:39:08
LastEditors: yeyu
LastEditTime: 2021-02-17 18:13:58
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class DataItem(scrapy.Item):
    data = scrapy.Field()

class VideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    aid = scrapy.Field()
    videos = scrapy.Field()
    tid = scrapy.Field()
    tname = scrapy.Field()
    copyright = scrapy.Field()
    pic = scrapy.Field()
    title = scrapy.Field()
    pubdate = scrapy.Field()
    ctime = scrapy.Field()
    desc = scrapy.Field()
    state = scrapy.Field()
    duration = scrapy.Field()
    owner_mid = scrapy.Field()
    owner_name = scrapy.Field()
    owner_face = scrapy.Field()
    view = scrapy.Field()
    danmaku = scrapy.Field()
    reply = scrapy.Field()
    favorite = scrapy.Field()
    coin = scrapy.Field()
    share = scrapy.Field()
    now_rank = scrapy.Field()
    his_rank = scrapy.Field()
    like = scrapy.Field()
    dislike = scrapy.Field()
    dislike = scrapy.Field()
    cid = scrapy.Field()
    dimension_width = scrapy.Field()
    dimension_height = scrapy.Field()
    dimension_rotate = scrapy.Field()
    bvid = scrapy.Field()
    dynamic = scrapy.Field()
    crawltime = scrapy.Field()

