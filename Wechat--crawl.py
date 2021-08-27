'''
-*- coding: utf-8 -*-
@Author  : TY Ren
@Time    : 2021/8/17 12:20
@Software: PyCharm
@File    : Wechat.py
'''
import pandas as pd
import pdfkit
import time
import requests
import json

arr = []
n = 0
for i in range(0,30):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030522)',
             'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=260452680; lang=zh_CN; pass_ticket=36HKgH5y1LYJhnjrwveB5yFkYNosmLSN91zwk3j0dDuy0K1ClCD5kDSOfYFa5own; appmsg_token=1128_IiA1WsPZaN%2BT36wfcvNvULmCPEz_g4w2Z5nTzMTdr0RK29VFWetZxcuKh-M~; devicetype=iPhoneiOS12.4.5; version=18000c22; wap_sid2=CMjimHwSigF5X0hLNHEtSjZBNzhieU1hZGhORnotNEdBOTNObmdFaUg2dXJCRlIwaDhIdnYyVG5iVWRfYnRiTF91dng1dTNoeWdwU29tYlZaZVdDdFU2VEJ2SlYzQjJHcFV0MTBFSlRpWHVuQW1yMlotalhIR29zeHlkSTVBdkFLSlZzX1dxRy1BSzBVU0FBQX4w1IiiiQY4DUCVTg==',
             'Host': 'mp.weixin.qq.com',
             'Referer':'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzIxNjc2MTc2MQ==&scene=124&uin=MjYwNDUyNjgw&key=09101c1c7f70495468512f63d626450eb3dd00ecf07eb255830f8dc9e390044d2766588b3d5ede309eb9bda56d7bbecada2ca1dddd6ef7a4818f5113d20e54de3561c117f79f141030290d716a29b356e70c77727b163272a198750f46aaf5a35e255ce650f8d28aa48e425b042f96e55f9dd94d9451a8be6cf0b3af9fa4170c&devicetype=Windows+10+x64&version=63030522&lang=zh_CN&a8scene=7&pass_ticket=36HKgH5y1LYJhnjrwveB5yFkYNosmLSN91zwk3j0dDuy0K1ClCD5kDSOfYFa5own&fontgear=2 HTTP/1.1'}
    # url ='https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzIxNjc2MTc2MQ==&f=json&offset='+str(i*10)+'&count=10&is_ok=1&scene=124&uin=MTM2MTk0NDc1&key=1b8ee8087b452ef1ffe573b64c127ccde8f2ae78f3554fb62ab5e0d6871a64de90670a6278131aa7b504688dc7812e8928499540bf30bb3b73fa5036b06546a83091ce4f8aff99fa17f06cc161883c4b017ed303029de7fd47bacb073610af23c924aeec2fb7bab962a9991c6f17f11bf7add5fcf5c74a3a452584d2be90af81&pass_ticket=PgxVpwDa7fOQ%2Bs0XmUVQhpmbNz9E1fOm7NVn%2Fy4tF713hAl7z21Mo%2BgW9XWfPkVB&wxtoken=&appmsg_token=1126_opAIloIO3FHh%252FuAYAEpMUUUYe_q8c9qkg6K76Q~~&x5=0&f=json'
    url ='https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzIxNjc2MTc2MQ==&f=json&offset='+str(i*10)+'&count=10&is_ok=1&scene=124&uin=MjYwNDUyNjgw&key=09101c1c7f70495468512f63d626450eb3dd00ecf07eb255830f8dc9e390044d2766588b3d5ede309eb9bda56d7bbecada2ca1dddd6ef7a4818f5113d20e54de3561c117f79f141030290d716a29b356e70c77727b163272a198750f46aaf5a35e255ce650f8d28aa48e425b042f96e55f9dd94d9451a8be6cf0b3af9fa4170c&pass_ticket=36HKgH5y1LYJhnjrwveB5yFkYNosmLSN91zwk3j0dDuy0K1ClCD5kDSOfYFa5own&wxtoken=&appmsg_token=1128_tF%252FIIdHELljP6zumvh0CzsHrQ1Unn_yZVHgsCg~~&x5=0&f=json HTTP/1.1'
    print(url)
    time.sleep(6)
    res = requests.get(url,headers=headers)
    print(res.json())
    jd = res.json()
    for j in range(10):
        n += 1
        print('第'+str(n)+'篇',json.loads(jd['general_msg_list'])['list'][j]['app_msg_ext_info']['title'])
        n1 = '第'+str(n)+'篇'
        t1 = json.loads(jd['general_msg_list'])['list'][j]['app_msg_ext_info']['title']
        u1 = json.loads(jd['general_msg_list'])['list'][j]['app_msg_ext_info']['content_url']
        if "SaaS" in t1 or "saas" in t1:
            li = [n1,t1,u1]
            arr.append(li)
    df = pd.DataFrame(arr,columns=['篇幅','标题','链接'])
    df.to_excel(r'C:\Users\Administrator\Desktop\SaaS白夜行.xlsx')








