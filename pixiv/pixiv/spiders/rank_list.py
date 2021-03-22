import scrapy
import logging
import json
from pixiv.items import PixivItem

class RankListSpider(scrapy.Spider):
    name = 'rank_list'
    start_urls = ['https://www.pixiv.net/ranking.php?mode=daily&p=%d&format=json' % i for i in range(1,11)]

    def read_cookie(self):
        with open("pixiv_cookies.txt", "r") as fp:
            cookies = json.load(fp)
        return cookies

    def start_requests(self):
        headers = {'referer':'https://www.pixiv.net/ranking.php?mode=daily'}
        cookies = self.read_cookie()
        for url in self.start_urls:
            yield scrapy.Request(url,self.parse,headers = headers,cookies=cookies,meta={'proxy':'http://121.235.184.29:8118'})

    def parse(self, response):
        rank_list = json.loads(response.text)['contents']
        for i in rank_list:
            item = PixivItem()
            item['id'] = (str)(i['illust_id'])
            item['rank'] = i['rank']
            referer = 'https://www.pixiv.net/artworks/'+item['id']
            url = 'https://www.pixiv.net/ajax/illust/'+item['id']+'/pages?lang=zh'
            headers = {'referer':referer}
            yield scrapy.Request(url,dont_filter=True,callback=self.img_parese,meta={'item':item},headers=headers)

    #ajax页
    def img_parese(self,response):
        img_list = json.loads(response.text)['body']
        url_list = []
        for  i in img_list:
            url_list.append(i['urls']['original'])
        item = response.meta['item']
        item['img_urls'] = url_list
        yield item
