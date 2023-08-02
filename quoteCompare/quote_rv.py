# -*-coding:GBK -*-
import json
import os
import sys

import zstd
from PyQt5.QtCore import QUrl

'''
rvΪ�����ӿ�
�˽ӿڽ�֧�ֻ���Level2
��������Ϊ�ɽ������������������ֱ��Ӧ24������,�ֺ͹���100����ϵ��ծȯ�͹���10����ϵ
����ͳ�ƶ�������䵥λΪ��
'''
curPath = os.path.abspath(os.path.dirname(__file__))

rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import re
import time
from itertools import groupby
from operator import itemgetter
from threading import Thread

import pandas as pd
import requests
import yaml
from deepdiff import DeepDiff
from util.base93 import decode

import paho.mqtt.client as mqtt

# ��ǰ����
date1 = time.strftime('%Y%m%d', time.localtime())
# ��ǰʱ��
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
# �������ļ�·��
stock_path = f'../testCase/AllStock'
# url�ļ�·��
url_path = f'../testCase/quote/url_rv.yaml'
# �ȶԽ�����·��
result_path = 'result'
# ÿ��������Ĺ�Ʊ����
interval = 50
# ��ſ����ֶ�
data = []
# ��Ż���1����
quote_list1 = []
# ��Ż���2����
quote_list2 = []
# �ļ�����
file_name = ""
# ����Ϊ�չ�Ʊ�б�
none_list = []
# �����쳣�Ĺ�Ʊ�б�
exception_list = []

quote_map1 = {}
quote_map2 = {}


def arr_spits(item, n):
    return [item[i:i + n] for i in range(0, len(item), n)]


# ��ȡ�����ֶ����ļ�
def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        # load()������fp(һ��֧��.read()���ļ�����󣬰���һ��JSON�ĵ�)�����л�Ϊһ��Python����
        return yaml.safe_load(fp)


# �ָ��Ʊ����
def interval_stock(path, item):
    stock_list = []
    stock_str = ''
    index = 0
    with open(path, 'r', encoding='utf-8') as stock:
        # load()������fp(һ��֧��.read()���ļ�����󣬰���һ��JSON�ĵ�)�����л�Ϊһ��Python����
        txt_list = json.load(stock)
        for st in txt_list:
            stock_list.append(st['s'])
    thread_run(stock_list, item)


# ���߳�����ӿ�
def thread_run(stock_list, item):
    # env = None
    thread_array = []
    for i in range(2):
        key = "env" + str(i + 1)
        env = item[key]
        t = Thread(target=request_run, args=(stock_list, env, i))
        thread_array.append(t)
        t.start()
    for t in thread_array:
        t.join()
    compare_result(item)


# �ӿ�����
def request_run(stock_list, env, flag):
    print("�ӿڵ�����....")
    for k in stock_list:
        header = {
            'Token': 'MitakeWeb',
            'Symbol': k
        }
        try:
            resp = requests.session().get(url=env, headers=header,verify=False)
            resp_list = resp.text.split("\x03")
            if resp_list[-1] == '':
                resp_list.remove('')
            if len(resp_list) == 0 or resp_list[0] == "":
                none_str = "���룺" + k + ",������" + env
                none_list.append(none_str)
                continue

            resp_list_quantity = str(resp_list[0]).split("\x02")
            resp_list_buy_quantity = str(resp_list[1]).split("\x02")
            resp_list_sell_quantity = str(resp_list[2]).split("\x02")

            for m in range(len(resp_list_quantity)):
                quote_dict = dict()
                quote_dict["����"] = k + "#�����" + str(m)
                quote_dict["��"] = resp_list_quantity[m]
                quote_dict["����"] = resp_list_buy_quantity[m]
                quote_dict["����"] = resp_list_sell_quantity[m]

                if flag == 0:
                    quote_list1.append(quote_dict)
                    quote_map1[k + "#�����" + str(m)] = quote_dict
                else:
                    quote_list2.append(quote_dict)
                    quote_map2[k + "#�����" + str(m)] = quote_dict
        except Exception:
            exception_list.append(file_name)
            raise
