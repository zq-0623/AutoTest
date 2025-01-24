#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：AutoTest 
@File    ：query_redis_keys.py
@IDE     ：PyCharm 
@Author  ：Qiang zhao
@Date    ：2024/9/13 13:59 
"""
import json

import redis

# Redis服务器信息
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 9264
REDIS_PASSWORD = "SseRedis@123456"

OUTPUT_FILE = "output.txt"
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

'''
# 查询 BanKuai_SH*、BanKuai_SZ* 和 BanKuai_BZ* 的所有键
除了14开头的板块文件夹

keys_sh = r.keys("BanKuai_SH*")
keys_sz = r.keys("BanKuai_SZ*")
keys_bz = r.keys("BanKuai_BZ*")

# 合并键并排除以 14 开头的键
keys = []
for key in keys_sh + keys_sz + keys_bz:
    if not key.startswith(("BanKuai_SH14", "BanKuai_SZ14", "BanKuai_BZ14")):
        keys.append(key)
'''

keys_sh = r.keys("BanKuai_SH14*")
keys_sz = r.keys("BanKuai_SZ14*")
keys_bz = r.keys("BanKuai_BZ14*")
keys = keys_sh + keys_sz + keys_bz
s_values = set()
for key in keys:
    key_value = r.get(key)
    if key_value:
        try:
            json_data = json.loads(key_value)
            for item in json_data:
                if 's' in item:
                    s_values.add(item['s'])
        except ValueError:
            print("Error decoding JSON for key:", key)

redis_values = set()

for item in s_values:
    parts = item.split('.')
    stock_code = parts[0]
    suffix = parts[1]
    if suffix == 'sh':
        redis_key = r.get("sh")
    elif suffix == 'sz':
        redis_key = r.get("sz")
    elif suffix == 'bz':
        redis_key = r.get("bz")
    else:
        redis_key = None
    if redis_key:
        formatted_code = "{}.{}.{}".format(suffix, redis_key, stock_code)
        redis_values.add(formatted_code)

with open(OUTPUT_FILE, "w") as f:
    for a in redis_values:
        turnover_rate = r.hget(a, "15")
        total_market_value = r.hget(a, "26")
        flow_market_value = r.hget(a, "27")
        wb = r.hget(a, "wb")
        wc = r.hget(a, "wc")
        syttm_rate = r.hget(a, "ttm")
        syjt_rate = r.hget(a, "103")
        sydt_rate = r.hget(a, "38")
        sjl_rate = r.hget(a, "28")
        f.write("指数代码:{}, 换手率:{}, 总市值:{}, 流通市值:{}, 委比:{}, 委差:{}, 市盈率TTM:{}, 市净率静态:{}, 市盈率动态:{}, 市净率:{}\n".format(
            a, turnover_rate, total_market_value, flow_market_value, wb, wc, syttm_rate, syjt_rate, sydt_rate, sjl_rate))
