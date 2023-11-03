# -*-coding:GBK -*-
import os
import re
import time
from datetime import datetime

import pandas as pd
from deepdiff import DeepDiff
from util.base93 import decode
import requests
import yaml
from util.logTool import logger
import numpy as np
# python�����������Ա�
# np.array_equiv
# ��űȶԲ��ϵĹ�Ʊ��
code_list = []
# ��űȶԲ��ϵ��ֶ���
field_list = []

time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
yaml_path = rootPath + '/testCase/quote/Kline.yaml'
date = time.strftime("%Y%m%d", time.localtime())
time = time.strftime("%H%M%S", time.localtime())
current_date = int(datetime.now().strftime('%Y%m%d'))
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
    """
    :param json1: д�������
    :param title: title
    :return: excel
    """
    excel_path = curPath + f'\\result\\{time}K������.xlsx'
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
        "symbol": "600000.sh"
        # "param": "20231031140200"

    }
    # headers1 = {
    #     "token": "MitakeWeb",
    #     "symbol": "getline"
    #
    # }
    # url1 = "http://114.80.155.61:22016/v1/sh1/dayk/601099?today=y&select=date,open,high,low,close,volume,amount,prevClose,fp_volume,fp_amount,ref,iopv,avg&begin=300&end=202206130930"
    url2 = "http://114.80.155.134:22016/v3/m1"
    response_list1 = []
    response_list2 = []
    response1 = SseOptionQuote(url2, header=headers)
    # response2 = SseOptionQuote(url2, header=headers1)
    # print(type(response1.text))
    # MDS�ӿڷ�������δ���룬ֱ�����
    # print(response1.text)
    # SDK�ӿڷ������ݼ��ܣ���Ҫ����
    decode_response = decode_quote(response1.text)
    print(decode_response)
    if response1:
        response_list1.append(decode_response)
        logger.debug(f"url1 success headers '{headers}'")
    else:
        logger.info(f"Failed to get response for url '{url2}'")
    logger.info(f"����K������=====>'{response_list1}'")
    # �������б�  ������K���������ó������K�����ݣ��Ա�͵������������ݶԱ�
    filtered_data = []
    for items in response_list1:
        for row in items:
            if row[0] == current_date:
                filtered_data.append(row)
        logger.info(f"����K������=====>'{filtered_data}'")
    # res2 = response2.json()["kline"]
    # response_list2.append(res2)
    # if response2:
    #     response_list2.append(response2.text)
    #     logger.debug(f"url2 success headers '{headers}'")
    # else:
    #     logger.info(f"Failed to get response for url '{url2}'")
    # compare_lists(response_list1,response_list2)
    # logger.info(f"response_list2=====>'{response_list2}'")
    write_excel(filtered_data,excel_yaml_title())

