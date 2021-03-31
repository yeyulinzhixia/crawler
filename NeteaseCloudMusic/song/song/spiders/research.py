'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-03-10 19:37:24
LastEditors: yeyu
LastEditTime: 2021-03-31 20:53:06
'''
import scrapy
import scrapy
from song.items import Song2Item
import json
import execjs
import logging
import  numpy as np
import pymysql

class ResearchSpider(scrapy.Spider):
    name = 'research'
    allowed_domains = ['163.com']
    start_urls = ['http://163.com/']
    js = open('/root/Music163.js', 'r').read()
    ext = execjs.compile(js)
    retry=0
    
    def start_requests(self):
        connection = pymysql.connect(host='localhost', port=3306, user='', password='',db='',charset='utf8')
        cursor = connection.cursor()
        sql = "select * from song2 order by id desc limit 100 "
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        start = int(np.mean([i[0] for i in result]))-2000000
        for _ in range(500):
            s = start
            e = start+1000
            ids = [i for i in range(s,e)]
            query = {"c":str([{'id':i} for i in ids]),'ids':str(ids)}
            param = self.ext.call('start',query)
            url = 'https://music.163.com/weapi/v3/song/detail'
            yield scrapy.FormRequest(url,formdata = param,headers={'Referer':'https://music.163.com/'})
            start+=1000
            logging.info("开始：{}，结束{}".format(s,e))

    def parse(self, response):
        try:
            non_count = 0
            if (json.loads(response.text))['code']==200:
                for data in (json.loads(response.text))['songs']:
                    item = Song2Item()
                    if data['name']==None or data['name']=='':
                        non_count+=1
                    else:
                        for i in item.fields.keys():
                            if i=='ar':
                                if len(data[i])!=0 and data[i]!=None:
                                    item[i] = '\n'.join([j['name']+','+str(j['id']) for j in data[i]])
                            elif i.startswith('al_'):
                                if data['al'][i[3:]]!=None:
                                    item[i] = data['al'][i[3:]]
                            elif i in data.keys():
                                if type(data[i])==list:
                                    if len(data[i])!=0:
                                        item[i] = ','.join(data[i])
                                else:
                                    if data[i]!=None:
                                        item[i] = data[i]
                        yield item
            if len((json.loads(response.text))['songs'])==non_count:
                self.retry+=1
            else:
                self.retry=0
            logging.info('retry次数')
            logging.info(self.retry)
        except:
            self.retry+=1
            logging.warning(response.text)
        if self.retry>50:
            self.crawler.engine.close_spider(self,'爬取出错')
