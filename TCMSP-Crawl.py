'''
-*- coding: utf-8 -*-
@Author  : TY Ren
@Time    : 2021/8/12 9:58
@Software: PyCharm
@File    : TestRequest.py
'''

import requests
import re
import time
import json
import pandas as pd
from lxml import html
from lxml import etree
from bs4 import BeautifulSoup


#导入文档，处理url,请求header
df1=pd.read_excel(r'C:\Users\Administrator\Desktop\TCMSP全.xlsx',sheet_name='All Herbs')
name = df1['Latin name']
n = 0
for i in name:
    n += 1
    print(i,n)
    try:
        url ='https://old.tcmsp-e.com/tcmspsearch.php?qr='+i+'&qsr=herb_en_name&token=aa2a36e4dcbbf97b8e86bf24df9efec1'
        print(url)
        # for i in range(1,25):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
               'Cookie':'_ga=GA1.1.95170299.1627889797; Hm_lvt_045f99afbec668d057769af796f1ed4f=1627869359; Hm_lvt_045f99afbec668d057769af796f1ed4f=1627869359,1629873218; Hm_lpvt_045f99afbec668d057769af796f1ed4f=1629873218; PHPSESSID=qjhvupnu38fvqsvc1pqeuc3bf7; PHPTCM=qjhvupnu38fvqsvc1pqeuc3bf7; _ga_Y7GC5FHYTY=GS1.1.1629939617.43.1.1629939885.0; Hm_lpvt_045f99afbec668d057769af796f1ed4f=1629939886',
               'Host': 'old.tcmsp-e.com'}
        time.sleep(8)
        res = requests.get(url,headers=headers, verify=False)
        wb = BeautifulSoup(res.text,'lxml')
        # print(wb)
        p1= 'data:(.*)'
        # 以下代码因为eval将string转化为list报错，使用null
        print(eval(re.findall(p1,str(wb))[1].replace(' ', '').replace('null', '""')))
        # 以下注释的代码为正常代码：
        # data = eval(re.findall(p1,str(wb))[1])
        data = eval(re.findall(p1,str(wb))[1].replace(' ', '').replace('null', '""'))

        df = pd.DataFrame(data[0])
        df['nm'] = i
        df.to_excel('C:/Users/Administrator/Desktop/新建文件夹/'+i+'.xlsx')
    except:
        pass









































