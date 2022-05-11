# -*- coding: utf-8 -*-

import requests
import datetime
import json

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

date = datetime.datetime.now().strftime("%Y%m%d")

for name in json.loads(name_response)['components']:
    list = []
    list.append("项目名称：" + name['name'])
    for data in json.loads(data_response)['measures']:
        if (name['key'] == data['component'] and data['metric'] != 'alert_status' and data['metric'] != 'ncloc_language_distribution' and data['metric'] != 'reliability_rating' and data['metric'] != 'security_rating' and data['metric'] != 'sqale_rating' and data['metric'] != 'ncloc'):
            if(data['metric'] == 'bugs'):
                list.append("bug：" + data['value'])
            if (data['metric'] == 'vulnerabilities'):
                list.append("漏洞：" + data['value'])
            if (data['metric'] == 'code_smells'):
                list.append("异味：：" + data['value'])
            if (data['metric'] == 'coverage'):
                list.append("覆盖率：" + data['value'] + '%')

    print(list)