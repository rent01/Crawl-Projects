'''
-*- coding: utf-8 -*-
@Author  : TY Ren
@Time    : 2021/10/9 9:20
@Software: PyCharm
@File    : Tianjin.py
'''
import time
import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote
from http import cookiejar
import pyodbc
import numpy as np

t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print('当前时间:',t)
t2 = time.time()
# print(int(t2))

connect = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=192.168.10.203;DATABASE=TY_Statistics;UID=sa;PWD=sjty_118sqlpass')
# connect = pyodbc.connect(
#     'DRIVER={SQL Server};SERVER=119.23.224.75;DATABASE=TY_Statistics;UID=sa;PWD=niceeasy2021!@#')
sql = "Select Name from YBJH_ArticleKey where type = '关键字'"
sql_bai = "Select Name from YBJH_ArticleKey where type = '白名单'"
sql_hei = "Select Name from YBJH_ArticleKey where type = '黑名单'"

kw = pd.read_sql(sql, connect)
bai = pd.read_sql(sql_bai, connect)
hei = pd.read_sql(sql_hei, connect)

input_key = kw["Name"]
input_bai = bai["Name"]
input_hei = hei["Name"]

# input_key = ['中介','保险兼业','保险代理','保险经纪','资格证']

for word in input_key:
    arr = []
    dic = []
    a = (str(word.encode("gbk")).replace("\\x","%")[2:-1])
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
               'Cookie': 'PHPSESSID=pqa78eqk26qeq8n18fq1jj95j4; Hm_lvt_b4ea5af7afceeead309aaea30a6a8ee9=1636360507,1636948487,1637831804; safedog-flow-item=CBC738CD0480A7D3C7B4B7011C1F9314; Hm_lpvt_b4ea5af7afceeead309aaea30a6a8ee9='+str(t2),
               'Host':'www.tjia.org.cn',
               'Referer': 'http://www.tjia.org.cn/'}

    url = 'http://www.tjia.org.cn/plus/search.php?q='+a
    print(url)

    res = requests.get(url,headers = headers)
    # res.encoding = 'utf-8'
    wb = BeautifulSoup(res.text,'html.parser')
    time.sleep(6)
    print(wb)

    # 定位文章”标题“
    article_title = re.findall('</span><a href="/a(.*?)</a></li>',str(wb))
    title_list = []
    # print(article_title)
    for paper in article_title:
        papername = paper.replace('</span><a href="/a','').split('</a></li>')[0].replace('<font color="red">','').replace('</font>','').split('>')[1]
        print(papername)
        title_list.append(papername)

    # # 文章“时间”
    article_time = re.findall('<li><span>.*?]</span>',str(wb))
    time_list = []
    # print(article_time)
    for uptime in article_time:
       publish = uptime.replace('</a></li><li><span>[','').replace('<li><span>[','').replace(']</span>','')
       print(publish)
       time_list.append(publish)

    # 文章”地址“
    article_url = re.findall('</span><a href="/(.*?)" target',str(wb))
    url_list = []
    content_list = []
    # print(article_url)
    for url in article_url:
        address = url.replace('</span><a href="/','').split('" target')[0]
        new_url = 'http://www.tjia.org.cn/'+str(address)
        url_list.append(new_url)
        print(new_url)

        cont = requests.get(new_url)
        cont.encoding = 'gbk'
        soup = BeautifulSoup(cont.text,'html.parser')
        content_list.append(str(soup))

    # 其他额外信息
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    web_name = '天津市保险行业协会'
    web_address = 'http://www.tjia.org.cn/'
    keywords = word

    #导出至表格
    for x, y, z, w in zip(title_list, time_list, url_list,content_list):
        li = [update_time, web_name, web_address, keywords, x, z, y, w]
        arr.append(li)

        new_key1 = "|".join(input_key)
        new_key2 = '|'.join(input_bai)
        new_key3 = '|'.join(input_hei)
        print("关：" + new_key1)
        print("白：" + new_key2)
        print("黑：" + new_key3)

        check_keywords = len(list(filter(None, list(set(re.findall(word, w))))))
        check_bai = len(list(filter(None, list(set(re.findall(new_key2, w))))))
        check_hei = len(list(filter(None, list(set(re.findall(new_key3, w))))))

        print(z)
        print(list(filter(None, list(set(re.findall(word, w))))))
        print(list(filter(None, list(set(re.findall(new_key2, w))))))
        print(list(filter(None, list(set(re.findall(new_key3, w))))))

        if check_keywords > 0:
            if check_hei > 0 and check_bai == 0:
                pass
            else:
                print(check_keywords)
                print(check_bai)
                print(check_hei)
                print("====分割线=====")
                dic.append(li)
    # print(dic)

                # connect = pyodbc.connect(
                #     'DRIVER={SQL Server};SERVER=119.23.224.75;DATABASE=TY_Statistics;UID=sa;PWD=niceeasy2021!@#')
                # if connect:
                #     print("连接成功!")
                # cur = connect.cursor()
                # sql = "INSERT INTO [TY_Statistics].[dbo].[YBJH_Articles]([UpdateTime],[WebName],[WebAddress],[Keywords],[ArticleName],[ArticleAddress],[PublishTime]) VALUES(?,?,?,?,?,?,?)"
                # cur.execute(sql, li)
                # connect.commit()
                # connect.close()
    try:
        connect = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=192.168.10.203;DATABASE=TY_Statistics;UID=sa;PWD=sjty_118sqlpass')
        # connect = pyodbc.connect(
        #     'DRIVER={SQL Server};SERVER=119.23.224.75;DATABASE=TY_Statistics;UID=sa;PWD=niceeasy2021!@#')
        if connect:
            print("连接成功!")
        cur = connect.cursor()
        sql = "INSERT INTO [TY_Statistics].[dbo].[YBJH_Articles]([UpdateTime],[WebName],[WebAddress],[Keywords],[ArticleName],[ArticleAddress],[PublishTime],[Content]) VALUES(?,?,?,?,?,?,?,?)"
        cur.executemany(sql, dic)
        connect.commit()
        connect.close()
    except:
        pass


                # df = pd.DataFrame(arr, columns=['爬取时间', '网站名称', '网站网址', '关键字','文章标题','文章链接','发布时间'])
                # df.to_excel('C:Users/Administrator/Desktop/天津保险行业协会-'+word+'.xlsx')