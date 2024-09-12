#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：AutoTest
@File    ：query_index.py
@IDE     ：PyCharm
@Author  ：Qiang zhao
@Date    ：2024/8/29 14:49
"""
import codecs
import json
import math
import os
from decimal import getcontext, Decimal, ROUND_HALF_UP

import redis

# Redis服务器信息
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
# REDIS_PORT = 9264
REDIS_PASSWORD = "SseRedis@123456"
# 设置全局精度
getcontext().prec = 28
# 连接 Redis
client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
# client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
path = './TestFile'
# path = '/usr/local/datafeed/cfg/sse'
gb_files = ["SH_GBJG.txt", "SZ_GBJG.txt", "BZ_GBJG.txt"]

keys = [
    'BanKuai_SH1400',
    'BanKuai_SZ1400',
    'BanKuai_BZ1400'
]

# 获取所有key对应的值一次性批量处理
key_values = client.mget(keys)
s_values = []

for key_value in key_values:
    if key_value:
        s_values.extend('I_' + k['s'] for k in json.loads(key_value))

# 初始化结果列表
index_stocks = {}

# 将成分股索引映射与对应的BanKuai_XYZZZ一一对应
stock_mapping = {
    'I_000001.sh': 'BanKuai_SH1001',
    'I_000688.sh': 'BanKuai_SH1006',
    'I_399001.sz': 'BanKuai_SZ1001',
    'I_399003.sz': 'BanKuai_SZ1002',
    'I_399006.sz': 'BanKuai_SZ1004',
    'I_899050.bz': 'BanKuai_BZ1001',
}
# 添加两个特殊指数到stock_mapping
special_indices = {
    'BanKuai_SHSZ1001': 'BanKuai_SHSZ1001',
    'BanKuai_SHSZBZ1001': 'BanKuai_SHSZBZ1001',
}
stock_mapping.update(special_indices)
# 处理所有GB文件内容一次性读取
gb_data = {}
for gb_file_name in gb_files:
    gb_file_path = os.path.join(path, gb_file_name)
    with codecs.open(gb_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split('|')
            if len(fields) > 12:
                gb_data[fields[0].strip()] = {
                    'ltgb': fields[5].strip(),
                    'zgb': fields[12].strip()
                }

# 获取特殊指数的成分股
for index_key, redis_key in special_indices.items():
    index_stocks[index_key] = []
    bk_stocks = client.get(redis_key)
    if not bk_stocks:
        print(u"{}指数无成分股……".format(index_key))
        continue
    js_stocks = [{"s": f.get('s')} for f in json.loads(bk_stocks) if f.get('s')]
    for item in js_stocks:
        stock_code = item['s']
        first_part, second_part = stock_code.split('.')
        redis_value = client.get(second_part)
        if redis_value:
            processed_code = "{}.{}.{}".format(second_part, redis_value, first_part)
        index_stocks[index_key].append(processed_code)

for stocks in s_values:
    try:
        # 处理stock_mapping中已有的映射
        bk_stocks = client.get(stock_mapping.get(stocks, stocks))
        if not bk_stocks:
            print(u"{}指数无成分股……".format(stocks))
            continue
        js_stocks = [{"s": f.get('s')} for f in json.loads(bk_stocks) if f.get('s')]
        if js_stocks:
            redis_values = []
            for item in js_stocks:
                stock_code, suffix = item['s'].split('.')
                if suffix == 'hk':
                    continue
                redis_key = client.get(suffix)
                if redis_key:
                    formatted_code = u"{}.{}.{}".format(suffix, redis_key, stock_code)
                    redis_values.append(formatted_code)
            index_stocks[stocks] = redis_values

    except Exception as e:
        print(u"查询 Key {} 时出错: {}".format(stocks, e))

result = 'index_result.txt'
with codecs.open(result, "w", encoding='utf-8') as f:
    try:
        for stock_key, stock_value in index_stocks.items():
            GG_Total_market_value = Decimal(0)
            GG_Flow_market_value = Decimal(0)
            GG_Total_volume = Decimal(0)
            GG_Turnover_rate_denominator = Decimal(0)
            GG_SYTTM_numerator = Decimal(0)
            GG_SYTTM_denominator = Decimal(0)
            GG_SYJT_numerator = Decimal(0)
            GG_SYJT_denominator = Decimal(0)
            GG_SYDT_numerator = Decimal(0)
            GG_SYDT_denominator = Decimal(0)
            GG_SJL_numerator = Decimal(0)
            GG_SJL_denominator = Decimal(0)
            GG_total_buy = Decimal(0)
            GG_total_sell = Decimal(0)
            for a in stock_value:
                q = a.split('.')[-1]
                LastPrice = client.hmget(a, '7')
                if LastPrice is None or not LastPrice[0]:
                    LastPrice = client.hmget(a, 11)
                lp = Decimal(LastPrice[0].strip() or '0') if LastPrice and LastPrice[0] else Decimal('0')
                Volume = client.hmget(a, '13')
                cjl = Decimal(Volume[0] or '0')
                gdttm = Decimal(client.hmget(a, 'ttm')[0] or '0')
                jt = Decimal(client.hmget(a, '103')[0] or '0')
                dt = Decimal(client.hmget(a, '38')[0] or '0')
                bvps = Decimal(client.hmget(a, '28')[0] or '0')
                bv5 = sum(int(d.split('|')[0].strip()) for d in (client.hmget(a, '34')[0] or '').split(',') if d)
                sv5 = sum(int(d.split('|')[0].strip()) for d in (client.hmget(a, '36')[0] or '').split(',') if d)
                stock_data = gb_data.get(q, {})
                ltgb = stock_data.get('ltgb', '0')
                zgb = stock_data.get('zgb', '0')
                if not ltgb or ltgb == '0':
                    ltgb = client.hmget(a, 32)[0] or '0'
                if not zgb or zgb == '0':
                    zgb = client.hmget(a, 31)[0] or '0'
                GG_Total_market_value += lp * Decimal(zgb)
                GG_Flow_market_value += lp * Decimal(ltgb)
                GG_Total_volume += cjl
                GG_Turnover_rate_denominator += Decimal(ltgb)
                GG_SYTTM_numerator += lp * Decimal(zgb)
                GG_SYTTM_denominator += gdttm * Decimal(zgb) if gdttm != 0 and zgb != 0 else Decimal(0)
                GG_SYJT_numerator += lp * Decimal(zgb)
                GG_SYJT_denominator += jt * Decimal(zgb) if jt != 0 and zgb != 0 else Decimal(0)
                GG_SYDT_numerator += lp * Decimal(zgb)
                GG_SYDT_denominator += dt * Decimal(zgb) if dt != 0 and zgb != 0 else Decimal(0)
                GG_SJL_numerator += lp * Decimal(zgb)
                GG_SJL_denominator += bvps * Decimal(zgb) if bvps != 0 and zgb != 0 else Decimal(0)
                GG_total_buy += Decimal(bv5)
                GG_total_sell += Decimal(sv5)

            Total_market_value = math.floor(GG_Total_market_value / 1000)
            Flow_market_value = math.floor(GG_Flow_market_value / 1000)
            # 直接以原值输出到文件，不使用科学计数法
            total_market_value_str = "{:.0f}".format(Total_market_value)
            flow_market_value_str = "{:.0f}".format(Flow_market_value)

            # 换手率
            Turnover_rate1 = round((Decimal(GG_Total_volume) / Decimal(GG_Turnover_rate_denominator)),6) if GG_Turnover_rate_denominator != 0 else Decimal('0')
            Turnover_rate = (Decimal(Turnover_rate1) * Decimal(100)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

            # 市盈率TTM
            SYTTM_rate_Original1 = (Decimal(GG_SYTTM_numerator) / Decimal(GG_SYTTM_denominator) / Decimal(1000)) if GG_SYTTM_denominator != 0 else Decimal('0')
            SYTTM_rate_Original = SYTTM_rate_Original1.quantize(Decimal('0.000000'), rounding=ROUND_HALF_UP)

            # 市盈率静态
            SYJT_rate_Original1 = (Decimal(GG_SYJT_numerator) / Decimal(GG_SYJT_denominator) / Decimal(1000)) if GG_SYJT_denominator != 0 else Decimal('0')
            SYJT_rate_Original = SYJT_rate_Original1.quantize(Decimal('0.000000'), rounding=ROUND_HALF_UP)

            # 市盈率动态
            SYDT_rate_Original1 = (Decimal(GG_SYDT_numerator) / Decimal(GG_SYDT_denominator) / Decimal(1000)) if GG_SYDT_denominator != 0 else Decimal('0')
            SYDT_rate_Original = SYDT_rate_Original1.quantize(Decimal('0.000000'), rounding=ROUND_HALF_UP)

            # 市净率
            SJL_rate_Original1 = (Decimal(GG_SJL_numerator) / Decimal(GG_SJL_denominator) / Decimal(1000)) if GG_SJL_denominator != 0 else Decimal('0')
            SJL_rate_Original = SJL_rate_Original1.quantize(Decimal('0.000000'), rounding=ROUND_HALF_UP)
            WB_1 = round(((GG_total_buy - GG_total_sell) / (GG_total_buy + GG_total_sell)), 6) if (GG_total_buy + GG_total_sell) != 0 else Decimal('0')
            WB = (Decimal(WB_1) * Decimal(100)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

            WC = GG_total_buy - GG_total_sell
            print(u'指数：{}，总市值：{}，流通市值：{}，委比：{}，委差：{}，换手率：{}，市盈率TTM：{}，市盈率静态：{}，市盈率动态：{}，市净率：{}\n'.format(
                    stock_key, total_market_value_str, flow_market_value_str, WB, WC, Turnover_rate,SYTTM_rate_Original,SYJT_rate_Original,SYDT_rate_Original, SJL_rate_Original))
            print("{}指数Writing to file...".format(stock_key))
            f.write(u'指数：{}，总市值：{}，流通市值：{}，委比：{}，委差：{}，换手率：{}，市盈率TTM(反向)：{}，市盈率静态(反向)：{}，市盈率动态(反向)：{}，市净率(反向)：{}，\n'.format(
                    stock_key, total_market_value_str, flow_market_value_str, WB, WC, Turnover_rate,SYTTM_rate_Original,SYJT_rate_Original,SYDT_rate_Original, SJL_rate_Original))
            print(u"{}指数Write successful".format(stock_key))
    except ValueError as e:
        print("Caught a ValueError:", e)
        raise
    except Exception as e:
        print("Caught an unexpected error:", e)
        raise