# ���ձȶ�
def compare_result(item):
    print("��ʼ�ȶ�....")
    # print(quote_list1)
    # print(len(quote_list2))
    # list1 = key_sort_group(quote_list1, '����')
    # list2 = key_sort_group(quote_list2, '����')
    # print(list1)
    print("��Ʊ����������", len(quote_list1))
    print("��Ʊ����������", len(quote_list2))
    # ����ȶ�
    resp_list1 = DeepDiff(quote_list1, quote_list2, group_by='����')
    # print(resp_list1)
    # ��Ż���1����
    envList1 = []
    # ��Ż���2����
    envList2 = []
    key_list = []
    # ��űȶԲ��ϵĹ�Ʊ��
    code_list = []
    # ��űȶԲ��ϵ��ֶ���
    field_list = []
    # print(resp_list1)
    # �жϱȶԽ��
    if resp_list1:
        # print("����ģ�", item)
        # ��ȡ�ȶԲ��ϵ��ֶ�
        if 'values_changed' in resp_list1:
            values_changed = resp_list1['values_changed']
            key_list = list(values_changed.keys())
            val_list = list(values_changed.values())
            for i in val_list:
                old_value = i['old_value']
                new_value = i['new_value']
                envList1.append(old_value)
                envList2.append(new_value)
            # ��ȡ��Ʊ�����Լ��ֶ�
            for j in key_list:
                m = re.findall(r'\[\'(.*?)\'\]', j)
                code_list.append(m[0])
                field_list.append(m[1])
        # ��ȡ����ֶ�
        if 'dictionary_item_added' in resp_list1:
            dictionary_item_added = resp_list1['dictionary_item_added']
            for di in dictionary_item_added:
                code_list.append(di[6:-2])
                field_list.append('All')
                if di[6:-2] in quote_map1:
                    envList1.append(quote_map1[di[6:-2]])
                else:
                    envList1.append('')
                if di[6:-2] in quote_map2:
                    envList2.append(quote_map2[di[6:-2]])
                else:
                    envList2.append('')
        #  ��ȡ�ٵ��ֶ�
        if 'dictionary_item_removed' in resp_list1:
            dictionary_item_removed = resp_list1['dictionary_item_removed']
            for di in dictionary_item_removed:
                code_list.append(di[6:-2])
                field_list.append('All')
                if di[6:-2] in quote_map1:
                    envList1.append(quote_map1[di[6:-2]])
                else:
                    envList1.append('')
                if di[6:-2] in quote_map2:
                    envList2.append(quote_map2[di[6:-2]])
                else:
                    envList2.append('')
        json1 = {'��Ʊ����': code_list, '�ֶ���': field_list, item['env1']: envList1, item['env2']: envList2}
        # json1 = {'��Ʊ����': code_list,'�����':quj, '�ֶ���': field_list, item['env1']: envList1, item['env2']: envList2}
        write_excel(json1, file_name)
    else:
        # print("��ȷ�ģ�", item)
        json1 = {'�ȶԽ��': ['��ȫ��ͬ']}
        write_excel(json1, file_name)
    print("�ȶ����д��excel")


# �������
def key_sort_group(quote_list, str1):
    """���б���dict����ָ��key���򣬷���"""
    quote_list.sort(key=itemgetter(str1))  # code�����޷���ֵ
    # print(data)
    result = dict()
    for code, items in groupby(quote_list, key=itemgetter(str1)):  # ����code����
        # print(type(items))
        # d = dict(ChainMap(*items))
        result[str(code)] = list(items)
    return result


def sort_dict_by_keys(d, reverse=True):
    # ���������ǿ��ת���ᱨ����Ϊd.keys()�������ǣ�<class 'dict_keys'>��û��sort����
    keys = list(d.keys())
    keys.sort(reverse=reverse)
    return [(key, d[key]) for key in keys]

# ���д��excel
def write_excel(json1, item):
    # ����ļ�������
    write_path = curPath + f'\\result\\rvResult\\{time1}_�����ȶԽ��.xlsx'
    if not os.path.exists(write_path):
        ew = pd.ExcelWriter(write_path)
        wr = pd.DataFrame(json1)
        wr.to_excel(ew, sheet_name=item, index=False)
        ew.close()
    # ����ļ�����
    else:
        # wb = load_workbook(write_path, mode='a', engine='openpyxl')
        ew = pd.ExcelWriter(write_path, mode='a', engine='openpyxl')
        # ew.book = wb
        wr = pd.DataFrame(json1)
        wr.to_excel(ew, sheet_name=item, index=False)
        ew.close()


if '__main__' == __name__:
    # �жϴ��·���Ƿ����
    if os.path.exists(result_path):
        pass
    else:
        os.makedirs(result_path)
    # ��ȡ�����ֶ��ļ�
    # data = quote_yaml(yaml_path)
    # ��ȡurl�ļ�
    compare_url = quote_yaml(url_path)
    # ��ȡ�������ļ���
    dirs = os.listdir(stock_path)
    # �ȶԻ�����url
    url = None
    # ��������ļ����ļ���
    # for file in dirs:
    #     file_name = file
    # print(compare_url.keys())
    for url_key in compare_url.keys():
        url = None
        file = "AllStock_" + url_key + ".txt"
        file_name = url_key
        # if url_key == "shl2":
        #     url = compare_url[url_key]
        # if url_key == "szl2":
        #     url = compare_url[url_key]
        # if url_key == "bz":
        #     url = compare_url[url_key]
        # if url_key == "csi":
        #     url = compare_url[url_key]
        # if url_key == "hk":
        #     url = compare_url[url_key]
        if url_key == "shl2":
            url = compare_url[url_key]
            file = "AllStock_sh.txt"
        if url_key == "szl2":
            url = compare_url[url_key]
            file = "AllStock_sz.txt"
        # ��Ż���1����
        quote_list1 = []
        # ��Ż���2����
        quote_list2 = []
        print("==============================")
        print(f"�г���{file_name} \n����1�� {url['env1']}\n����2�� {url['env2']}")

        print("==============================")
        file_path = f'{stock_path}/{file}'
        interval_stock(file_path, url)
        time.sleep(10)  # ����5��
    print("==============================")
    print("����Ϊ�յĹ�Ʊ��")
    print(none_list)
    print("�����쳣�ĵ��г���")
    print(exception_list)
