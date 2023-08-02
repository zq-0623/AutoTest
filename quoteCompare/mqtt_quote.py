# -*-coding:GBK -*-
import json
import os
import sys

import zstd
from PyQt5.QtCore import QUrl

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import re
import time
from itertools import groupby
from operator import itemgetter

import pandas as pd
import yaml
from deepdiff import DeepDiff
from util.base93 import decode

import paho.mqtt.client as mqtt

# ��ǰ����
date1 = time.strftime('%Y%m%d', time.localtime())
# ��ǰʱ��
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
# �����ֶ����ļ�·��
yaml_path = rootPath + '/testCase/quote/mqtt_quote.yaml'
# �������ļ�·��
stock_path = f'../testCase/AllStock'
# url�ļ�·��
url_path = f'../testCase/quote/mqtt_tcp.yaml'

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

client1_topic = dict()
client2_topic = dict()


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


# ����һ����Ϊthread_run�ĺ������������Ϊstock_list��item
def thread_run(stock_list, item):
    print("������....")
    try:
        # ����item�е�env1ֵΪurl1
        url1 = QUrl(item["env1"])
        # ����һ����Ϊclient1��mqtt�ͻ��˶���ָ���ͻ���IDΪquote-check-1����ָ��on_message�¼�������Ϊon_message_1
        client1 = mqtt.Client("quote-check-1")
        client1.on_message = on_message_1
        # ���ӵ�url1��ָ����mqtt����������ָ�����ӳ�ʱʱ��Ϊ60����
        client1.connect(url1.host(), url1.port(), 60)
        # ����stock_list�е�ÿ����Ʊ���룬��������client1������������ص�����
        for k in stock_list:
            for topic in str(k[:-1]).split(','):
                client1.subscribe(topic)
                client1_topic[topic] = ''
        # ����һ�����߳��������mqtt�ͻ��˵���Ϣ
        client1.loop_start()
    except Exception as e:
        # �����쳣ʱ����ǰ�ļ�������exception_list�У����׳��쳣
        exception_list.append(file_name)
        raise

    try:
        # ����item�е�env2ֵΪurl2
        url2 = QUrl(item["env2"])
        # ����һ����Ϊclient2��mqtt�ͻ��˶���ָ���ͻ���IDΪquote-check����ָ��on_message�¼�������Ϊon_message_2
        client2 = mqtt.Client("quote-check")
        client2.on_message = on_message_2
        # ���ӵ�url2��ָ����mqtt����������ָ�����ӳ�ʱʱ��Ϊ60����
        client2.connect(url2.host(), url2.port(), 60)
        # ����stock_list�е�ÿ����Ʊ���룬��������client2������������ص�����
        for k in stock_list:
            for topic in str(k[:-1]).split(','):
                client2.subscribe(topic)
                client2_topic[topic] = ''
        # ����һ�����߳��������mqtt�ͻ��˵���Ϣ
        client2.loop_start()
    except Exception as e:
        # �����쳣ʱ����ǰ�ļ�������exception_list�У����׳��쳣
        exception_list.append(file_name)
        raise

    # ��ʼ��ѭ��������Ϊ0
    cycle_index = 0
    # ��client1_topic��client2_topic�л�����ֵʱ��ѭ����������
    while len(client1_topic) != 0 or len(client2_topic) != 0:
        print("�������ݴ�����...")
        # ��ѭ�����������ڵ���30ʱ������ѭ��
        if cycle_index >= 30:
            break
        # ��ѭ����������1
        cycle_index = cycle_index + 1
        time.sleep(10)

    # �Ͽ�client1��client2������
    client1.disconnect()
    client2.disconnect()

    compare_result(item)


