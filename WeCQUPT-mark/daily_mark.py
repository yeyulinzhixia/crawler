# -*- coding:UTF-8 -*-
'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-01-24 14:12:23
LastEditors: yeyu
LastEditTime: 2021-03-22 20:07:58
'''
# coding=UTF-8
import requests
import datetime
import base64
import json

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class DailyMark():
    def __init__(self,name,xh,xb,openid,szdq,xxdz,ywjcqzbl,ywjchblj,xjzdywqzbl,twsfzc,ywytdzz,beizhu,email):
        self.name = name
        self.xh = xh
        self.xb =xb
        self.openid = openid
        self.szdq = szdq
        self.xxdz = xxdz
        self.ywjcqzbl = ywjcqzbl
        self.ywjchblj = ywjchblj
        self.xjzdywqzbl = xjzdywqzbl
        self.twsfzc = twsfzc
        self.ywytdzz = ywytdzz
        self.beizhu = beizhu
        #邮箱
        self.email =email
        self.headers = {
            'Host':'we.cqu.pt',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br'
            }

    def base(self,code):
        code = code.encode(encoding='UTF-8')
        str_url = base64.b64encode(code)
        mima=str(str_url,'utf-8')
        return mima

    def create_data(self):
        location= requests.get('https://apis.map.qq.com/jsapi?qt=geoc&addr='+self.szdq+self.xxdz).text
        location = json.loads(location)

        a = datetime.datetime.now()
        day = a.day-1
        hour = a.hour
        r = [ "s9ZS", "jQkB", "RuQM", "O0_L", "Buxf", "LepV", "Ec6w", "zPLD", "eZry", "QjBF", "XPB0", "zlTr", "YDr2", "Mfdu", "HSoi", "frhT", "GOdB", "AEN0", "zX0T", "wJg1", "fCmn", "SM3z", "2U5I", "LI3u", "3rAY", "aoa4", "Jf9u", "M69T", "XCea", "63gc", "6_Kf" ]
        u = [ "89KC", "pzTS", "wgte", "29_3", "GpdG", "FDYl", "vsE9", "SPJk", "_buC", "GPHN", "OKax", "_Kk4", "hYxa", "1BC5", "oBk_", "JgUW", "0CPR", "jlEh", "gBGg", "frS6", "4ads", "Iwfk", "TCgR", "wbjP" ]
        mrdkkey = r[day] + u[hour]

        timestamp = int(a.timestamp())

        row_data = {
            "name": self.name,
            "xh":self.xh,
            "xb": self.xb,
            "openid": self.openid,
            "szdq": self.szdq,
            "locationBig": self.szdq,
            "locationSmall": self.szdq+self.xxdz,
            "latitude": float(location['detail']['pointy']),
            "longitude": float(location['detail']['pointx']),
            "xxdz":self.xxdz,
            "ywjcqzbl": self.ywjcqzbl,
            "ywjchblj": self.ywjchblj,
            "xjzdywqzbl": self.xjzdywqzbl,
            "twsfzc": self.twsfzc,
            "ywytdzz": self.ywytdzz,
            "beizhu": self.beizhu,
            "mrdkkey": mrdkkey,
            "timestamp": timestamp
        }
        encode_data='{"key": "' + self.base(json.dumps(row_data,ensure_ascii=False)) + '"}'
        return encode_data

    def sent_email(self,info):
        from_addr='479892367@qq.com'   #邮件发送账号
        to_addrs=self.email   #接收邮件账号
        qqCode='kcacswpawzlecahi'   #授权码（这个要填自己获取到的）
        smtp_server='smtp.qq.com'#固定写死
        smtp_port=465#固定端口

        #配置服务器
        stmp=smtplib.SMTP_SSL(smtp_server,smtp_port)
        stmp.login(from_addr,qqCode)

        #组装发送内容
        message = MIMEText(info, 'plain', 'utf-8')   #发送的内容
        message['From'] = Header("We重邮每日自动打卡", 'utf-8')   #发件人
        message['To'] = Header("self.name", 'utf-8')   #收件人
        subject = '今日打卡'
        message['Subject'] = Header(subject, 'utf-8')  #邮件标题

        try:
            stmp.sendmail(from_addr, to_addrs, message.as_string())
        except Exception as e:
            print ('邮件发送失败--' + str(e))
        print ('邮件发送成功')

    def check(self):
        url = 'https://we.cqu.pt/api/mrdk/get_mrdk_list_test.php'
        row_data={
            "openid":self.openid,
            "xh": self.xh,
            "timestamp":int( datetime.datetime.now().timestamp())
            }
        r = requests.post(url,data='{"key": "' + self.base(json.dumps(row_data,ensure_ascii=False)) + '"}',headers=self.headers,verify=False)
        check_info = ''
        for i in json.loads(r.text)['data']:
            check_info+='最近打卡时间:'+i['created_at']+'\n'
        return check_info

    def mark(self):
        url  = 'https://we.cqu.pt/api/mrdk/post_mrdk_info.php'
        status = 0
        count = 0
        while(status!=200 and count<3):
            r = requests.post(url,data=self.create_data(),headers=self.headers)
            status = json.loads(r.text)['status']
            if status==200:
                print("打卡成功")
                self.sent_email("打卡成功\n"+self.check())
                break
            else:
                count+=1
                print("打开失败{}次".format(count))
        if count==3:
            self.sent_email("今日打卡失败，请检查相关配置或联系管理员")

if __name__=='__main__':
    work = DailyMark("","","","","","","","","","","","","")
    work.mark()