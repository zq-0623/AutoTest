# -*-coding:GBK -*-
'''
import json
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import re
import time
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
    # print(f"接口调用中....\n",{env})
    for k in stock_list:
        header = {
            'Token': 'MitakeWeb',
            'Symbol': k,
            'Param': '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,'
                     '35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,'
                     '66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,'
                     '97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125| '
        }
        try:
            resp = requests.session().get(url=env, headers=header, verify=False)
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
    # print("resp_list1",resp_list1)
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
                # print(j)
                m = re.findall(r'\[\'(.*?)\'\]', j)
                code_list.append(m[0])
                field_list.append(m[1])
        json1 = {'股票名称': code_list, '字段名': field_list, item['env1']: envList1, item['env2']: envList2}
        write_excel(json1, file_name)
    else:
        # print("正确的：", item)
        json1 = {'比对结果': ['完全相同']}
        write_excel(json1, file_name)
    print("比对完成写入excel")


def clean_data(value):
    if isinstance(value, str):
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    return value


def sanitize_data(data):
    if isinstance(data, dict):
        return {key: sanitize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(value) for value in data]
    else:
        return clean_data(data)


# 结果写入excel
def write_excel(json1, item):
    # 如果文件不存在
    write_path = curPath + f'\\result\\quoteResult\\{time1}_请求快照比对结果.xlsx'
    sanitized_json = sanitize_data(json1)
    wr = pd.DataFrame(sanitized_json)
    if not os.path.exists(write_path):
        with pd.ExcelWriter(write_path) as ew:
            wr.to_excel(ew,sheet_name=item,index=False)
    # 如果文件存在
    else:
        with pd.ExcelWriter(write_path,mode="a",engine='openpyxl') as ew:
            wr.to_excel(ew,sheet_name=item,index=False)


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
        # print(f"市场：{file_name} \n环境1： {url['env1']}\n环境2： {url['env2']}")

        print("==============================")
        file_path = f'{stock_path}/{file}'
        print(url)
        interval_stock(file_path, url)
        time.sleep(5)  # 休眠5秒
    print("==============================")
    print("快照为空的股票：")
    print(none_list)
    print("请求异常的的市场：")
    print(exception_list)


'''
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests
import yaml
from deepdiff import DeepDiff

from util.base93 import decode

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

# 当前日期和时间
date1 = time.strftime('%Y%m%d', time.localtime())
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())

# 文件路径
yaml_path = os.path.join(rootPath, 'testCase/quote/quote.yaml')
stock_path = os.path.join(rootPath, 'testCase/AllStock')
url_path = os.path.join(rootPath, 'testCase/quote/url_quote.yaml')
result_path = os.path.join(rootPath, 'result')

interval = 200  # 每次请求传入的股票数量

none_list = []  # 快照为空股票列表
exception_list = []  # 请求异常的股票列表


def arr_spits(item, n):
    return [item[i:i + n] for i in range(0, len(item), n)]


# 读取 YAML 文件
def load_yaml(path, encoding='gbk'):
    with open(path, 'r', encoding=encoding) as fp:
        return yaml.safe_load(fp)


# 分割股票代码
def interval_stock(stock_path, interval, item, data, file_name):
    stock_list = []
    with open(stock_path, 'r', encoding='utf-8') as stock:
        txt_list = json.load(stock)
        stock_str = ''
        for i, stock_data in enumerate(txt_list):
            stock_str += stock_data['s'] + ","
            if (i + 1) % interval == 0:
                stock_list.append(stock_str.strip(','))  # 每组股票代码去掉最后的逗号
                stock_str = ''
        if stock_str:  # 加入剩余的股票
            stock_list.append(stock_str.strip(','))
    thread_run(stock_list, item, data, file_name)


# 使用线程池优化多线程请求
def thread_run(stock_list, item, data, file_name):
    quote_list1, quote_list2 = [], []
    with ThreadPoolExecutor(max_workers=8) as executor:  # 调整 max_workers，根据机器情况决定并发数
        futures = [executor.submit(request_run, stock_list, item[f'env{i + 1}'], i, data) for i in range(2)]
        for future in as_completed(futures):
            result = future.result()
            if result[1] == 0:
                quote_list1.extend(result[0])
            else:
                quote_list2.extend(result[0])
    compare_result(item, data, quote_list1, quote_list2, file_name)