# ����һ����Ϊon_message_1���¼����������������Ϊclient��userdata��msg
def on_message_1(client, userdata, msg):
    # ��ѹ��msg.payload�����ݲ�ת��Ϊutf8�����ʽ
    data_all = zstd.decompress(msg.payload).decode('utf8')
    # ����ѹ���������С�ڵ���1�����򽫸���Ϣ������ͻ�����Ϣ����none_list�У�����client1_topic���Ƴ�������
    if len(str(data_all).split("\x02")) <= 1:
        none_str = "���룺" + msg.topic + ",������" + str(client._host)
        none_list.append(none_str)
        client1_topic.pop(msg.topic, '')
        return
    # ����һ���ֵ�ṹ�ı���quote_dict��һ���ֵ�ṹ�ı���dataMap
    quote_dict = {}
    dataMap = {}
    # ����data_all�е�ÿ�����ݿ飬���䰴�ա�=�����Ž��в�ֲ��洢��dataMap��
    for d in str(data_all).split("\x02"):
        ds = d.split('=')
        if len(ds) >= 2:
            dataMap[ds[0]] = ds[1]
    # ����data�е�ÿ��������
    for d in data:
        # ����������Ĵ��벻��dataMap�С�dataMap�е�ֵΪ�ջ���ֵΪ''����quote_dict�и��������ֵ��Ϊ���ַ���
        if d[0] not in dataMap or dataMap[d[0]] is None or dataMap[d[0]] == '':
            quote_dict[d[1]] = ''
        # ������quote_dict��Ϊ���������ֵ���벢�洢��quote_dict��
        elif d[2] == 'Y':
            quote_dict[d[1]] = decode(dataMap[d[0]])
        else:
            quote_dict[d[1]] = dataMap[d[0]]
    # ��quote_dict����quote_list1��
    quote_list1.append(quote_dict)
    # ȡ��������Ķ��ģ�����client1_topic���Ƴ�������
    client.unsubscribe(msg.topic)
    client1_topic.pop(msg.topic, '')


# ����һ����Ϊon_message_2���¼����������������Ϊclient��userdata��msg
def on_message_2(client, userdata, msg):
    # ��ѹ��msg.payload�����ݲ�ת��Ϊutf8�����ʽ
    data_all = zstd.decompress(msg.payload).decode('utf8')
    # ����ѹ���������С�ڵ���1�����򽫸���Ϣ������ͻ�����Ϣ����none_list�У�����client2_topic���Ƴ�������
    if len(str(data_all).split("\x02")) <= 1:
        none_str = "���룺" + msg.topic + ",������" + str(client._host)
        none_list.append(none_str)
        client2_topic.pop(msg.topic, '')
        return
    # ����һ���ֵ�ṹ�ı���quote_dict��һ���ֵ�ṹ�ı���dataMap
    quote_dict = {}
    dataMap = {}
    # ����data_all�е�ÿ�����ݿ飬���䰴�ա�=�����Ž��в�ֲ��洢��dataMap��
    for d in str(data_all).split("\x02"):
        ds = d.split('=')
        if len(ds) >= 2:
            dataMap[ds[0]] = ds[1]
    # ����data�е�ÿ��������
    for d in data:
        # ����������Ĵ��벻��dataMap�С�dataMap�е�ֵΪ�ջ���ֵΪ''����quote_dict�и��������ֵ��Ϊ���ַ���
        if d[0] not in dataMap or dataMap[d[0]] is None or dataMap[d[0]] == '':
            quote_dict[d[1]] = ''
        # ������quote_dict��Ϊ���������ֵ���벢�洢��quote_dict��
        elif d[2] == 'Y':
            quote_dict[d[1]] = decode(dataMap[d[0]])
        else:
            quote_dict[d[1]] = dataMap[d[0]]
    # ��quote_dict����quote_list2��
    quote_list2.append(quote_dict)
    # ȡ��������Ķ��ģ�����client2_topic���Ƴ�������
    client.unsubscribe(msg.topic)
    client2_topic.pop(msg.topic, '')


# ���ձȶ�
def compare_result(item):
    print("��ʼ�ȶ�....")
    # print(quote_list1)
    # print(len(quote_list2))
    # list1 = key_sort_group(quote_list1, '����')
    # list2 = key_sort_group(quote_list2, '����')
    # print(list1)
    print("��Ʊ������", len(quote_list1))
    print("��Ʊ������", len(quote_list2))
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
    write_path = curPath + f'\\result\\mqttResult\\{time1}_���Ϳ��ձȶԽ��.xlsx'
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
        if url_key == "sh":
            url = compare_url[url_key]
        if url_key == "sz":
            url = compare_url[url_key]
        if url_key == "bz":
            url = compare_url[url_key]
        if url_key == "csi":
            url = compare_url[url_key]
        if url_key == "hk":
            url = compare_url[url_key]
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