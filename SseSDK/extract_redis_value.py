#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：AutoTest
@File    ：extract_redis_value.py
@IDE     ：PyCharm
@Author  ：Qiang zhao
@Date    ：2024/8/30 13:58
"""
import json

import pandas as pd
import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

path = './TestFile'
gb_files = ["SH_GBJG.txt", "SZ_GBJG.txt", "BZ_GBJG.txt"]

keys = [
    'BanKuai_SH1400',
    'BanKuai_SZ1400',
    'BanKuai_BZ1400'
]

key_values = client.mget(keys)
s_values = []

for key_value in key_values:
    if key_value:
        data = json.loads(key_value)
        for item in data:
            s_values.append('I_' + item['s'])

stock_mapping = {
    'I_000001.sh': 'BanKuai_SH1001',
    'I_000688.sh': 'BanKuai_SH1006',
    'I_399001.sz': 'BanKuai_SZ1001',
    'I_399006.sz': 'BanKuai_SZ1004',
    'I_899050.bz': 'BanKuai_BZ1001',
}

redis_keys_to_query = ['7', '11', '13', 'ttm', '103', '38', '28']

index_stocks = {}
for stocks in s_values:
    try:
        bk_stocks = client.get(stock_mapping.get(stocks, stocks))
        if not bk_stocks:
            print(f"{stocks}指数无成分股……")
            continue
        js_stocks = json.loads(bk_stocks)
        redis_values = []
        for item in js_stocks:
            stock_code = item.get('s')
            if stock_code:
                split_code = stock_code.split('.')
                if len(split_code) == 2:
                    code, suffix = split_code
                    redis_key = client.get(suffix)
                    if redis_key:
                        formatted_code = f"{suffix}.{redis_key}.{code}"
                        redis_values.append(formatted_code)
        index_stocks[stocks] = redis_values
    except Exception as e:
        print(f"查询 Key {stocks} 时出错: {e}")

data = []

for index, stock_list in index_stocks.items():
    for stock in stock_list:
        row = {'Index': index, 'Stock': stock}
        for redis_key in redis_keys_to_query:
            value = client.hget(stock, redis_key)
            if redis_key == '7':
                if not value:
                    value = client.hget(stock, '11')
                if not value:
                    value = '0'
            row[redis_key] = value if value else '0'
        data.append(row)

extra_data = {}

# 处理 gb_files 文件
for gb_file in gb_files:
    file_path = f"{path}/{gb_file}"
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()[1:]
        for line in lines:
            fields = line.strip().split('|')
            if len(fields) >= 13:
                code = fields[0]
                field_13 = fields[12] if fields[12] and fields[12] != '0' else None
                field_6 = fields[5] if fields[5] and fields[5] != '0' else None

                # 如果 field_13 和 field_6 是空值或零，则从 Redis 查询
                if field_13 is None or field_13 == '0':
                    field_13 = client.hget(code, '31')
                if field_6 is None or field_6 == '0':
                    field_6 = client.hget(code, '32')

                extra_data[code] = {'field_13': field_13 if field_13 else '0', 'field_6': field_6 if field_6 else '0'}

# 处理数据行，添加额外字段
for row in data:
    stock_code = row['Stock'].split('.')[-1]
    # 如果 stock_code 在 extra_data 中找不到，则从 Redis 中获取
    if stock_code not in extra_data:
        field_13 = client.hget(stock_code, '31')
        field_6 = client.hget(stock_code, '32')
        extra_data[stock_code] = {
            'field_13': field_13 if field_13 else '0',
            'field_6': field_6 if field_6 else '0'
        }

    row['ExtraField_13'] = extra_data.get(stock_code, {}).get('field_13', '0')
    row['ExtraField_6'] = extra_data.get(stock_code, {}).get('field_6', '0')

output_file = 'index_stocks2.xlsx'
df = pd.DataFrame(data, columns=['Index', 'Stock'] + redis_keys_to_query + ['ExtraField_13', 'ExtraField_6'])

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False)

print(f"Data saved to {output_file}")
