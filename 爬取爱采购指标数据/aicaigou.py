# -*- coding: utf-8 -*-

import requests
import sys
import csv
import time
import urllib3
urllib3.disable_warnings()
import importlib
importlib.reload(sys)


# 组装请求
for i in range(34):
    time.sleep(5)
    url = 'https://b2b.baidu.com/s/a?ajax=1&csrf_token=c6214ae34b4845f8598d5fca0de1b51a&logid=2385513514806284054&fid=67567616,1654236396849&_=1654237074685&q=水泥检查井&from=search&pi=b2b.index.search...1199248967131081&o=0' + '&p={p}'.format(p=i) + '&mxk=全部结果&f=[]&s=30&adn=3&resType=product&fn={"brand_name":"品牌","select_param1":"外观","select_param2":"形状"}'
    print(url)
    headers = {
                "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
               }
    response = requests.get(url,headers=headers,verify=False).json()

    f = open('aicaigou.csv','w',encoding='utf-8-sig')
    writer = csv.writer(f)
    writer.writerow(['地址','姓名','手机号','邮箱','QQ','微信'])

    # 提取数据
    for video in response['data']['productList']:
        time.sleep(5)
        title = video['jumpUrl']
        if ('&logid' in title):
            url = 'https://b2b.baidu.com/land/entProdAjax?ajax=1&csrf_token=c6214ae34b4845f8598d5fca0de1b51a&name=%E5%86%85%E8%92%99%E5%8F%A4%E8%92%99%E8%90%A5%E6%96%B0%E5%9E%8B%E5%BB%BA%E6%9D%90%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&s=8&';
            url = url + '&logid' + title.split("&logid")[1]
            response = requests.get(url,headers=headers).json()
            time.sleep(5)
            address = response['data']['cardInfo']['externalAddress']
            name = response['data']['cardInfo']['contactName']
            phone = response['data']['cardInfo']['phoneNumber']
            email = response['data']['cardInfo']['email']
            qq = response['data']['cardInfo']['qqNumber']
            wx = response['data']['cardInfo']['wechatNumber']
            print(address,name,phone,email,qq,wx)
            # writer.writerow([address,name,phone,email,qq,wx])
            # writer.writerow(['address','name','phone','email','qq','wx'])