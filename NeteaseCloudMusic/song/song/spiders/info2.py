'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-01-29 23:29:37
LastEditors: yeyu
LastEditTime: 2021-03-10 19:37:31
'''
import scrapy
from song.items import Song2Item
import json
import execjs

class Info2Spider(scrapy.Spider):
    name = 'info2'
    allowed_domains = ['music.163.com']
    flag = True
    start = 30210799
    retry = 0
    js = open('/root/Music163.js', 'r').read()
    ext = execjs.compile(js)
    #每天增长歌曲数100000内
        #   1814040574
        #   1815969450
    def start_requests(self):
        if self.retry>5:
            self.flag=False
        while(self.flag):
            s = self.start
            e = self.start+1000
            ids = [i for i in range(s,e)]
            query = {"c":str([{'id':i} for i in ids]),'ids':str(ids)}
            param = self.ext.call('start',query)
            url = 'https://music.163.com/weapi/v3/song/detail'
            # param ={"c":str([{'id':i} for i in ids]),'ids':str(ids)}
            # url  = 'https://music.163.com/api/v3/song/detail'
            
            yield scrapy.FormRequest(url,formdata = param,headers={'Referer':'https://music.163.com/'})
            self.start+=1000
            print(self.start)

    def parse(self, response):
        try:
            non_count = 0
            if bool(len((json.loads(response.text))['songs']))==False:
                return
            else:
                self.retry=0
            if self.flag and (json.loads(response.text))['code']==200:
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
                print(self.retry)
                self.retry+=1
            else:
                self.retry=0
        except:
            print(response.text)
