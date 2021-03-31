'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-03-13 08:55:14
LastEditors: yeyu
LastEditTime: 2021-03-31 20:51:35
'''
import scrapy

import execjs
import pymysql
import json
import re
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["netease"]
mycol = mydb["lyrics"]

class InfoSpider(scrapy.Spider):
    name = 'info'
    allowed_domains = ['163.com']
    start_urls = ['http://163.com/']

    def start_requests(self):
        connection = pymysql.connect(host='localhost', port=3306, user='', password='',db='',charset='utf8')
        cursor = connection.cursor()
        x = mycol.find_one()  
        if x==None:
            sql = "select id from song2 order by id limit 10000"
        else:
            sql = "select id from song2 where id >{} order by id limit 10000".format(x['id'])
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        url = 'https://music.163.com/api/song/lyric'
        for id in result:
            query ={'id':str(id[0]),'lv': '-1'}
            yield scrapy.FormRequest(url,formdata = query,headers={'Referer':'https://music.163.com/'},meta={'id':id[0]},callback=self.parse)
            
    def parse(self, response):
        result = json.loads(response.text)
        if 'uncollected' in result:
            return
        if 'nolyric' in result:
            return
        output = {}
        output['id'] = response.meta['id']
        return self.parse_lyrics(result['lrc']['lyric'],output)
    def parse_lyrics(self,text,output):
        for line in re.finditer('](.*)[:：](.*)\\n',text):
            if len(line.group(2))>8:
                continue
            k = line.group(1).strip()
            if len(k)>8:
                continue
            if text.count(k)>1 and k not in ['作词','作曲','编曲']:
                continue
            for v in re.split('[、/]',line.group(2)):
                if v.strip()!='':
                    output[k] = v.strip()
        if len(output)>1:
            mycol.insert_one(output)