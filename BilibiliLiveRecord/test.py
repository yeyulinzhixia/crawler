'''
Descripttion: 
version: 
Author: yeyu
Date: 2021-03-15 22:15:29
LastEditors: yeyu
LastEditTime: 2021-03-15 22:24:11
'''
import requests
import json
import time
import subprocess
import os
import threading
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

#直播间信息
id = 3110168
live_status = 0
i = 1
while live_status==0:
    response = requests.get("https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id=" + str(id),
                            headers = headers, timeout = 10)
    live_status = json.loads(response.text)['data']['room_info']['live_status']
    if live_status==1:
        #流信息
        stream_response = requests.get("https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl?platform=web&quality=0&cid=" + str(id), 
                                headers = headers, timeout = 10)
        #流地址
        url = json.loads(stream_response.text)['data']['durl'][0]['url']
        cmd = "ffmpeg -headers \"User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0\" -i \"{}\" -c copy \"test{}.flv\"".format(url,i)
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE, stdin = subprocess.PIPE, shell=True,encoding='gbk')
        while True:
            if p.poll()==0:
                print('shutdown')
                live_status = 0
                i+=1
                break
    time.sleep(1)