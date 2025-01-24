"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest 
@File    ：test.py
@IDE     ：PyCharm 
@Author  ：ZhaoQiang
@Date    ：2025/1/23 星期四 14:33 
"""
import json

import redis

# Redis 配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = "SseRedis@123456"
client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
# 数据文件路径
path = r'../../../testCase/AllStock/AllStock_sh.txt'
# 四个特殊指数
special_indices = ["000001.sh"]
special_index_codes_cfg = []
tol_zdf = 0.0
for code in special_indices:
    index_code = f"I_{code}"
    index_code_cfg = client.get(index_code)
    index = json.loads(index_code_cfg)
    for dk in index:
        special_index_codes_cfg.append(dk['s'])
    for cfg in special_index_codes_cfg:
        comp_code, comp_suffix = cfg.split('.')
        date = client.get(comp_suffix)
        quote_code = f'{comp_suffix}.{date}.{comp_code}'
        lastpx = client.hget(quote_code, 7)
        close = client.hget(quote_code, 11)
        lastpx = float(lastpx)
        close = float(close)
        zdf = abs((lastpx - close) / close) * 100
        tol_zdf += zdf
        avg = close * (1 + tol_zdf / 2244)
    print(avg)
