# # -*-coding:GBK -*-
import json

import requests
import yaml
from deepdiff import DeepDiff

from util.base93 import decode

yaml_path = r'../testCase/quote/tick_l2.yaml'
tick_url = r'../testCase/quote/tick_l2_url.yaml'
stock_files = {
    'shl2': r'../testCase/AllStock/AllStock_sh.txt',
    'szl2': r'../testCase/AllStock/AllStock_sz.txt',
    # 'hk': r'../testCase/AllStock/AllStock_hk.txt'
}


def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        return yaml.safe_load(fp)


data = quote_yaml(yaml_path)
urls = quote_yaml(tick_url)


def SseOptionQuote(url, header, **kwargs):
    try:
        response = requests.Session().get(url, headers=header)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error while requesting url '{url}':{e}")
        return None


def compare_lists(list1, list2, symbol):
    diff = DeepDiff(list1, list2)
    if not diff:
        print("{}对比结果一致".format(symbol))
    else:
        if 'values_changed' in diff:
            values_changed = diff['values_changed']
            for key, change in values_changed.items():
                # 找到第一个单引号的位置
                start = key.find("['") + 2  # 加2是为了跳过"['"
                # 找到第二个单引号的位置
                end = key.find("']", start)
                index = key[start:end]
                old_value = change['old_value']
                new_value = change['new_value']
                print('字段：{}，环境1：{}，环境2：{}'.format(index, old_value, new_value))


def decode_quote(msg):
    results = []
    res_list = msg.split("\x04")
    for i in res_list:
        resp_list = list(filter(None, i.split('\x03')))  # 去除空字符串
        for j in resp_list:
            dic_list = json.loads(j)  # 将JSON字符串转换为字典
            dicts = {}
            data_keys = []
            data_values = []
            for d in data:
                data_keys.append(next(iter(d.keys())))  # 获取第一个键
                data_values.append(next(iter(d.values())))  # 获取第一个值
            for m, key in enumerate(data_keys):
                value = list(dic_list.values())[m]  # 获取对应的值
                if value:
                    if data_values[m] == 'Y':
                        decoded_value_str = decode(value)  # 如果标记为'Y'，解码值
                    else:
                        decoded_value_str = value  # 否则，保留原值
                    dicts[key] = decoded_value_str
            results.append(dicts)
    return results


if __name__ == '__main__':
    for key, file_path in stock_files.items():
        headers = {
            "token": "MitakeWeb",
            "param": "0,10,-1"
        }
        url_data = urls.get(key)
        if not url_data:
            print(f"未找到对应的 URL 配置：{key}")
            continue
        url1 = url_data.get('url1')
        url2 = url_data.get('url2')
        with open(file_path, 'r', encoding='utf-8') as stock_file:
            str = stock_file.read()
            stock_list = json.loads(str)
            stock_lists = []
            for stock_i in stock_list:
                if stock_i.get('t') == '1001':
                    stock_s = stock_i.get('s')
                    stock_lists.append(stock_s)
                for symbol in stock_lists:
                    headers["symbol"] = symbol
                    response1 = SseOptionQuote(url1, header=headers)
                    response2 = SseOptionQuote(url2, header=headers)
                    if response1 and response2:
                        decode_response1 = decode_quote(response1.text)
                        decode_response2 = decode_quote(response2.text)
                        if decode_response1 and decode_response2:
                            compare_lists(decode_response1, decode_response2, symbol)
                        else:
                            print(f"解码失败：{symbol}")
                    else:
                        print(f"未能获取响应：{symbol}")
