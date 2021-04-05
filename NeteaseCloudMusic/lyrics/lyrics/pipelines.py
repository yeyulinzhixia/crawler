'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-03-13 08:53:02
LastEditors: yeyu
LastEditTime: 2021-04-05 23:15:01
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class LyricsPipeline:

    def process_item(self, item, spider):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["netease"]
        mycol = mydb["lyrics"]
        data = item['data']

        if mycol.find({'id':data['id']}).count():
            mycol.delete_many({'id':data['id']})
        else:
            mycol.insert_one(data)
        return item

