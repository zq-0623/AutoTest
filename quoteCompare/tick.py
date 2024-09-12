# -*-coding:GBK -*-
import asyncio
import json
import os
import time

import aiohttp
import pandas as pd
import yaml
from deepdiff import DeepDiff

from util.base93 import decode

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
yaml_path = r'../testCase/quote/tick.yaml'
tick_url = r'../testCase/quote/tick_url.yaml'
write_path = curPath + f'\\result\\tickResult\\{time1}_明细比对结果.xlsx'

stock_file_mapping = {
    'sh': r'../testCase/AllStock/AllStock_sh.txt',
    'sz': r'../testCase/AllStock/AllStock_sz.txt',
    'bz': r'../testCase/AllStock/AllStock_bz.txt',
    'csi': r'../testCase/AllStock/AllStock_csi.txt',
    'hk': r'../testCase/AllStock/AllStock_hk.txt',
}


def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        return yaml.safe_load(fp)


tick = quote_yaml(yaml_path)
tick_url = quote_yaml(tick_url)


def compare_lists(list1, list2, symbol, url1, url2, results):
    fields = [list(item.keys())[0] for item in tick]
    diff = DeepDiff(list1, list2)
    if not diff:
        print("{}对比结果一致".format(symbol))
    else:
        if 'values_changed' in diff:
            values_changed = diff['values_changed']
            for key, change in values_changed.items():
                index = int(key.split('[')[-1].split(']')[0])
                field_name = fields[index]
                old_value = change['old_value']
                new_value = change['new_value']
                results.append({'代码': symbol, '字段': field_name, url1: old_value, url2: new_value})
                print('代码：{}，字段：{}，环境1：{}，环境2：{}'.format(symbol, field_name, old_value, new_value))


async def fetch_data(session, url, headers):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_text = await response.text()
                response_str = response_text.split('\03')
                if response_str[-1] == '':
                    response_str.remove('')
                all_data = []
                if response_str:
                    for m in range(len(response_str)):
                        split_list = response_str[m].split("\x02")
                        for i in range(len(split_list)):
                            data_key = list(tick[i].keys())[0]
                            data_value = list(tick[i].values())[0]
                            if data_value == 'Y':
                                split_list[i] = decode(split_list[i])
                        params_header = response.headers.get('params', None)
                        second_value = params_header.split(',')[1]
                        headers['param'] = '{},100,1'.format(second_value)
                        all_data.append(split_list)
                return all_data
    except Exception as e:
        print(f"Error while requesting url '{url}': {e}")
        return None


async def process_symbol(session, symbol, url1, url2, results):
    headers = {
        'token': 'MitakeWeb',
        'symbol': symbol,
        'param': '0,100,-1'
    }
    evn1_tick, evn2_tick = await asyncio.gather(
        fetch_data(session, url1, headers),
        fetch_data(session, url2, headers)
    )
    if evn1_tick and evn2_tick:
        compare_lists(evn1_tick, evn2_tick, symbol, url1, url2, results)


async def process_file(session, file_path, url1, url2, results):
    if not os.path.exists(file_path):
        print("文件不存在：{}".format(file_path))
        return
    with open(file_path, 'r', encoding='utf-8') as stock_file:
        stock_list = json.load(stock_file)
        stock_symbols = [stock_item.get('s') for stock_item in stock_list]
    tasks = [process_symbol(session, symbol, url1, url2, results) for symbol in stock_symbols]
    await asyncio.gather(*tasks)


async def main():
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        with pd.ExcelWriter(write_path) as writer:
            for key, urls in tick_url.items():
                if key in stock_file_mapping:
                    file_path = stock_file_mapping[key]
                    results = []
                    env1_url = urls.get('url1')
                    env2_url = urls.get('url2')
                    if env1_url and env2_url:
                        await process_file(session, file_path, env1_url, env2_url, results)
                        if results:
                            df = pd.DataFrame(results)
                            df.to_excel(writer, sheet_name=key, index=False)
                        else:
                            print("没有{}文件, 跳过写入excel文件".format(key))

    end_time = time.time()
    total_time = end_time - start_time
    print(f"运行时间: {total_time:.2f} 秒")


if __name__ == '__main__':
    asyncio.run(main())
