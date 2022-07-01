# -*- coding: utf-8 -*-

import requests
import sys
import urllib3
urllib3.disable_warnings()
import importlib
importlib.reload(sys)


url = 'http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do'
headers = {
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
           }
datas = (('pType', '01'), ('startDate', '2022-01-01'), ('endDate', '2022-06-30'), ('page', '1'), ('pageSize', '15'))
rsp = requests.post(url,data=datas,headers=headers,verify=False).json()

# 提取数据
for video in rsp['rows']:
    NOTICE_ID = video['NOTICE_ID']
    NOTICE_TITLE = video['NOTICE_TITLE']
    url = 'http://www.ccgp-hunan.gov.cn/mvc/viewNoticeContent.do?noticeId='+str(NOTICE_ID)+'&area_id='
    rsp_html = requests.post(url,data=datas,headers=headers,verify=False).content
    with open(str(NOTICE_TITLE)+".html", "wb") as file:
        file.write(rsp_html)
