'''
-*- coding: utf-8 -*-
@Author  : TY Ren
@Time    : 2021/10/12 16:36
@Software: PyCharm
@File    : Shenzhen_Insurance.py
'''
import time
import requests
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote
import pyodbc
import lxml
import numpy as np

t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print('当前时间:',t)

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

# input_key = ['中介','保险代理']

for word in input_key:
    arr = []
    dic = []
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '72',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'HWWAFSESID=b0ff1739e548b08578; HWWAFSESTIME=1637828642922; 32a9272417d7420a83f7931456ffe009=WyIyMzI1MjE3MDgwIl0',
    'Host': 'www.szia.org.cn',
    'Origin': 'https://www.szia.org.cn',
    'Referer': 'https://www.szia.org.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-mobile': "'?0",
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin'}

    url = 'https://www.szia.org.cn/guild-website-api/search/queryResultList.do'
    data = {'queryData': word, 'pagesize': 10, 'currentPage': 1}

    res = requests.post(url,data = data,headers = headers, verify= False)
    res.encoding = 'utf-8'
    wb = BeautifulSoup(res.text,'lxml')
    time.sleep(3)
    # print(wb)

    # 定位文章”标题“
    article_title = re.findall('"title":"(.*?)","publishTime":',str(wb))
    title_list = []
    # print(article_title)
    for paper in article_title:
        papername = paper.replace('"title":"','').split('","publishTime":')[0]
        print(papername)
        title_list.append(papername)

    # 文章“时间”
    article_time = re.findall('"publishTime":".*?digest":null',str(wb))
    time_list = []
    # print(article_time)
    for uptime in article_time:
       publish = uptime.replace('"publishTime":"','').split('"digest":null,')[0].split('","')[0]
       print(publish)
       time_list.append(publish)

    # 文章”地址“
    article_url = re.findall('"contentId":".*?","title":"',str(wb))
    url_list = []
    content_list = []
    # print(article_url)
    for url in article_url:
        address = url.replace('"contentId":"','').split('","title":"')[0]
        new_url = r'https://www.szia.org.cn/#/newsDetails?parentName=%E6%96%B0%E9%97%BB%E4%B8%AD%E5%BF%83&crumbsTitle=%E7%9B%91%E7%AE%A1%E4%BF%A1%E6%81%AF&id='+str(address)
        url_list.append(new_url)
        # print(new_url)

        new2 = 'https://www.szia.org.cn/guild-website-api/newsCenter/queryNewsInfoById.do'
        headers = {"Cookie": "HWWAFSESID=b0ff1739e548b08578; HWWAFSESTIME=1637828642922; 32a9272417d7420a83f7931456ffe009=WyIxNzMxMzc2NDIiXQ",
                   "Host": "www.szia.org.cn",
                   "Origin": "https://www.szia.org.cn",
                   "Referer": "https://www.szia.org.cn/",
                   "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}
        data2 = {"id": str(address)}
        cont = requests.post(new2, headers= headers,data = data2)
        cont.encoding = 'utf-8'
        soup = BeautifulSoup(cont.text,'lxml')
        content_list.append(str(soup))
        # print(soup)


    # 其他额外信息
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    web_name = '深圳市保险行业协会'
    web_address = 'https://www.szia.org.cn/'
    keywords = word

    #导出至表格
    for x,y,z,w in zip(title_list,time_list,url_list,content_list):
        li = [update_time, web_name, web_address, keywords, x, z, y, w]
        arr.append(li)

                # connect = pyodbc.connect(
                #     'DRIVER={SQL Server};SERVER=119.23.224.75;DATABASE=TY_Statistics;UID=sa;PWD=niceeasy2021!@#')
                # if connect:
                #     print("连接成功!")
                # cur = connect.cursor()
                # sql = "INSERT INTO [TY_Statistics].[dbo].[YBJH_Articles]([UpdateTime],[WebName],[WebAddress],[Keywords],[ArticleName],[ArticleAddress],[PublishTime]) VALUES(?,?,?,?,?,?,?)"
                # cur.execute(sql, li)
                # connect.commit()
                # connect.close()

        new_key1 = "|".join(input_key)
        new_key2 = '|'.join(input_bai)
        new_key3 = '|'.join(input_hei)
        print("关："+new_key1)
        print("白："+new_key2)
        print("黑："+new_key3)

        check_keywords = len(list(filter(None,list(set(re.findall(word, w))))))
        check_bai = len(list(filter(None,list(set(re.findall(new_key2, w))))))
        check_hei = len(list(filter(None,list(set(re.findall(new_key3, w))))))

        print(z)
        print(list(filter(None,list(set(re.findall(word, w))))))
        print(list(filter(None,list(set(re.findall(new_key2, w))))))
        print(list(filter(None,list(set(re.findall(new_key3, w))))))

        if check_keywords > 0:
            if check_hei > 0 and check_bai == 0:
                pass
            else:
                print('当前搜索关键字:'+word)
                print(check_keywords)
                print(check_bai)
                print(check_hei)
                print("====分割线=====")
                dic.append(li)

    try:
        connect = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=192.168.10.203;DATABASE=TY_Statistics;UID=sa;PWD=sjty_118sqlpass')
        # connect = pyodbc.connect(
        #     'DRIVER={SQL Server};SERVER=119.23.224.75;DATABASE=TY_Statistics;UID=sa;PWD=niceeasy2021!@#')
        if connect:
            print("连接成功!")
        cur = connect.cursor()
        sql = "INSERT INTO [TY_Statistics].[dbo].[YBJH_Articles]([UpdateTime],[WebName],[WebAddress],[Keywords],[ArticleName],[ArticleAddress],[PublishTime],[Content]) VALUES(?,?,?,?,?,?,?,?)"
        cur.executemany(sql,dic)
        connect.commit()
        connect.close()
    except:
        pass

        # df = pd.DataFrame(arr, columns=['爬取时间', '网站名称', '网站网址','关键字','文章标题','文章链接','发布时间'])
        # print(df["文章链接"])
        # df.to_excel('C:Users/Administrator/Desktop/深圳市保险行业协会-'+word+'.xlsx')

# =========================导出方法2============================#
# df = pd.DataFrame(arr, columns=['爬取时间', '网站名称', '网站网址','文章标题','文章链接','发布时间'])
# df['关键字'] = keywords
# df.to_excel('C:Users/Administrator/Desktop/吉林省保险行业协会-'+word+'.xlsx')
