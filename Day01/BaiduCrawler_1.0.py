#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/18/21 9:32 下午
# @Author  : Haodi Wang
# @FileName: BaiduCrawler_1.0.py
# @Software: PyCharm
# @contact: whdi@foxmail.com
#           whd@seu.edu.cn

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def convert_url(url):
    resp = requests.get(url=url,
                        headers=headers,
                        allow_redirects=False
                        )
    return resp.headers['Location']

def get_url(wd, num):
    s = requests.session()
    total_title = []
    total_url = []
    total_info = []
    num = num * 10 - 10
    for i in range(-10, num, 10):
        url = 'https://www.baidu.com/s'
        params = {
            "wd": wd,
            "pn": i,
        }
        r = s.get(url=url, headers=headers, params=params)
        print("返回状态码:", r.status_code)
        soup = BeautifulSoup(r.text, 'lxml')
        for so in soup.select('#content_left .t a'):
            g_url = convert_url(so.get('href'))
            g_title = so.get_text().replace('\n', '').strip()
            print(g_title, g_url)
            total_title += [g_title]
            total_url += [g_url]
        time.sleep(1 + (i / 10))
        print("当前页码：", (i + 10) / 10 + 1)
    try:
        total_info = zip(total_title, total_url)
        df = pd.DataFrame(data=total_info, columns=['标题', 'Url'])
        df.to_csv('BaiduCrawler.csv', index=False, encoding='utf_8_sig')
        print("保存成功")
    except:
        return 'FALSE'


if __name__ == '__main__':
    # while True:  # 循环
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0",
        "Host": "www.baidu.com",
    }
    wd = input("输入搜索内容：")
    num = int(input("输入页数："))
    get_url(wd, num)
