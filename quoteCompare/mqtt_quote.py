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

# 当前日期
date1 = time.strftime('%Y%m%d', time.localtime())
# 当前时间
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
# 快照字段名文件路径
yaml_path = rootPath + '/testCase/quote/mqtt_quote.yaml'
# 股名表文件路径
stock_path = f'../testCase/AllStock'
# url文件路径
url_path = f'../testCase/quote/mqtt_tcp.yaml'

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

client1_topic = dict()
client2_topic = dict()


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


# 定义一个名为thread_run的函数，传入参数为stock_list和item
def thread_run(stock_list, item):
    print("推送中....")
    try:
        # 解析item中的env1值为url1
        url1 = QUrl(item["env1"])
        # 创建一个名为client1的mqtt客户端对象，指定客户端ID为quote-check-1，并指定on_message事件处理函数为on_message_1
        client1 = mqtt.Client("quote-check-1")
        client1.on_message = on_message_1
        # 连接到url1所指定的mqtt服务器，并指定连接超时时间为60秒钟
        client1.connect(url1.host(), url1.port(), 60)
        # 遍历stock_list中的每个股票代码，并依次向client1订阅其所有相关的主题
        for k in stock_list:
            for topic in str(k[:-1]).split(','):
                client1.subscribe(topic)
                client1_topic[topic] = ''
        # 开启一个新线程来处理该mqtt客户端的消息
        client1.loop_start()
    except Exception as e:
        # 遇到异常时将当前文件名加入exception_list中，并抛出异常
        exception_list.append(file_name)
        raise

    try:
        # 解析item中的env2值为url2
        url2 = QUrl(item["env2"])
        # 创建一个名为client2的mqtt客户端对象，指定客户端ID为quote-check，并指定on_message事件处理函数为on_message_2
        client2 = mqtt.Client("quote-check")
        client2.on_message = on_message_2
        # 连接到url2所指定的mqtt服务器，并指定连接超时时间为60秒钟
        client2.connect(url2.host(), url2.port(), 60)
        # 遍历stock_list中的每个股票代码，并依次向client2订阅其所有相关的主题
        for k in stock_list:
            for topic in str(k[:-1]).split(','):
                client2.subscribe(topic)
                client2_topic[topic] = ''
        # 开启一个新线程来处理该mqtt客户端的消息
        client2.loop_start()
    except Exception as e:
        # 遇到异常时将当前文件名加入exception_list中，并抛出异常
        exception_list.append(file_name)
        raise

    # 初始化循环计数器为0
    cycle_index = 0
    # 当client1_topic和client2_topic中还存在值时，循环推送数据
    while len(client1_topic) != 0 or len(client2_topic) != 0:
        print("推送数据处理中...")
        # 当循环计数器大于等于30时，跳出循环
        if cycle_index >= 30:
            break
        # 将循环计数器加1
        cycle_index = cycle_index + 1
        time.sleep(10)

    # 断开client1和client2的连接
    client1.disconnect()
    client2.disconnect()

    compare_result(item)


# 定义一个名为on_message_1的事件处理函数，传入参数为client、userdata、msg
def on_message_1(client, userdata, msg):
    # 解压缩msg.payload的数据并转换为utf8编码格式
    data_all = zstd.decompress(msg.payload).decode('utf8')
    # 若解压缩后的数据小于等于1个，则将该消息的主题和环境信息加入none_list中，并从client1_topic中移除该主题
    if len(str(data_all).split("\x02")) <= 1:
        none_str = "代码：" + msg.topic + ",环境：" + str(client._host)
        none_list.append(none_str)
        client1_topic.pop(msg.topic, '')
        return
    # 定义一个字典结构的变量quote_dict和一个字典结构的变量dataMap
    quote_dict = {}
    dataMap = {}
    # 遍历data_all中的每个数据块，将其按照“=”符号进行拆分并存储到dataMap中
    for d in str(data_all).split("\x02"):
        ds = d.split('=')
        if len(ds) >= 2:
            dataMap[ds[0]] = ds[1]
    # 遍历data中的每个数据项
    for d in data:
        # 若该数据项的代码不在dataMap中、dataMap中的值为空或者值为''，则将quote_dict中该数据项的值设为空字符串
        if d[0] not in dataMap or dataMap[d[0]] is None or dataMap[d[0]] == '':
            quote_dict[d[1]] = ''
        # 否则，在quote_dict中为该数据项的值解码并存储在quote_dict中
        elif d[2] == 'Y':
            quote_dict[d[1]] = decode(dataMap[d[0]])
        else:
            quote_dict[d[1]] = dataMap[d[0]]
    # 将quote_dict加入quote_list1中
    quote_list1.append(quote_dict)
    # 取消该主题的订阅，并从client1_topic中移除该主题
    client.unsubscribe(msg.topic)
    client1_topic.pop(msg.topic, '')


# 定义一个名为on_message_2的事件处理函数，传入参数为client、userdata、msg
def on_message_2(client, userdata, msg):
    # 解压缩msg.payload的数据并转换为utf8编码格式
    data_all = zstd.decompress(msg.payload).decode('utf8')
    # 若解压缩后的数据小于等于1个，则将该消息的主题和环境信息加入none_list中，并从client2_topic中移除该主题
    if len(str(data_all).split("\x02")) <= 1:
        none_str = "代码：" + msg.topic + ",环境：" + str(client._host)
        none_list.append(none_str)
        client2_topic.pop(msg.topic, '')
        return
    # 定义一个字典结构的变量quote_dict和一个字典结构的变量dataMap
    quote_dict = {}
    dataMap = {}
    # 遍历data_all中的每个数据块，将其按照“=”符号进行拆分并存储到dataMap中
    for d in str(data_all).split("\x02"):
        ds = d.split('=')
        if len(ds) >= 2:
            dataMap[ds[0]] = ds[1]
    # 遍历data中的每个数据项
    for d in data:
        # 若该数据项的代码不在dataMap中、dataMap中的值为空或者值为''，则将quote_dict中该数据项的值设为空字符串
        if d[0] not in dataMap or dataMap[d[0]] is None or dataMap[d[0]] == '':
            quote_dict[d[1]] = ''
        # 否则，在quote_dict中为该数据项的值解码并存储在quote_dict中
        elif d[2] == 'Y':
            quote_dict[d[1]] = decode(dataMap[d[0]])
        else:
            quote_dict[d[1]] = dataMap[d[0]]
    # 将quote_dict加入quote_list2中
    quote_list2.append(quote_dict)
    # 取消该主题的订阅，并从client2_topic中移除该主题
    client.unsubscribe(msg.topic)
    client2_topic.pop(msg.topic, '')


# 快照比对
def compare_result(item):
    print("开始比对....")
    # print(quote_list1)
    # print(len(quote_list2))
    # list1 = key_sort_group(quote_list1, '代码')
    # list2 = key_sort_group(quote_list2, '代码')
    # print(list1)
    print("股票数量：", len(quote_list1))
    print("股票数量：", len(quote_list2))
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
    write_path = curPath + f'\\result\\mqttResult\\{time1}_推送快照比对结果.xlsx'
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