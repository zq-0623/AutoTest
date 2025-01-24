"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest
@File    ：quote_request.py
@IDE     ：PyCharm
@Author  ：ZhaoQiang
@Date    ：2025/1/16 星期四 10:21

请求快照接口计算均价

"""
import json

import redis

# Redis 配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = "SseRedis@123456"
client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

stock = "I_000001.sh"
index_stocks = client.get(stock)
cfg = json.loads(index_stocks)
for i in cfg:
    code, market = i["s"].split(".")
    date = client.get(market)
    quote_cfg = f"{market}.{date}.{code}"
    lastpx = client.hmget(quote_cfg, 7)[0]
    closePrice = client.hmget(quote_cfg, 11)[0]
    lpx_clp = abs(int(lastpx) - int(closePrice))
    print(quote_cfg, lpx_clp)
