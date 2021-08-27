'''
-*- coding: utf-8 -*-
@Author  : TY Ren
@Time    : 2021/8/27 12:09
@Software: PyCharm
@File    : pdf.py
'''
import pandas as pd
import pdfkit

data = pd.read_excel(r'C:\Users\Administrator\Desktop\SaaS白夜行.xlsx')
urls = data['链接']
name = data['标题']
for i in range(len(urls)):
    try:
        path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        pdfkit.from_url(urls[i],'C:/Users/Administrator/Desktop/SaaS白夜行/'+name[i]+'.pdf',configuration=config)
    except:
        pass

