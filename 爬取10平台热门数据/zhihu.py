# -*- coding: utf-8 -*-

import requests
from lxml import etree
import datetime
import redis
import sys
import importlib
importlib.reload(sys)

# 组装请求
url = 'https://www.zhihu.com/hot'
headers = {
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
	    "cookie":'_zap=98b5e7eb-3f7b-4a6a-b882-ee99b8f658e7; _xsrf=346b45af-98e0-4731-8e01-16cab9cc0dd7; d_c0="AIBfypPD8ROPTu6KdrYMnr-neV4H5R8oFSw=|1635422020"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1635422022; __snaker__id=WT8bJY2YOqasF50m; gdxidpyhxdE=cB4RNL2Q6MNBU4NjWKMPx8jifdJNu%5Cqy7Mc09R%2FC4LWOassp4DDwqt0%2Fo22SbWHT%2BtS3xcvwA3bn4ULfrNKjhp4Ka2569gAy9cqsKqekxlwAXU5NTYa%5C15oPCGrdvbABeHyR5GfeozYdG94pHZU%2FZJZT8zIzjqaICTqiaoBuDsdp072s%3A1635422922633; _9755xjdesxxd_=32; YD00517437729195%3AWM_NI=WI4UOJbDRs%2BuVnJzCLDYeeqhRYupz0vL0qmi6yhF1nxL5uenPalQXaOjH4Ast6o6qlSvyz%2BIFWBmXU36%2FH0eX9loI2PhKbUjx2%2FhFz4kKRiqxvAl97TfHW7issmEnuxMQnE%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eea3d364b0ece5a8d26288ef8fb7c54b838f8baef833a28bf78af47b9bbaa589b82af0fea7c3b92a9597fcb6ce42a29c9e94aa7f96b2869bc2488887ab86f4649287bb91f93cb6940092f063f6a7a8a7b466bc94fb96e86694bfa4b2db6b8db688d5c479b8eaa1d7f46891aab79baa4386898e8edb5ff1eae1a9b36f9ce7a490cc3a94b88583d862bceee189c572f8b585b3ec7bbcaa8f8dbc3d98ba88b8b663b1ada3a6ed7fbc939f8fc837e2a3; YD00517437729195%3AWM_TID=44%2FHkg9tRYlEEQBRRQI%2BsbQsz%2Brcbkgt; captcha_session_v2="2|1:0|10:1635422022|18:captcha_session_v2|88:UWQrSkszSlNoR2cxYllYZ0pJZEJNVVhrVHNFNkhSVFJMRmVzTE9CSm8zNTBaOEM3NzZoeGdRQWd3K2hQMjd2Ug==|3fe6b8d51990ce190daf9b9f0d53def649ebb05fb0d198c929cece6a7f2a820a"; captcha_ticket_v2="2|1:0|10:1635422028|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfZHZNdFNxeFJjdUVkT0VzakxtZkcuQ1djVnBPOVptSW11cHBlZHNMaXFZODlESVRRRThGZkRGeEdrVWNDY3RyQ0Y2ZlVzYUhJbWNHT2hxcDVEb3pCRGJqUXI4Y1R5V1NocG9BRlg0QlFpZ2lGOFRTSkRvV3BxRnVwb3J1LjlzS21FVmhSZUh0Z0VEeGFkV0hJWTFST2FmR2lBbHBsenZoMEVJWjJwTnVEVmpUcmFxQ0dRc3ROTEZKRjR4NXQ4TmJtVTZLeVVvTzFGUFk5N284ZFpYV19RR1FTVXpqNWpIajVkTlhodEVON1lyZkhmcUVqdlg5YVEtaURJNmhsLXEwbHpRVU0yOEdCVVRJV1A0b2pHSDY2c3FxWjRnNi5fUzdpbzUybC1sWHd5bWt6em1BdjZLYWdHemFRaUFPdGJFOTVTNEpiaXJUZ0tNUE9OU2ktVXpORlZRTl9qeFZkU3I5Si1uMXlVczcxRlBwaGNwNjdmZXViRi5hNktRMS41ZWZibWZKc0J5SzkwbFlielY4UkE0QkRVcEtQUHdXTzdNamcxWnRuMUNVSWR5QnZWa3pMY1BHWERyNkVfZ2ktZW15RjlEVWJKTEtteVZ3WXlzSFFySnp2Z29JNmJYY2Vhc2ZsdTZaZzZDLXM5aHVPS0poNWFlV3RRSEJLMW9qMyJ9|03338095e3083f415343a00b47a78ace379eb24ff4a14f7997b5effc5f8951a7"; z_c0="2|1:0|10:1635422028|4:z_c0|92:Mi4xaGZOTEF3QUFBQUFBZ0ZfS2s4UHhFeVlBQUFCZ0FsVk5UTjFuWWdDWFdjUjJKX2dmTnFKc0J6a3dCaTBjRjlqWkZR|ae128d6d68d54bf5353b85c455c394bdedfd9022ccc37b11da7e901f5f64be18"; tshl=; tst=h; NOT_UNREGISTER_WAITING=1; KLBRSID=b5ffb4aa1a842930a6f64d0a8f93e9bf|1635422235|1635422019; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1635422237'
}
response = requests.get(url,headers=headers)
date = datetime.datetime.now().strftime("%Y%m%d")
times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# 连接redis
pool = redis.ConnectionPool(host="81.70.163.240", port=6379, password="", max_connections=1024,db=0)
con = redis.Redis(connection_pool=pool)

# 提取数据
selector = etree.HTML(response.text)
lists = selector.xpath("//div[@class='HotList-list']/section[@class='HotItem']")
i = 0
for video in lists:
    title = video.xpath("./div[@class='HotItem-content']/a/@title")
    hot = video.xpath("./div[@class='HotItem-content']/div[@class='HotItem-metrics HotItem-metrics--bottom']/text()")
    link = video.xpath("./div[@class='HotItem-content']/a/@href")

    if (len(hot) == 0):
        hot = video.xpath("./div[@class='HotItem-content']/div[@class='HotItem-metrics']/text()")

    # 写入redis
    i = i + 1
    mid = "title$$" + title[0] + '##' + "link$$" + link[0] + '##' + "hot$$" + str(hot[0]).replace('热度','').replace(" ","")
    con.zadd('zhihu_{}'.format(date), {mid: i})

    # 读取redis
    # title = con.zrange('36kr_20201211', 0, -1, desc=False)
    # print (title)
    # break
