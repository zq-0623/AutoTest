# -*-coding:GBK -*-
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests
import yaml
from deepdiff import DeepDiff

from util.base93 import decode

yaml_path = r'../testCase/quote/tick_l2.yaml'
tick_url = r'../testCase/quote/tick_l2_url.yaml'
stock_files = {
    'shl2': r'../testCase/AllStock/AllStock_sh.txt',
    'szl2': r'../testCase/AllStock/AllStock_sz.txt',
    'hk': r'../testCase/AllStock/AllStock_hk.txt'
}


def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        return yaml.safe_load(fp)


data = quote_yaml(yaml_path)
urls = quote_yaml(tick_url)

# 使用Session复用，减少连接开销
session = requests.Session()


# 发起HTTP请求，并加入失败重试机制，增加timeout和具体异常处理
def SseOptionQuote(url, headers, retries=3, timeout=5):
    attempt = 0
    while attempt < retries:
        try:
            response = session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.Timeout:
            print(f"Timeout while requesting url '{url}' (attempt {attempt + 1}/{retries})")
        except requests.exceptions.ConnectionError:
            print(f"Connection error while requesting url '{url}' (attempt {attempt + 1}/{retries})")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error {e.response.status_code} for url '{url}' (attempt {attempt + 1}/{retries})")
        except requests.exceptions.RequestException as e:
            print(f"General error while requesting url '{url}' (attempt {attempt + 1}/{retries}): {e}")
        attempt += 1
        time.sleep(3)  # 等待2秒后重试
    print(f"请求 {url} 失败，已重试 {retries} 次。")
    return None


comparison_results = []


def compare_lists(list1, list2, symbol,decode_response1,decode_response2):
    diff = DeepDiff(list1, list2)
    if not diff:
        print(f"{symbol} 对比结果一致")
        # print(f"decode_response1: {json.dumps(decode_response1, ensure_ascii=False)}")
        # print(f"decode_response2: {json.dumps(decode_response2, ensure_ascii=False)}")
    else:
        if 'values_changed' in diff:
            values_changed = diff['values_changed']
            for key, change in values_changed.items():
                start = key.find("['") + 2
                end = key.find("']", start)
                index = key[start:end]
                old_value = change['old_value']
                new_value = change['new_value']
                comparison_results.append({
                    '代码': symbol,
                    '字段': index,
                    'old_value': old_value,
                    '环境new_value二': new_value,
                    '环境一': decode_response1,
                    '环境二': decode_response2,
                })
                # print(f'代码：{symbol}，字段：{index}，环境1：{old_value}，环境2：{new_value}')


def decode_quote(msg):
    results = []
    res_list = msg.split("\x04")
    for i in res_list:
        resp_list = list(filter(None, i.split('\x03')))
        for j in resp_list:
            dic_list = json.loads(j)
            dicts = {}
            for entry in data:
                key,decode_flag = next(iter(entry.items()))
                value = dic_list.get(key)
                if value:
                    if decode_flag == 'Y':
                        dicts[key] = decode(value)
                    else:
                        dicts[key] = value
            results.append(dicts)
    return results


# 并发处理每个 symbol 的请求
def process_symbol(symbol, url1, url2, headers):
    headers["symbol"] = symbol
    response1 = SseOptionQuote(url1, headers)
    response2 = SseOptionQuote(url2, headers)

    if response1 and response2:
        decode_response1 = decode_quote(response1)
        decode_response2 = decode_quote(response2)
        if decode_response1 and decode_response2:
            compare_lists(decode_response1, decode_response2, symbol,decode_response1,decode_response2)
        else:
            print(f"解码失败：{symbol}")
    else:
        print(f"未能获取响应：{symbol}")


if __name__ == '__main__':
    for key, file_path in stock_files.items():
        headers = {
            "token": "MitakeWeb",
            "param": "0,100,-1"
        }
        url_data = urls.get(key)
        if not url_data:
            print(f"未找到对应的 URL 配置：{key}")
            continue

        url1, url2 = url_data.get('url1'), url_data.get('url2')

        with open(file_path, 'r', encoding='utf-8') as stock_file:
            stock_list = json.loads(stock_file.read())
            # 过滤出 t != '1400' 且 t != '1420' 的股票
            # stock_lists = [stock_i['s'] for stock_i in stock_list if stock_i.get('t') not in ['1400', '1420']]
            stock_lists = [stock_i['s'] for stock_i in stock_list if stock_i.get('t') == '1001']

        # 使用线程池并发处理每个 symbol
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_symbol, symbol, url1, url2, headers) for symbol in stock_lists]
            for future in as_completed(futures):
                future.result()  # 获取结果并处理异常

df = pd.DataFrame(comparison_results)
df.to_csv('comparison_results.csv', index=False)


