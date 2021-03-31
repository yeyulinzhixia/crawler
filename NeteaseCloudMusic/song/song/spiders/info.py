'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-01-29 16:24:46
LastEditors: yeyu
LastEditTime: 2021-03-31 20:52:32
'''
import scrapy
from song.items import SongItem
import json

class InfoSpider(scrapy.Spider):
    name = 'info'
    allowed_domains = ['music.163.com']
    flag = True
    start = 100000
    def start_requests(self):
        while(self.flag):
            s = self.start
            e = self.start+200
            ids = [i for i in range(s,e)]
            param = {'c':str(ids),'ids':str(ids)}
            url  = 'https://music.163.com/api/song/detail'
            yield scrapy.FormRequest(url,formdata = param,headers={'Referer':'http://music.163.com/'})
            self.start+=200
        
    def parse(self, response):
        print((json.loads(response.text))['code'])
        self.flag = bool(len((json.loads(response.text))['songs']))
        if self.flag:
            for data in (json.loads(response.text))['songs']:
                item = SongItem()
                for i in item.fields.keys():
                    if i=='artists':
                        if len(data[i])!=0:
                            item[i] = '\n'.join([j['name']+','+str(j['id']) for j in data[i]])
                    elif i=='playTime':
                        if data['lMusic']!=None:
                            item[i] = data['lMusic'][i]
                        elif data['mMusic']!=None: 
                            item[i] = data['mMusic'][i]
                        elif data['hMusic']!=None: 
                            item[i] = data['hMusic'][i]
                        elif data['bMusic']!=None: 
                            item[i] = data['bMusic'][i]
                    elif i.startswith('al_'):
                        if data['album'][i[3:]]!=None:
                            item[i] = data['album'][i[3:]]
                    elif i in data.keys():
                        if type(data[i])==list:
                            if len(data[i])!=0:
                                item[i] = ','.join(data[i])
                        else:
                            if data[i]!=None:
                                item[i] = data[i]
                yield item
