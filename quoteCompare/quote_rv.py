# -*-coding:GBK -*-
import json
import os
import sys

import zstd
from PyQt5.QtCore import QUrl

'''
rv为分量接口
此接口仅支持沪深Level2
分量数据为成交量、买量、卖量。分别对应24个区间,手和股是100倍关系，债券和股是10倍关系
分量统计定义的区间单位为股
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

# 当前日期
date1 = time.strftime('%Y%m%d', time.localtime())
# 当前时间
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
# 股名表文件路径
stock_path = f'../testCase/AllStock'
# url文件路径
url_path = f'../testCase/quote/url_rv.yaml'
# 比对结果存放路径
result_path = 'result'
# 每次请求传入的股票数量
interval = 50
# 存放快照字段
data = []
# 存放环境1快照
quote_list1 = []
# 存放环境2快照
quote_list2 = []
# 文件名称
file_name = ""
# 快照为空股票列表
none_list = []
# 请求异常的股票列表
exception_list = []

quote_map1 = {}
quote_map2 = {}


def arr_spits(item, n):
    return [item[i:i + n] for i in range(0, len(item), n)]


# 读取快照字段名文件
def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        return yaml.safe_load(fp)


# 分割股票代码
def interval_stock(path, item):
    stock_list = []
    stock_str = ''
    index = 0
    with open(path, 'r', encoding='utf-8') as stock:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        txt_list = json.load(stock)
        for st in txt_list:
            stock_list.append(st['s'])
    thread_run(stock_list, item)


# 多线程请求接口
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


# 接口请求
def request_run(stock_list, env, flag):
    print("接口调用中....")
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
                none_str = "代码：" + k + ",环境：" + env
                none_list.append(none_str)
                continue

            resp_list_quantity = str(resp_list[0]).split("\x02")
            resp_list_buy_quantity = str(resp_list[1]).split("\x02")
            resp_list_sell_quantity = str(resp_list[2]).split("\x02")

            for m in range(len(resp_list_quantity)):
                quote_dict = dict()
                quote_dict["代码"] = k + "#区间段" + str(m)
                quote_dict["量"] = resp_list_quantity[m]
                quote_dict["买量"] = resp_list_buy_quantity[m]
                quote_dict["卖量"] = resp_list_sell_quantity[m]

                if flag == 0:
                    quote_list1.append(quote_dict)
                    quote_map1[k + "#区间段" + str(m)] = quote_dict
                else:
                    quote_list2.append(quote_dict)
                    quote_map2[k + "#区间段" + str(m)] = quote_dict
        except Exception:
            exception_list.append(file_name)
            raise
# 快照比对
def compare_result(item):
    print("开始比对....")
    # print(quote_list1)
    # print(len(quote_list2))
    # list1 = key_sort_group(quote_list1, '代码')
    # list2 = key_sort_group(quote_list2, '代码')
    # print(list1)
    print("股票区间数量：", len(quote_list1))
    print("股票区间数量：", len(quote_list2))
    # 结果比对
    resp_list1 = DeepDiff(quote_list1, quote_list2, group_by='代码')
    # print(resp_list1)
    # 存放环境1数据
    envList1 = []
    # 存放环境2数据
    envList2 = []
    key_list = []
    # 存放比对不上的股票名
    code_list = []
    # 存放比对不上的字段名
    field_list = []
    # print(resp_list1)
    # 判断比对结果
    if resp_list1:
        # print("错误的：", item)
        # 获取比对不上的字段
        if 'values_changed' in resp_list1:
            values_changed = resp_list1['values_changed']
            key_list = list(values_changed.keys())
            val_list = list(values_changed.values())
            for i in val_list:
                old_value = i['old_value']
                new_value = i['new_value']
                envList1.append(old_value)
                envList2.append(new_value)
            # 截取股票代码以及字段
            for j in key_list:
                m = re.findall(r'\[\'(.*?)\'\]', j)
                code_list.append(m[0])
                field_list.append(m[1])
        # 获取多的字段
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
        #  获取少的字段
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
        json1 = {'股票名称': code_list, '字段名': field_list, item['env1']: envList1, item['env2']: envList2}
        # json1 = {'股票名称': code_list,'区间段':quj, '字段名': field_list, item['env1']: envList1, item['env2']: envList2}
        write_excel(json1, file_name)
    else:
        # print("正确的：", item)
        json1 = {'比对结果': ['完全相同']}
        write_excel(json1, file_name)
    print("比对完成写入excel")


# 排序分组
def key_sort_group(quote_list, str1):
    """对列表中dict数据指定key排序，分组"""
    quote_list.sort(key=itemgetter(str1))  # code排序；无返回值
    # print(data)
    result = dict()
    for code, items in groupby(quote_list, key=itemgetter(str1)):  # 按照code分组
        # print(type(items))
        # d = dict(ChainMap(*items))
        result[str(code)] = list(items)
    return result


def sort_dict_by_keys(d, reverse=True):
    # 这里如果不强制转换会报错，因为d.keys()的类型是：<class 'dict_keys'>，没有sort方法
    keys = list(d.keys())
    keys.sort(reverse=reverse)
    return [(key, d[key]) for key in keys]

# 结果写入excel
def write_excel(json1, item):
    # 如果文件不存在
    write_path = curPath + f'\\result\\rvResult\\{time1}_分量比对结果.xlsx'
    if not os.path.exists(write_path):
        ew = pd.ExcelWriter(write_path)
        wr = pd.DataFrame(json1)
        wr.to_excel(ew, sheet_name=item, index=False)
        ew.close()
    # 如果文件存在
    else:
        # wb = load_workbook(write_path, mode='a', engine='openpyxl')
        ew = pd.ExcelWriter(write_path, mode='a', engine='openpyxl')
        # ew.book = wb
        wr = pd.DataFrame(json1)
        wr.to_excel(ew, sheet_name=item, index=False)
        ew.close()


if '__main__' == __name__:
    # 判断存放路径是否存在
    if os.path.exists(result_path):
        pass
    else:
        os.makedirs(result_path)
    # 读取快照字段文件
    # data = quote_yaml(yaml_path)
    # 读取url文件
    compare_url = quote_yaml(url_path)
    # 读取股名表文件夹
    dirs = os.listdir(stock_path)
    # 比对环境的url
    url = None
    # 输出所有文件和文件夹
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
        # 存放环境1快照
        quote_list1 = []
        # 存放环境2快照
        quote_list2 = []
        print("==============================")
        print(f"市场：{file_name} \n环境1： {url['env1']}\n环境2： {url['env2']}")

        print("==============================")
        file_path = f'{stock_path}/{file}'
        interval_stock(file_path, url)
        time.sleep(10)  # 休眠5秒
    print("==============================")
    print("快照为空的股票：")
    print(none_list)
    print("请求异常的的市场：")
    print(exception_list)
