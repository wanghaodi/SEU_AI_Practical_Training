#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/18/21 9:18 下午
# @Author  : Haodi Wang
# @FileName: hw1.py
# @Software: PyCharm
# @contact: whdi@foxmail.com
#           whd@seu.edu.cn

import requests
import re
import xlwt

workbook = xlwt.Workbook(encoding = 'utf-8')#创建工作簿，编码格式utf-8
worksheet = workbook.add_sheet('sheet')#创建表格
worksheet.write(0,0,'category')#写入标签
worksheet.write(0,1,'name')
worksheet.write(0,2,'room')
worksheet.write(0,3,'hall')
worksheet.write(0,4,'toilet')
worksheet.write(0,5,'rent')
worksheet.write(0,6,'location')
worksheet.write(0,7,'price')
worksheet.write(0,8,'area')
worksheet.write(0,9,'dirction')
count = 1
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
cookies = {
    'cookie': 'global_cookie=ai01cplesuwl8l1nbpjcfrpio4ykipri3jy; city=sh; lastscanpage=0; new_search_uid=430e999c1521b72cf5f69a18b974f17f; newhouse_user_guid=B18A6281-B376-4139-2616-53B6D48932E3; csrfToken=ClhhX-HElCvsxISNU0ItpYef; __utma=147393320.2112072102.1608023219.1608052579.1608119578.6; __utmc=147393320; __utmz=147393320.1608119578.6.4.utmcsr=sh.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; newhouse_chat_guid=8A9B6410-E067-F252-1852-097B76499870; Captcha=305A394146676F43686A674861584576484F6635356F7032684C6E6A353832596775697678734C5157594F7677723767305771594A7373514F3555522F7636705869434C3231753769484D3D; g_sourcepage=esf_xq%5Elb_pc; unique_cookie=U_wk2r5fw8dvqmkq7jz7knbpllk3nkircvasy*6; __utmb=147393320.18.10.1608119578'
}
page = int(input('输入网页数量：'))
for i in range(1,page+1):
    url = 'http://sh.baletu.com/zhaofang/p{}c2o1a1/?seachId=0&is_rec_house=0&entrance=3&solr_house_cnt=2557'.format(i)
    res = requests.get(url,headers = head,cookies = cookies)
    html = res.text
    links = re.findall('<a target="_blank" href="http://sh.baletu.com/house/(.*?)" onclick="',html)[0::2]
    for link in links:
        link = 'http://sh.baletu.com/house/'+link
        res = requests.get(link,headers = head,cookies = cookies)
        if res.status_code != 200:#状态码，200即表示访问成功
            continue
        html = res.text
        infos = re.findall("<title>(.*?)-上海巴乐兔租房</title>",html)[0]
        name = infos.split('_')[1]
        type = infos.split('_')[2]
        hall = type[2]
        room = type[0]
        toilet = type[4]
        variant = infos.split('_')[3]
        rent_type = variant[0] + variant[1]
        if len(variant) != 2:
            list_str = list(variant)
            list_str.pop(1)
            list_str.pop(0)
            list_str = ''.join(list_str)
        else:
            list_str = ''
        location = infos.split('_')[4]
        category = infos.split('_')[0]
        price = re.findall('price="(.*?).00"',html)[0]
        area = re.findall('<li class="cent">(.*) <span>M²</span></li>',html)[0]
        worksheet.write(count, 0, category)
        worksheet.write(count, 1, name)
        worksheet.write(count, 2, room)
        worksheet.write(count, 3, hall)
        worksheet.write(count, 4, toilet)
        worksheet.write(count, 5, rent_type)
        worksheet.write(count, 6, location)
        worksheet.write(count, 7, price)
        worksheet.write(count, 8, area)
        worksheet.write(count, 9, list_str)
        count += 1

workbook.save('演示房源信息表.csv')
