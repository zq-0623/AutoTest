# -*- coding: utf-8 -*-
import json

import redis
from termcolor import colored

# 配置 Redis 連接
source_redis = redis.StrictRedis(host='192.168.251.53', port=6379, db=0)
target_redis = redis.StrictRedis(host='192.168.251.54', port=6379, db=0)

# 定義 subKey 列表
## subkeys = [
##     "0", "1", "2", "3", "5", "6", "7", "8", "9", "10", "11", "ref", "13", "14", "15", "nt",
##     "18", "20", "21", "22", "23", "29", "33", "34", "35", "36", "bov", "sov", "volavg", "ir",
##     "ic", "iopv", "o7", "okey", "oir", "oic", "o18", "nzdbp", "wb", "wc", "avo", "ant", "ava"
## ]

subkeys = [
    "0", "1", "2", "5", "6", "7", "8", "9", "10", "11", "ref", "13", "14", "15", "nt",
    "18", "20", "21", "22", "23", "29", "33", "34", "35", "36", "bov", "sov", "volavg", "ir",
    "ic", "iopv", "o7", "okey", "oir", "oic", "o18", "nzdbp", "avo", "ant", "ava"
]

# 顯示開關
SHOW_MISMATCH_ONLY = True  # 設為 True 只顯示不相同的部分，False 則顯示相同和不相同的部分


# SHOW_MISMATCH_ONLY = False  # 設為 True 只顯示不相同的部分，False 則顯示相同和不相同的部分

# 提取 stock ids
def get_stock_ids():
    stock_ids = []

    # 從 AllStock_sh.txt 讀取 stock ids
    with open('/usr/local/datafeed/AllStock_sh.txt', 'r', encoding='utf-8') as f:
        stock_data = json.load(f)
        # stock_ids += [f"c_sh.20240306.{stock_id['s'].replace('.sh', '')}" for stock_id in stock_data]
        stock_ids += [f"c_sh.20240930.{stock_id['s'].replace('.sh', '')}" for stock_id in stock_data]

    # 從 Redis 獲取港股通商品的 rowkey
    hk_keys_pattern = "*_HK1"
    hk_keys = source_redis.keys(hk_keys_pattern)
    stock_ids += [key.decode('utf-8') for key in hk_keys]

    return stock_ids


# 比對兩台 Redis 上的 Rowkey 和 subkey 的數據，並根據開關進行顯示
def compare_redis_keys(stock_ids):
    for rowkey in stock_ids:
        # 從兩台 Redis 中取出相同 rowkey 和 subkeys 的值
        source_values = source_redis.hmget(rowkey, subkeys)
        target_values = target_redis.hmget(rowkey, subkeys)

        mismatch_output = []  # 用來存儲 mismatch 的輸出

        # 比對兩邊的值
        for i in range(len(subkeys)):
            source_value = source_values[i]
            target_value = target_values[i]
            subkey = subkeys[i]  # 將 subkey 變數正確對應

            # 如果來源和目標不同，記錄 mismatch
            if source_value != target_value:
                mismatch_output.append(
                    f"{subkey}: {colored(f'Src={source_value.decode() if source_value else None}', 'red')} | "
                    f"{colored(f'Dst={target_value.decode() if target_value else None}', 'red')}"
                )
            elif not SHOW_MISMATCH_ONLY:
                # 如果相同且開關為 False，則顯示綠色
                mismatch_output.append(
                    f"{subkey}: {colored(f'Src={source_value.decode() if source_value else None}', 'green')} | "
                    f"{colored(f'Dst={target_value.decode() if target_value else None}', 'green')}"
                )

        # 只顯示有 mismatch 的部分
        if mismatch_output:
            print(f"Rowkey: {rowkey}")
            print("\n".join(mismatch_output))
            print("\n")


# 獲取 stock ids
stock_ids = get_stock_ids()

# 執行比對
compare_redis_keys(stock_ids)
