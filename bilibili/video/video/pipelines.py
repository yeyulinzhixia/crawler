'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-02-14 16:39:08
LastEditors: yeyu
LastEditTime: 2021-02-17 18:20:59
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class MysqlPipeline:
    def __init__(self, mysql_host, mysql_port, mysql_user,mysql_password, mysql_db, mysql_charset):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db
        self.mysql_charset = mysql_charset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_db=crawler.settings.get('MYSQL_DB'),
            mysql_charset=crawler.settings.get('MYSQL_CHARSET'),
        )

    def open_spider(self, spider):
        self.connection = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user,
                                          password=self.mysql_password, db=self.mysql_db, charset=self.mysql_charset)
        self.cursor = self.connection.cursor()

    def process_item(self, items, spider):
        if len(items['data'])!=0:
            insert1 = ('%s,' * len(items['data'][0]))[:-1]
            insert2 = ",".join(['video.' + i for i in dict(items['data'][0]).keys()])
            sql = 'INSERT INTO video (' + insert2 + ') VALUES (' + insert1 + ')'
            try:
                self.cursor.executemany(sql, [list(i.values()) for i in items['data']])
                self.connection.commit()
                return items
            except Exception as e:
                print(e)
                self.cursor.rollback()
                raise DropItem("插入失败")
                

    def close_spider(self, spider):
        self.cursor.close()

