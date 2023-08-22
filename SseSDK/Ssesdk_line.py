# -*-coding:GBK -*-
import os
import time

from deepdiff import DeepDiff
from util.base93 import decode
import requests
import yaml
from util.logTool import logger
import numpy as np
# python�����������Ա�
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
        # load()������fp(һ��֧��.read()���ļ�����󣬰���һ��JSON�ĵ�)�����л�Ϊһ��Python����
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
    # # ��Ż���1����
    envList1 = []
    # # ��Ż���2����
    envList2 = []
    # ʹ�� DeepDiff �����Ƚ������б�������Ԫ�ص�˳��
    diff = DeepDiff(list1,list2)
    if not diff:
        logger.debug("�ԱȽ��һ��")
    else:
        logger.debug(f"���ڲ���===��'{diff}'")
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


def SseOptionQuote(url, headers, **kwargs):
    try:
        response = requests.Session().get(url,headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.debug(f"Error while requesting url '{url}':{e}")
        logger.debug(f"Error while request headers '{headers}':{e}")
        return None


if __name__ == '__main__':
    headers = {
        "token": "MitakeWeb",
        "symbol": "000902.csi",
        "param": "0930"
    }
    # headers1 = {
    #     "token": "MitakeWeb",
    #     "symbol": "getline"
    #
    # }
    # url1 = "http://114.80.155.61:22016/v3/m1"
    url1 = "http://114.80.155.61:22016/v4/line"
    url2 = "http://114.80.155.134:22016/v4/line"
    # url2 = "http://114.80.155.61:22016/v1/sh1/mink/600050?begin=-200&end=-1&period=1&recovered=forward&select=date,
    # close,avg,volume,ref,amount,open,high,low"
    response_list1 = []
    response_list2 = []
    response1 = SseOptionQuote(url1,headers=headers)
    response2 = SseOptionQuote(url2,headers=headers)
    if response1:
        response_list1.append(decode_quote(response1.text))
        logger.debug(f"url1 success headers '{headers}'")
    else:
        logger.info(f"Failed to get response for url '{url1}'")
    # res2 = response2.json()["kline"]
    # response_list2.append(res2)
    if response2:
        response_list2.append(decode_quote(response2.text))
        logger.debug(f"url2 success headers '{headers}'")
    else:
        logger.info(f"Failed to get response for url '{url2}'")
    compare_lists(response_list1,response_list2)
    logger.info(f"response_list1=====>'{response_list1}'")
    logger.info(f"response_list2=====>'{response_list2}'")
