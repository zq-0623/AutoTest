# -*-coding:GBK -*-
import json
import os
import sys

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

# ��ǰ����
date1 = time.strftime('%Y%m%d', time.localtime())
# ��ǰʱ��
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
# �����ֶ����ļ�·��
yaml_path = rootPath + '/testCase/quote/quote.yaml'
# �������ļ�·��
stock_path = f'../testCase/AllStock'
# url�ļ�·��
url_path = f'../testCase/quote/url_quote.yaml'
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
        txt_length = len(txt_list)
        # �������Ʊ����ȡ��
        num = txt_length % interval
        # ÿintervalֻȡ���������еĹ�Ʊ����
        # �����ܱ�interval����ʱ
        if num == 0:
            for m in range(txt_length):
                stock_str = stock_str + txt_list[m]['s'] + ","
                index = index + 1
                if index >= interval:
                    stock_list.append(stock_str)
                    index = 0
                    stock_str = ''
        # ����С��intervalʱ
        elif num == txt_length:
            for m in range(txt_length):
                stock_str = stock_str + txt_list[m]['s'] + ","
                stock_list.append(stock_str)
        # �������ܱ�interval����ʱ
        else:
            for m in range(txt_length):
                stock_str = stock_str + txt_list[m]['s'] + ","
                index = index + 1
                if index >= interval:
                    stock_list.append(stock_str)
                    index = 0
                    stock_str = ''
                if m == (txt_length - 1):
                    stock_list.append(stock_str)
    thread_run(stock_list, item)


# ���߳�����ӿ�
def thread_run(stock_list, item):
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
    print(f"�ӿڵ�����....",{env})
    for k in stock_list:
        header = {
            'Token': 'MitakeWeb',
            'Symbol': k,
            'Param': '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,'
                     '35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,'
                     '66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,'
                     '97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117| '
        }
        try:
            resp = requests.session().get(url=env, headers=header,verify=False)
            resp_list = resp.text.split("\x03")
            if resp_list[-1] == '':
                resp_list.remove('')
            for m in range(len(resp_list)):
                split_list = resp_list[m].split("\x02")
                quote_dict = dict()
                for i in range(len(split_list)):
                    data_key = list(data[i].keys())[0]
                    data_value = list(data[i].values())[0]
                    # �жϸ��ֶ��Ƿ�ѹ��
                    if data_value == 'Y':
                        # �ֶ�valueת��
                        split_list[i] = decode(split_list[i])
                    quote_dict[data_key] = split_list[i]
                # # ȥ����ע����Ӱ����ֶ�
                # zcz_dict = quote_dict['����������Ϣ��۹�ͨ��ʶ������ȯ��ʶjson��ʽ']
                # zcz_list = ['vie', 'upf', 'vote', 'reg', 'cdr', 'dtrad', 'ZSSSL']
                # if quote_dict['����������Ϣ��۹�ͨ��ʶ������ȯ��ʶjson��ʽ']:
                #     # print(type(quote_dict['����������Ϣ��۹�ͨ��ʶ������ȯ��ʶjson��ʽ']))
                #     quote_dict['����������Ϣ��۹�ͨ��ʶ������ȯ��ʶjson��ʽ'] = list(quote_dict['����������Ϣ��۹�ͨ��ʶ������ȯ��ʶjson��ʽ'])

                #     #     for zcz in zcz_list:
                #     #         if zcz in quote_dict['����������Ϣ��۹�ͨ��ʶ������ȯ��ʶjson��ʽ']:
                #     #             quote_dict['����������Ϣ��۹�ͨ��ʶ������ȯ��ʶjson��ʽ'].pop(zcz)
                #     quote_dict['����������Ϣ��۹�ͨ��ʶ������ȯ��ʶjson��ʽ'] = sort_dict_by_keys(quote_dict['����������Ϣ��۹�ͨ��ʶ������ȯ��ʶjson��ʽ'])
                # if quote_dict['�����޼۲���(�������ֵ)']:
                #     quote_dict['�����޼۲���(�������ֵ)'].pop('�����޼۲���(�������ֵ)')
                # �ҳ�����Ϊ�յĹ�Ʊ
                if split_list[1] == '':
                    codes = k.split(',')
                    none_str = "���룺" + codes[m] + ",������" + env
                    none_list.append(none_str)
                else:
                    if flag == 0:
                        quote_list1.append(quote_dict)
                    else:
                        quote_list2.append(quote_dict)
        except Exception as e:
            exception_list.append(file_name)
            raise


# ���ձȶ�
def compare_result(item):
    print("��ʼ�ȶ�....")
    print("��Ʊ������", len(quote_list1))
    print("��Ʊ������", len(quote_list2))
    # ����ȶ�
    resp_list1 = DeepDiff(quote_list1, quote_list2, group_by='����')
    # ��Ż���1����
    envList1 = []
    # ��Ż���2����
    envList2 = []
    # ��űȶԲ��ϵĹ�Ʊ��
    code_list = []
    # ��űȶԲ��ϵ��ֶ���
    field_list = []
    # �жϱȶԽ��
    if resp_list1:
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
                print(j)
                m = re.findall(r'\[\'(.*?)\'\]', j)
                code_list.append(m[0])
                field_list.append(m[1])
        # ��ȡ����ֶ�
        # if 'iterable_item_added' in resp_list1:
        #     iterable_item_added = resp_list1['iterable_item_added']
        #     print(iterable_item_added)
        #     # code_list.append(iterable_item_added)
        # # ��ȡ�ٵ��ֶ�
        # if 'iterable_item_removed' in resp_list1:
        #     iterable_item_removed = resp_list1['iterable_item_removed']
        #     print(iterable_item_removed)
        # code_list.append(iterable_item_removed)
        # print(code_list)
        json1 = {'��Ʊ����': code_list, '�ֶ���': field_list, item['env1']: envList1, item['env2']: envList2}
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
    result = dict()
    for code, items in groupby(quote_list, key=itemgetter(str1)):  # ����code����
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
    write_path = curPath + f'\\result\\quoteResult\\{time1}_������ձȶԽ��.xlsx'
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
    data = quote_yaml(yaml_path)
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
        # if url_key == "sh":
        #     url = compare_url[url_key]
        # if url_key == "sz":
        #     url = compare_url[url_key]
        if url_key == "bz":
            url = compare_url[url_key]
        # if url_key == "csi":
        #     url = compare_url[url_key]
        # if url_key == "hk":
        #     url = compare_url[url_key]
        # if url_key == "shl2":
        #     url = compare_url[url_key]
        #     file = "AllStock_sh.txt"
        # if url_key == "szl2":
        #     url = compare_url[url_key]
        #     file = "AllStock_sz.txt"
        # ��Ż���1����
        quote_list1 = []
        # ��Ż���2����
        quote_list2 = []
        print("==============================")
        print(f"�г���{file_name} \n����1�� {url['env1']}\n����2�� {url['env2']}")

        print("==============================")
        file_path = f'{stock_path}/{file}'
        interval_stock(file_path, url)
        time.sleep(5)  # ����5��
    print("==============================")
    print("����Ϊ�յĹ�Ʊ��")
    print(none_list)
    print("�����쳣�ĵ��г���")
    print(exception_list)
