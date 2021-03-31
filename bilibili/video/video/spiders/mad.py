'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-02-14 16:39:58
LastEditors: yeyu
LastEditTime: 2021-02-17 18:19:42
'''
#  -*- coding: UTF-8 -*
import datetime
import time
from urllib.parse import urlencode

import scrapy
import json
import requests
from video.items import VideoItem,DataItem

class MadSpider(scrapy.Spider):
    name = 'mad'
    allowed_domains = ['bilibili.com']
    start_urls = ['http://bilibili.com/']
    error_count = 0
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_requests(self):
        api = 'https://api.bilibili.com/x/web-interface/newlist'
        params = {'rid': 24, 'type': 0, 'pn': 1, 'ps': 20}
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/88.0.4324.150 Safari/537.36',
                   'referer': 'https://www.bilibili.com/'}
        response = requests.get(api, headers=headers, params=params, timeout=30)
        pages = json.loads(response.text)['data']['page']['count'] // 50 + 1
        for page in [i for i in range(pages)]:
            params['ps'] = 50
            params['pn'] = page + 1
            p = urlencode(params)
            yield scrapy.Request(api + '?' + p, dont_filter=True, callback=self.parse,
                                 headers={'referer': 'https://www.bilibili.com/'})

    def parse(self, response):
        # ip过期检查
        if response.status == 412:
            self.crawler.engine.close_spider(self, 'ip已被禁用')
        if json.loads(response.text)['code'] != 0:
            self.error_count += 1
            if self.error_count > 3:
                self.crawler.engine.close_spider(self, 'ip已被禁用')
            else:
                return

        timeout_count = 0
        alldata = DataItem()
        alldata['data'] = []
        for data in json.loads(response.text)['data']['archives']:
            # 爬取时间检查
            t = datetime.datetime.now() - datetime.timedelta(days=7)
            if data['ctime'] < int(time.mktime(t.timetuple())):
                timeout_count += 1
                continue
            item = VideoItem()
            for key in item.fields.keys():
                if key in data:
                    item[key] = data[key]
                elif key.startswith('owner_'):
                    item[key] = data['owner'][key[6:]]
                elif key.startswith('dimension_'):
                    item[key] = data['dimension'][key[10:]]
                elif key in data['stat'].keys():
                    item[key] = data['stat'][key]
                item['crawltime'] = self.time
            alldata['data'].append(item)
        if timeout_count == 50:
            self.crawler.engine.close_spider(self, '达到最远爬取距离')
        yield alldata
