'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-03-15 22:24:32
LastEditors: yeyu
LastEditTime: 2021-03-16 09:27:02
'''
import requests
import json
import time
import subprocess
import os
import threading
import time
from fake_useragent import UserAgent

class stream:
    def __init__(self,room_id):
        self.id = room_id
        #setting quality
        self.qn = 10000
        
    def islive(self):
        headers={'user-agent': UserAgent().random}
        response = requests.get("https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id=" + str(self.id),
                            headers = headers, timeout = 10)
        live_status = json.loads(response.text)['data']['room_info']['live_status']

        return live_status
    
    def loop(self):
        while True:
            if self.islive():
                self.save()
            time.sleep(1)
            print('尝试ing')
    
    def save(self):
        file_name  = str(self.id)+time.strftime("-%Y-%m-%d-%H-%M-%S",time.localtime())+".flv"
        #流信息
        headers={'user-agent': UserAgent().random}
        stream_response = requests.get(f"https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl?platform=web&quality=0&qn={self.qn}&cid={self.id}" , 
                                headers = headers, timeout = 10)
        url = json.loads(stream_response.text)['data']['durl'][0]['url']
        cmd = "ffmpeg -headers \"User-Agent: {}\" -i \"{}\" -c copy \"{}\"".format(UserAgent().random ,url, file_name)
        print(cmd)
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE, stdin = subprocess.PIPE, shell=True,encoding='gbk')
        while True:
            if p.poll()==0:
                break

room_id = input()
stream(room_id).loop()



