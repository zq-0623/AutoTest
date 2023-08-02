# -*-coding:GBK -*-
import os
import time

from deepdiff import DeepDiff
from util.base93 import decode
import requests
import yaml
import numpy as np
# python两个数组做对比
# np.array_equiv

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
yaml_path = rootPath + '/testCase/quote/line.yaml'
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
        print("对比结果一致")
    else:
        print(f"存在差异===》'{diff}'")
        if 'values_changed' in diff:
            values_changed = diff['values_changed']
            key_list = list(values_changed.keys())
            val_list = list(values_changed.values())
            print(key_list)
            for i in val_list:
                new_value = i['new_value']
                old_value = i['old_value']
                envList1.append(old_value)

                envList2.append(new_value)
            print(envList1)
            print(envList2)


def SseOptionQuote(url, headers, **kwargs):
    try:
        response = requests.Session().get(url,headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error while requesting url '{url}':{e}")
        return None


if __name__ == '__main__':
    headers = {
        "token": "MitakeWeb",
        "symbol": "000539.sz",
        "param": "0930"
    }
    url1 = "http://114.80.155.61:22016/v4/line5d"
    url2 = "http://114.80.155.134:22016/v4/line5d"
    response_list1 = []
    response_list2 = []
    response1 = SseOptionQuote(url1,headers=headers)
    response2 = SseOptionQuote(url2,headers=headers)
    if response1:
        response_list1.append(decode_quote(response1.text))
    else:
        print(f"Failed to get response for url '{url1}'")
    if response2:
        response_list2.append(decode_quote(response2.text))
    else:
        print(f"Failed to get response for url '{url2}'")
    compare_lists(response_list1,response_list2)
    print(f"response_list1=====>'{response_list1}'")
    print(f"response_list2=====>'{response_list2}'")