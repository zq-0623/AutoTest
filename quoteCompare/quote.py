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

# 当前日期
date1 = time.strftime('%Y%m%d', time.localtime())
# 当前时间
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
# 快照字段名文件路径
yaml_path = rootPath + '/testCase/quote/quote.yaml'
# 股名表文件路径
stock_path = f'../testCase/AllStock'
# url文件路径
url_path = f'../testCase/quote/url_quote.yaml'
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
        txt_length = len(txt_list)
        # 股名表股票数量取余
        num = txt_length % interval
        # 每interval只取出股名表中的股票代码
        # 数量能被interval整除时
        if num == 0:
            for m in range(txt_length):
                stock_str = stock_str + txt_list[m]['s'] + ","
                index = index + 1
                if index >= interval:
                    stock_list.append(stock_str)
                    index = 0
                    stock_str = ''
        # 数量小于interval时
        elif num == txt_length:
            for m in range(txt_length):
                stock_str = stock_str + txt_list[m]['s'] + ","
                stock_list.append(stock_str)
        # 数量不能被interval整除时
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


# 多线程请求接口
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


# 接口请求
def request_run(stock_list, env, flag):
    print(f"接口调用中....",{env})
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
                    # 判断该字段是否压缩
                    if data_value == 'Y':
                        # 字段value转码
                        split_list[i] = decode(split_list[i])
                    quote_dict[data_key] = split_list[i]
                # # 去除受注册制影响的字段
                # zcz_dict = quote_dict['个股其他信息如港股通标识融资融券标识json格式']
                # zcz_list = ['vie', 'upf', 'vote', 'reg', 'cdr', 'dtrad', 'ZSSSL']
                # if quote_dict['个股其他信息如港股通标识融资融券标识json格式']:
                #     # print(type(quote_dict['个股其他信息如港股通标识融资融券标识json格式']))
                #     quote_dict['个股其他信息如港股通标识融资融券标识json格式'] = list(quote_dict['个股其他信息如港股通标识融资融券标识json格式'])

                #     #     for zcz in zcz_list:
                #     #         if zcz in quote_dict['个股其他信息如港股通标识融资融券标识json格式']:
                #     #             quote_dict['个股其他信息如港股通标识融资融券标识json格式'].pop(zcz)
                #     quote_dict['个股其他信息如港股通标识融资融券标识json格式'] = sort_dict_by_keys(quote_dict['个股其他信息如港股通标识融资融券标识json格式'])
                # if quote_dict['竞价限价参数(仅深交所有值)']:
                #     quote_dict['竞价限价参数(仅深交所有值)'].pop('竞价限价参数(仅深交所有值)')
                # 找出快照为空的股票
                if split_list[1] == '':
                    codes = k.split(',')
                    none_str = "代码：" + codes[m] + ",环境：" + env
                    none_list.append(none_str)
                else:
                    if flag == 0:
                        quote_list1.append(quote_dict)
                    else:
                        quote_list2.append(quote_dict)
        except Exception as e:
            exception_list.append(file_name)
            raise


# 快照比对
def compare_result(item):
    print("开始比对....")
    print("股票数量：", len(quote_list1))
    print("股票数量：", len(quote_list2))
    # 结果比对
    resp_list1 = DeepDiff(quote_list1, quote_list2, group_by='代码')
    # 存放环境1数据
    envList1 = []
    # 存放环境2数据
    envList2 = []
    # 存放比对不上的股票名
    code_list = []
    # 存放比对不上的字段名
    field_list = []
    # 判断比对结果
    if resp_list1:
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
                print(j)
                m = re.findall(r'\[\'(.*?)\'\]', j)
                code_list.append(m[0])
                field_list.append(m[1])
        # 获取多的字段
        # if 'iterable_item_added' in resp_list1:
        #     iterable_item_added = resp_list1['iterable_item_added']
        #     print(iterable_item_added)
        #     # code_list.append(iterable_item_added)
        # # 获取少的字段
        # if 'iterable_item_removed' in resp_list1:
        #     iterable_item_removed = resp_list1['iterable_item_removed']
        #     print(iterable_item_removed)
        # code_list.append(iterable_item_removed)
        # print(code_list)
        json1 = {'股票名称': code_list, '字段名': field_list, item['env1']: envList1, item['env2']: envList2}
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
    result = dict()
    for code, items in groupby(quote_list, key=itemgetter(str1)):  # 按照code分组
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
    write_path = curPath + f'\\result\\quoteResult\\{time1}_请求快照比对结果.xlsx'
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
    data = quote_yaml(yaml_path)
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
        # 存放环境1快照
        quote_list1 = []
        # 存放环境2快照
        quote_list2 = []
        print("==============================")
        print(f"市场：{file_name} \n环境1： {url['env1']}\n环境2： {url['env2']}")

        print("==============================")
        file_path = f'{stock_path}/{file}'
        interval_stock(file_path, url)
        time.sleep(5)  # 休眠5秒
    print("==============================")
    print("快照为空的股票：")
    print(none_list)
    print("请求异常的的市场：")
    print(exception_list)