# 请求函数优化，添加批量处理和重试机制
def request_run(stock_list, env, flag, data, max_retries=3):
    quote_list = []
    session = requests.Session()  # 使用 session 提升多次请求的效率
    for k in stock_list:
        header = {
            'Token': 'MitakeWeb',
            'Symbol': k,
            'Param': '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,'
                     '35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,'
                     '66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,'
                     '97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125| '
        }
        retry_count = 0
        while retry_count < max_retries:  # 重试机制
            try:
                print(f"请求URL：{env}, 股票代码：{k}")
                resp = session.get(url=env, headers=header, verify=False, timeout=5)  # 降低 timeout 到 5 秒
                resp.raise_for_status()  # 如果请求返回错误，抛出异常
                resp_list = [x for x in resp.text.split("\x03") if x]
                for m, stock_data in enumerate(resp_list):
                    split_list = stock_data.split("\x02")
                    quote_dict = {list(data[i].keys())[0]: decode(split_list[i]) if list(data[i].values())[0] == 'Y' else split_list[i] for i in range(len(split_list))}
                    if split_list[1] == '':
                        codes = k.split(',')
                        none_str = f"代码：{codes[m]}, 环境：{env}"
                        none_list.append(none_str)
                    else:
                        quote_list.append(quote_dict)
                break  # 成功请求后跳出重试循环
            except requests.exceptions.RequestException as e:
                retry_count += 1
                print(f"请求 {env} 失败，重试 {retry_count}/{max_retries} 次：{e}")
                if retry_count >= max_retries:
                    exception_list.append(env)  # 重试次数超过限制，记录异常
    return quote_list, flag


# 快照比对
def compare_result(item, data, quote_list1, quote_list2, file_name):
    print("开始比对....")
    print(f"股票数量 环境1：{len(quote_list1)}")
    print(f"股票数量 环境2：{len(quote_list2)}")

    diff = DeepDiff(quote_list1, quote_list2, group_by='代码')
    if diff:
        if 'values_changed' in diff:
            values_changed = diff['values_changed']
            code_list, field_list, envList1, envList2 = [], [], [], []
            for key, value in values_changed.items():
                envList1.append(value['old_value'])
                envList2.append(value['new_value'])
                code, field = re.findall(r"\['(.*?)'\]", key)
                code_list.append(code)
                field_list.append(field)
            result_data = {
                '股票名称': code_list,
                '字段名': field_list,
                item['env1']: envList1,
                item['env2']: envList2
            }
            write_excel(result_data, file_name)
    else:
        result_data = {'比对结果': ['完全相同']}
        write_excel(result_data, file_name)
    print("比对完成写入excel")


# 清理字符串中的非法字符
def clean_data(value):
    if isinstance(value, str):
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    return value


def sanitize_data(data):
    if isinstance(data, dict):
        return {key: sanitize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(value) for value in data]
    else:
        return clean_data(data)


def write_excel(json1, file_name):
    # 如果文件不存在
    write_path = curPath + f'\\result\\quoteResult\\{time1}_请求快照比对结果.xlsx'
    sanitized_json = sanitize_data(json1)
    wr = pd.DataFrame(sanitized_json)
    if not os.path.exists(write_path):
        with pd.ExcelWriter(write_path) as ew:
            wr.to_excel(ew, sheet_name=file_name, index=False)
    # 如果文件存在
    else:
        with pd.ExcelWriter(write_path, mode="a", engine='openpyxl') as ew:
            wr.to_excel(ew, sheet_name=file_name, index=False)


if __name__ == '__main__':
    # 创建存放路径
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # 读取配置
    data = load_yaml(yaml_path)
    compare_url = load_yaml(url_path)

    all_start_time = time.time()  # Start timing for the entire process

    for url_key, url_item in compare_url.items():
        start_time = time.time()  # Start timing for the current market

        if url_key == 'shl2':
            file_name = 'AllStock_sh.txt'
        elif url_key == 'szl2':
            file_name = 'AllStock_sz.txt'
        else:
            file_name = f"AllStock_{url_key}.txt"

        file_path = os.path.join(stock_path, file_name)
        print(f"处理股票文件：{file_name}")
        interval_stock(file_path, interval, url_item, data, url_key)

        end_time = time.time()  # End timing for the current market
        elapsed_time = end_time - start_time
        print(f"市场 {url_key} 处理耗时: {elapsed_time:.2f} 秒")

    all_end_time = time.time()  # End timing for the entire process
    all_elapsed_time = all_end_time - all_start_time
    print("==============================")
    print(f"整个处理过程耗时: {all_elapsed_time:.2f} 秒")
    print("快照为空的股票：", none_list)
    print("请求异常的市场：", exception_list)

