# -*- coding: utf-8 -*-

import requests
import datetime
import json
import csv

# author: tianyong
# date: 2022-05-07 20:00
# target: 爬取sonar指标数据

# 获取组件名称
name_url = 'https://sonar-biz.qianxin-inc.cn/api/components/search_projects?ps=50&facets=reliability_rating%2Csecurity_rating%2Csqale_rating%2Ccoverage%2Cduplicated_lines_density%2Cncloc%2Calert_status%2Clanguages%2Ctags&f=analysisDate%2CleakPeriodDate'
# 获取指标数据
data_url = 'https://sonar-biz.qianxin-inc.cn/api/measures/search?projectKeys=situation%3Aactivity1%2Ccssa%3Ademo%2Cemergency%3Aemergency1%2Cgovernance%3Agovernance1%2Csituation%3Aleo1%2Csituation%3AdataGraph1%2Cnotice%3Anotice1%2Csituation%3Aorchestration1%2Csituation%3Aplan1%2Csituation%3Aresource1%2CTSGZ%3Ascene-v1%2CTSGZ%3Asiriusv1%2Csirius%3Asdk1%2CdataReport%3AdataReport1%2Csituation%3Acertification1%2Ctransfer%3Atransfer1%2Cssc%3Aapi%2Cssc%3Aspark%2Cssc%3A1012%2Cbisheng%3Abisheng1%2Cintegrated%3Aintegrated1%2Csafety-monitor%3Asafety-monitor1%2Csituation%3Aspeech%2Csisconfig%3Asisconfig&metricKeys=alert_status%2Cbugs%2Creliability_rating%2Cvulnerabilities%2Csecurity_rating%2Ccode_smells%2Csqale_rating%2Cduplicated_lines_density%2Ccoverage%2Cncloc%2Cncloc_language_distribution'
headers = {
           "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
           }
name_response = requests.get(name_url,headers=headers,auth=('tianyong','w979111986...')).content.decode()
data_response = requests.get(data_url,headers=headers,auth=('tianyong','w979111986...')).content.decode()

#  1. 创建文件对象
f = open('ty.csv', 'w', encoding='utf-8-sig')
#  2. 基于文件对象构建csv写入对象
csv_write = csv.writer(f)
#  3. 构建列表头
csv_write.writerow(['工程名', '日期', 'Bugs', '严重类Bugs', '阻断类Bugs', '异味' , '严重类异味', '阻断类异味', '单测覆盖率', '重复', '总代码行数' ,'漏洞', '严重类漏洞', '阻断类漏洞','异味/代码行'])

for name in json.loads(name_response)['components']:
    list = []
    list.append(name['name'])
    if('analysisDate' in name):
        list.append(name['analysisDate'][0:10])
    bag = 0
    yiwei = 0
    loudong = 0
    for data in json.loads(data_response)['measures']:
        if (name['key'] == data['component'] and data['metric'] != 'alert_status' and data['metric'] != 'ncloc_language_distribution' and data['metric'] != 'reliability_rating' and data['metric'] != 'security_rating' and data['metric'] != 'sqale_rating'):
            if(data['metric'] == 'bugs'):
                list.append(data['value'])
                # bug详情
                if(bag == 0):
                    bug_url = 'https://sonar-biz.qianxin-inc.cn/api/issues/search?componentKeys='+ name['key'] +'&s=FILE_LINE&resolved=false&types=BUG&ps=100&organization=default-organization&facets=severities,types&additionalFields=_all'
                    bug_detail = requests.get(bug_url, headers=headers, auth=('tianyong', 'w979111986...')).content.decode()
                    for bags in json.loads(bug_detail)['facets'][0]['values']:
                        if (bags['val'] == 'CRITICAL'):
                            list.append(bags['count'])
                        if (bags['val'] == 'BLOCKER'):
                            list.append(bags['count'])
                    bag = bag + 1
            if (data['metric'] == 'code_smells'):
                list.append(data['value'])
                # 异味详情
                if (yiwei == 0):
                    yiwei_url = 'https://sonar-biz.qianxin-inc.cn/api/issues/search?componentKeys=' + name['key'] + '&s=FILE_LINE&resolved=false&types=CODE_SMELL&ps=100&organization=default-organization&facets=severities,types&additionalFields=_all'
                    yiwei_detail = requests.get(yiwei_url, headers=headers, auth=('tianyong', 'w979111986...')).content.decode()
                    for yiweis in json.loads(yiwei_detail)['facets'][0]['values']:
                        if (yiweis['val'] == 'CRITICAL'):
                            list.append(yiweis['count'])
                        if (yiweis['val'] == 'BLOCKER'):
                            list.append(yiweis['count'])
                    yiwei = yiwei + 1
            if (data['metric'] == 'coverage'):
                list.append(data['value'] + '%')
            if (data['metric'] == 'duplicated_lines_density'):
                list.append(data['value'] + '%')
            if (data['metric'] == 'ncloc'):
                list.append(data['value'])
            if (data['metric'] == 'vulnerabilities'):
                list.append(data['value'])
                # 漏洞详情
                if (loudong == 0):
                    loudong_url = 'https://sonar-biz.qianxin-inc.cn/api/issues/search?componentKeys=' + name['key'] + '&s=FILE_LINE&resolved=false&types=VULNERABILITY&ps=100&organization=default-organization&facets=severities,types&additionalFields=_all'
                    loudong_detail = requests.get(loudong_url, headers=headers, auth=('tianyong', 'w979111986...')).content.decode()
                    for loudongs in json.loads(loudong_detail)['facets'][0]['values']:
                        if (loudongs['val'] == 'CRITICAL'):
                            list.append(loudongs['count'])
                        if (loudongs['val'] == 'BLOCKER'):
                            list.append(loudongs['count'])
                    loudong = loudong + 1
    # 异味/代码行
    if(len(list) > 10):
        list.append(round(((int(list[5])) / (int(list[10])) * 100), 2))
    # 输出至csv
    csv_write.writerow(list)
    print(list)

#  5.关闭文件
f.close()
