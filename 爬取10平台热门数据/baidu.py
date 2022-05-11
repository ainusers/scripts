# -*- coding: utf-8 -*-

import requests
from lxml import etree
import datetime
import redis
import sys
import importlib
importlib.reload(sys)

# 连接redis
pool = redis.ConnectionPool(host="81.70.163.240", port=6379, password="", max_connections=1024,db=0)
con = redis.Redis(connection_pool=pool)

# 组装请求
url = 'http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b1_c513'
headers = {
           "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
           }
response = requests.get(url,headers=headers)
# response.encoding = 'gbk'
date = datetime.datetime.now().strftime("%Y%m%d")

# 提取数据
selector = etree.HTML(response.text)
lists = selector.xpath("//div[@class='container-bg_lQ801']/div[2]/div")

i = 0
for video in lists:
    title = video.xpath("./div[@class='content_1YWBm']/a/div[@class='c-single-text-ellipsis']/text()")
    hot = video.xpath("./div[@class='trend_2RttY hide-icon']/div[@class='hot-index_1Bl1a']/text()")
    link = video.xpath("./a[@class='img-wrapper_29V76']/@href")

    if (len(title) != 0):

        # 写入redis
        i = i + 1
        mid = "title$$" + title[0] + '##' + "link$$" + link[0] + '##' + "hot$$" + hot[0]
        con.zadd('baidu_{}'.format(date), {mid: i})

        # 读取redis
        # title = con.zrange('36kr_20201211', 0, -1, desc=False)
        # print (title)
        # break
