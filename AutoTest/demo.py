"""
1 读取 AllStock 码表中的股票代码
2 请求两个环境的走势接口/v4/line 将返回结果进行比较
"""
import json,os,yaml
import re
from itertools import groupby
from threading import Thread
from deepdiff import DeepDiff
from util.base93 import decode
from util.logTool import logger
from util.requestTools import SseOptionQuote
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
stock_path = f"../testCase/AllStock/AllStock_bz.txt"
yaml_path = rootPath + '/testCase/quote/line.yaml'
url_path = f'../testCase/quote/url_line.yaml'
# 存放环境1走势数据
line_list1 = []
# 存放环境2走势数据
line_list2 = []


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


def read_AllStock(path):
    try:
        with open(path, 'r', encoding='utf-8') as stock:
            stocks_list = []
            stock_list = json.load(stock)
            stock_length = len(stock_list)
            for stock_i in stock_list:
                stock_s = stock_i.get('s')
                stocks_list.append(stock_s)
            # print(stocks_list)
            print("size", stock_length)
    except IOError as e:
        print("Error" + format(str(e)))
        raise
    thread_run(stocks_list,url)


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


def request_run(stock_list,env,flag):
    logger.info("接口调用环境为：%s",{env})
    stock_data = {}
    for stock in stock_list:
        header = {
            'Token': 'MitakeWeb',
            'Symbol': stock,
        }
        try:
            response = SseOptionQuote(url=env,header=header,verify=False)
            stock_data[stock] = decode_quote(response.text)
            if flag:
                line_list1.append(stock_data)
            else:
                line_list2.append(stock_data)
        except Exception as e:
            print(e)


def compare_result(item):
    logger.info("开始比对…………")
    logger.info("股票数量：%d",len(line_list1))
    logger.info("股票数量：%d",len(line_list1))
    response_list = DeepDiff(line_list1,line_list2)
    # 存放环境1数据
    envList1 = []
    # 存放环境2数据
    envList2 = []
    # # 存放比对不上的股票名
    code_list = []
    # 存放比对不上的字段名
    field_list = []
    # # 判断比对结果
    print("response_list",response_list)
    if response_list:
        # 获取比对不上的字段
        if 'values_changed' in response_list:
            values_changed = response_list['values_changed']
            key_list = list(values_changed.keys())
            val_list = list(values_changed.values())
            for i in val_list:
                old_value = i['old_value']
                new_value = i['new_value']
                envList1.append(old_value)
                envList2.append(new_value)
            for j in key_list:
                # 对比不一样的股票代码
                matches = re.findall(r'\[\'(.*?)\'\]', j)
                code_list.append(matches)


if __name__ == '__main__':
    compare_url = quote_yaml(url_path)
    for url_key in  compare_url.keys():
        url = compare_url[url_key]
    read_AllStock(stock_path)


