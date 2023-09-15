# -*-coding:GBK -*-
import os
import re
import time

import pandas as pd
from deepdiff import DeepDiff
from util.base93 import decode
import requests
import yaml
from util.logTool import logger
import numpy as np
# python两个数组做对比
# np.array_equiv
# 存放比对不上的股票名
code_list = []
# 存放比对不上的字段名
field_list = []

time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
yaml_path = rootPath + '/testCase/quote/Kline.yaml'
date = time.strftime("%Y%m%d", time.localtime())
time = time.strftime("%H%M%S", time.localtime())
file_name = ''


def request(url, methods, **kwargs):
    methods = methods.lower()
    if methods == "get":
        res = requests.Session().get(url, **kwargs)
        return res
    elif methods == "post":
        res = requests.Session().post(url, **kwargs)
        return res


def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        return yaml.safe_load(fp)


data = quote_yaml(yaml_path)


def decode_quote(msg):
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


def compare_lists(list1,list2):
    # # 存放环境1数据
    envList1 = []
    # # 存放环境2数据
    envList2 = []
    # 使用 DeepDiff 函数比较两个列表，并忽略元素的顺序
    diff = DeepDiff(list1,list2)
    if not diff:
        logger.debug("对比结果一致")
    else:
        logger.debug(f"存在差异===》'{diff}'")
        if 'values_changed' in diff:
            values_changed = diff['values_changed']
            key_list = list(values_changed.keys())
            val_list = list(values_changed.values())
            # print(key_list)
            for i in val_list:
                new_value = i['new_value']
                old_value = i['old_value']
                envList1.append(old_value)
                envList2.append(new_value)
            # print(envList1)
            # print(envList2)
            for j in key_list:
                m = re.findall(r'\[\'(.*?)\'\]' , j)
                code_list.append(m[0])
                field_list.append(m[1])


def SseOptionQuote(url, header, **kwargs):
    try:
        response = requests.Session().get(url, headers=header)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.debug(f"Error while requesting url '{url}':{e}")
        logger.debug(f"Error while request headers '{header}':{e}")
        return None


def write_excel(json1,title):
    excel_path = curPath + f'\\result\\{time1}_走势数据.xlsx'
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
        "symbol": "000002.sz",
        "permis": "L1"
        # "param": "20230914"
    }
    # headers1 = {
    #     "token": "MitakeWeb",
    #     "symbol": "getline"
    #
    # }
    url1 = "http://114.80.155.61:22016/v3/dayk"
    # url2 = "http://114.80.155.61:22016/v1/sh1/dayk/601099?today=y&select=date,open,high,low,close,volume,amount,prevClose,fp_volume,fp_amount,ref,iopv,avg&begin=300&end=202206130930"
    # url1 = "http://114.80.155.61:22016/v4/line"
    # url1 = "http://114.80.155.134:22016/v4/line"
    # url2 = "http://114.80.155.61:22016/v1/sh1/mink/600050?begin=-200&end=-1&period=1&recovered=forward&select=date,
    # close,avg,volume,ref,amount,open,high,low"
    response_list1 = []
    response_list2 = []
    response1 = SseOptionQuote(url1, header=headers)
    # response2 = SseOptionQuote(url2,headers=headers1)
    # print(type(response1.text))
    print(response1.text)
    decode_response = decode_quote(response1.text)
    if response1:
        response_list1.append(decode_response)
        logger.debug(f"url1 success headers '{headers}'")
    else:
        logger.info(f"Failed to get response for url '{url1}'")
    # res2 = response2.json()["kline"]
    # response_list2.append(res2)
    # if response2:
    #     response_list2.append(response2.text)
    #     logger.debug(f"url2 success headers '{headers}'")
    # else:
    #     logger.info(f"Failed to get response for url '{url2}'")
    # compare_lists(response_list1,response_list2)
    # logger.info(f"response_list1=====>'{response_list1}'")
    # logger.info(f"response_list2=====>'{response_list2}'")
    # print(decode_response)
    # write_excel(decode_response,excel_yaml_title())
