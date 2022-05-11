# -*- coding: utf-8 -*-

import requests
from lxml import etree
import datetime
import redis
import sys
import importlib
importlib.reload(sys)


# 组装请求
url = 'https://s.weibo.com/top/summary?cate=realtimehot'
headers = {
	   "cookie":"_s_tentry=passport.weibo.com; Apache=2691976605129.9688.1635394757347; SINAGLOBAL=2691976605129.9688.1635394757347; ULV=1635394757353:1:1:1:2691976605129.9688.1635394757347:; XSRF-TOKEN=MRyiYdwZVeUzNgE-j5GNCveM; login_sid_t=11d7ef29ee756a83c88b39d4a3aaf0ef; cross_origin_proto=SSL; WBStorage=5fd44921|undefined; wb_view_log=1280*7201.5; ALF=1666931916; SSOLoginState=1635395916; SUB=_2A25MflkdDeRhGeNJ7VoT9S7EyT6IHXVvCs3VrDV8PUNbmtAKLUXRkW9NS7ozs1we9WlhzEwTK2NU_Ml3-K9Q1oqp; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFHpcI2BAPP23oX1pFzuSDj5JpX5KzhUgL.Fo-NSonESK5Reoz2dJLoI7UWIg4HMcHE; WBPSESS=LOrcKJ3xqF2f-1P4Elf8YUJsmiLFboX88T_EKT-8iTWQgyul92Bg87Ns2DvUN7rEu1iTnzM-mL0zWGusuh6VrKC-cbM60v2r1Wn_QBNl6E7whxuHoetk7dO5JAyhh5_V"
           ,"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
           }
response = requests.get(url,headers=headers)
date = datetime.datetime.now().strftime("%Y%m%d")

# 连接redis
pool = redis.ConnectionPool(host="81.70.163.240", port=6379, password="", max_connections=1024,db=0)
con = redis.Redis(connection_pool=pool)

# 判断对象是否为纯数字
def isLetter(params):
    for ch in params.encode('utf-8').decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

# 提取数据
selector = etree.HTML(response.text)
lists = selector.xpath("//div[@class='m-wrap']/div[@class='data']/table/tbody/tr")
i = 0
for video in lists:
    title = video.xpath("./td[@class='td-02']/a/text()")
    hot = video.xpath("./td[@class='td-02']/span/text()")
    uri = video.xpath("./td[@class='td-02']/a/@href")
    if ("javascript:void(0);" in uri):
        uri = video.xpath("./td[@class='td-02']/a/@href_to")
    link = 'https://s.weibo.com/{}'.format(uri[0])

    if (len(hot) != 0):
        mid = title[0]

        # 判断是否为纯字母
        if (isLetter(mid) is False):
           title = str(mid)

        # 写入redis
        i = i + 1
        mid = "title$$" + title[0] + '##' + "link$$" + link + '##' + "hot$$" + hot[0]
        con.zadd('weibo_{}'.format(date), {mid: i})

        # 读取redis
        # title = con.zrange('36kr_20201211', 0, -1, desc=False)
        # print (title)
        # break
