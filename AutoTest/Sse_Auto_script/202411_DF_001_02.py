import json

import redis

# 連接兩個 Redis 實例
redis_instance_1 = redis.StrictRedis(host='192.168.251.53', port=6379, db=0)
redis_instance_2 = redis.StrictRedis(host='192.168.251.54', port=6379, db=0)

# 讀取 stock ids
with open('/usr/local/datafeed/AllStock_sh.txt', 'r', encoding='utf-8') as f:
    stock_data = json.load(f)
    stock_ids = [stock_id['s'].replace('.sh', '') for stock_id in stock_data]

# 這是開關，可以控制是否顯示相同的資料
show_same_data = False  # 設定為 True 以顯示相同資料，False 則隱藏相同資料
# show_same_data = True  # 設定為 True 以顯示相同資料，False 則隱藏相同資料

# 需要忽略 'a' 欄位的 stock IDs
ignore_a_ids = ['000001', '000688', '399001', '399006']

for stock_id in stock_ids:
    # print(f"stockid: {stock_id}")
    k_line_key = f'sh.20240930.{stock_id}_o'
    k_line_times = redis_instance_1.zrange(k_line_key, 0, 250)

    if not k_line_times:
        # print(f"No K-line times found for stock ID: {stock_id}")
        continue

    ohlc_key_1 = f'c_sh.20240930.{stock_id}_o_h'
    ohlc_key_2 = f'c_sh.20240930.{stock_id}_o_h'  # 這裡應該是從 redis_instance_2 取得資料

    # 取得兩個 Redis 實例中的資料
    ohlc_data_1 = redis_instance_1.hmget(ohlc_key_1, *k_line_times)
    ohlc_data_2 = redis_instance_2.hmget(ohlc_key_2, *k_line_times)

    for k_line_time, data_1, data_2 in zip(k_line_times, ohlc_data_1, ohlc_data_2):
        # 解析資料
        data_1 = json.loads(data_1) if data_1 else None
        data_2 = json.loads(data_2) if data_2 else None

        # 移除不比對的欄位
        if stock_id in ignore_a_ids:
            if data_1:
                data_1.pop('a', None)
            if data_2:
                data_2.pop('a', None)

        if data_1:
            data_1.pop('ot', None)
        if data_2:
            data_2.pop('ot', None)

        # 檢查資料是否相同
        if data_1 == data_2:
            if show_same_data:
                print(
                    f"\033[92m匹配資料 - stockid: {stock_id}, K 线时间: {k_line_time}, 数据内容: {data_1}\033[0m")  # 綠色
        else:
            print(
                f"\033[91m不同資料 - stockid: {stock_id} K 线时间: {k_line_time}, \nsrc 数据内容: {data_1}, \ndst 数据内容: {data_2}\033[0m")  # 紅色
            print("-----------------------")  # 分隔線
