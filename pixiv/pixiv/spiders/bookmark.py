'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-03-22 20:50:37
LastEditors: yeyu
LastEditTime: 2021-03-22 20:53:38
'''
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import json
import re
from pixiv.items import PixivItem

class BookmarkSpider(scrapy.Spider):
    name = 'bookmark'
    start_urls = ['https://www.pixiv.net/ajax/user/21405138/illusts/bookmarks?tag=&offset=0&limit=100&rest=show&lang=zh']
    
    def get_cookie(self):
        browser = webdriver.Chrome()
        browser.get('https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=pc&view_type=page')
        browser.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[1]/input').send_keys('479892367@qq.com')
        browser.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input').send_keys('13678475618zl')
        browser.find_element_by_xpath('//*[@id="LoginComponent"]/form/button').send_keys(Keys.ENTER)
        browser.get('https://www.pixiv.net/users/21405138/bookmarks/artworks')
        cookies = browser.get_cookies()
        browser.close()
        #保存cookies
        with open("pixiv_cookies.txt", "w") as fp:
            json.dump(cookies, fp)

    def read_cookie(self):
        with open("pixiv_cookies.txt", "r") as fp:
            cookies = json.load(fp)
        return cookies
  

    def start_requests(self):
        self.get_cookie()
        self.ck = self.read_cookie()
        for url in self.start_urls:
            yield scrapy.Request(url,dont_filter=True,cookies=self.ck)

    def parse(self, response):
        logging.warning("parse开始了")
        total = (json.loads(response.text)['body']['total'])
        pages = (int)(total/100)
        for i in range(pages):
            url = 'https://www.pixiv.net/ajax/user/21405138/illusts/bookmarks?tag=&offset=%d&limit=100&rest=show&lang=zh' % (i*100)
            yield scrapy.Request(url,dont_filter=True,cookies=self.ck,callback=self.bookmarks_list)

    def bookmarks_list(self, response):
        logging.warning("bookmarks_list开始了")
        bk_list = json.loads(response.text)['body']['works']
        for bk in bk_list:
            referer = 'https://www.pixiv.net/artworks/'+bk['illustId']
            item  = PixivItem()
            item['id'] = bk['illustId']
            url = 'https://www.pixiv.net/ajax/illust/'+item['id']+'/pages?lang=zh'
            headers = {'referer':referer}
            yield scrapy.Request(url,dont_filter=True,cookies=self.ck,callback=self.img_parese,meta={'item':item},headers=headers)

    #ajax页
    def img_parese(self,response):
        logging.warning("img_parese开始了")
        img_list = json.loads(response.text)['body']
        url_list = []
        for  i in img_list:
            url_list.append(i['urls']['original'])
        item = response.meta['item']
        item['img_urls'] = url_list
        yield item