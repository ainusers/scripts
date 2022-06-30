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

url = 'http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do'
print(url)
headers = {
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
           }
datas = (('pType', '01'), ('startDate', '2022-01-01'), ('endDate', '2022-06-30'), ('page', '1'), ('pageSize', '50'))
response = requests.post(url,data=datas,headers=headers,verify=False).json()

f = open('caigouwang.csv','w',encoding='utf-8-sig')
writer = csv.writer(f)
writer.writerow(['省份','方式','编号','名称','公告时间','招标方'])

print(response)
# 提取数据
for video in response['rows']:
    list = []
    AREA_NAME = video['AREA_NAME']
    list.append(AREA_NAME)
    PRCM_MODE_NAME = video['PRCM_MODE_NAME']
    list.append(PRCM_MODE_NAME)
    ORG_CODE = video['ORG_CODE']
    list.append(ORG_CODE)
    NOTICE_TITLE = video['NOTICE_TITLE']
    list.append(NOTICE_TITLE)
    NEWWORK_DATE = video['NEWWORK_DATE']
    list.append(NEWWORK_DATE)
    ORG_NAME = video['ORG_NAME']
    list.append(ORG_NAME)
    # 输出至csv
    writer.writerow(list)