# encoding=utf-8
import json
import os
import re
import time

import pandas as pd
import requests
import yaml
from util.base93 import decode
date = time.strftime("%Y%m%d", time.localtime())
time1 = time.strftime("%H%M%S", time.localtime())
curPath = os.path.abspath(os.path.dirname(__file__))
yaml_path = "../testCase/quote/line.yaml"


def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        return yaml.safe_load(fp)


data = quote_yaml(yaml_path)


def decode_quote(msg):
    res_list = [msg.get('a'), msg.get('c'), msg.get('ot'), msg.get('h'), msg.get('i'), msg.get('l'), msg.get('m'),
                msg.get('o'), msg.get('dt'), msg.get('r'), msg.get('t'), msg.get('v'), msg.get('r'), msg.get('ic')]
    for i in range(len(res_list)):
        data_values = list(data[i].values())[0]
        if data_values == 'Y':
            res_list[i] = decode(res_list[i])
    print(res_list)


def decode_quote1(msg):
    res_list = msg.split("\x03")
    list_result = []
    if res_list[-1] == '':
        res_list.remove('')
    for m in range(len(res_list)- 1):
        split_list = res_list[m].split("\x02")
        for i in range(len(split_list)):
            data_key = list(data[i].keys())[0]
            data_values = list(data[i].values())[0]
            if data_values == 'Y':
                split_list[i] = decode(split_list[i])
        list_result.append(split_list)
    return list_result


def write_excel(json1,title):
    excel_path = curPath + f'\\result\\{time1}test.xlsx'
    if not os.path.exists(excel_path):
        wr = pd.ExcelWriter(excel_path)
        ew = pd.DataFrame(json1,columns=title)
        ew.to_excel(wr,sheet_name=date,index=False)
        wr.close()
    else:
        wr = pd.ExcelWriter(excel_path,mode="a",engine='openpyxl')
        ew = pd.DataFrame(json1,columns=title)
        ew.to_excel(wr,sheet_name=date,index=False)
        wr.close()


def excel_yaml_title():
    keys_list = []
    for i in data:
        key_name = i.keys()
        m = re.findall(r"'(.*?)'", str(key_name))
        sheet_title = str(m).split("['")[1].split("']")[0]
        keys_list.append(sheet_title)
    return keys_list


if __name__ == '__main__':
    headers = {
        "token": "MitakeWeb",
        "symbol": "601099.sh",
        "param": "202309141315"
    }
    url1 = "http://114.80.155.61:22016/v4/line"
    response = requests.get(url=url1,headers=headers)
    json1 = decode_quote1(response.text)




