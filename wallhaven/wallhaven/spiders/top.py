'''
Descripttion: 
version: 
Author: yeyu
Date: 2020-10-29 11:47:41
LastEditors: yeyu
LastEditTime: 2020-10-29 23:09:41
'''
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from wallhaven.items import WallhavenItem
import logging
selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)
class TopSpider(scrapy.Spider):
    name = 'top'
    start_urls = ['https://wallhaven.cc/toplist?page=4']
    def parse(self, response):
        browser = webdriver.Chrome()
        for d in range(1,51):
            browser.get('https://wallhaven.cc/toplist?page=%d' % d)
            item  = WallhavenItem()
            item['url'] = 'https://wallhaven.cc/toplist?page=%d' % d
            item['id'] = d
            item['img_urls'] = []
            for i in range(1,25):
                a = browser.find_element_by_xpath('//*[@id="thumbs"]/section/ul/li[%d]/figure/a' % i)
                row_url = a.get_attribute('href')
                url = 'https://w.wallhaven.cc/full/'+row_url.split('/')[-1][:2]+'/wallhaven-'+row_url.split('/')[-1]+'.jpg'
                item['img_urls'].append(url)
            yield item
        