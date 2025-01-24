# -*- coding: UTF-8 -*-
"""
@Project ：AutoTest
@File    ：query_redis_cal_avg.py
@IDE     ：PyCharm
@Author  ：ZhaoQiang
@Date    ：2025/1/16 星期四 14:46

从redis中获取数据，计算均价
"""
import json
from concurrent.futures import ThreadPoolExecutor

import redis

from util.base93 import decode

# Redis 配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = "SseRedis@123456"
client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
# 数据文件路径
path = r'../../../testCase/AllStock/AllStock_sh.txt'
# 四个特殊指数
special_indices = ["000001.sh", "000688.sh", "399001.sz", "399006.sz"]


def process_index_data(index_code):
    """处理单个指数代码的累计求和逻辑"""
    index_details = client.zrange(index_code, 0, -1)  # 获取 Redis 中的明细数据
    total_volume = 0.0  # 初始化成交量总和
    total_value = 0.0  # 初始化最新价*成交量的和 
    for index_detail in index_details:
        try:
            index_detail_dict = json.loads(index_detail)  # JSON 解析
            decoded_detail = {}
            for key, value in index_detail_dict.items():
                decoded_value = decode(value)
                decoded_detail[key] = decoded_value
            p_lastpx = float(decoded_detail.get('p', 0))  # 最新价
            q_volume = float(decoded_detail.get('q', 0))  # 成交量
            total_volume += q_volume
            total_value += p_lastpx * q_volume
        except Exception as e:
            print(f"处理指数明细失败: {e}, 数据: {index_detail}")
            continue

    if total_volume > 0:
        index_avg = total_value / total_volume
    else:
        index_avg = 0.0

    return {"index_code": index_code, "index_avg": index_avg}


def calculate_special_index_avg(index_code, date_str):
    """计算特殊指数的均价，公式为昨收 * (1 + 成分股涨跌幅平均值)"""
    components_key = f"I_{index_code}"
    components = client.get(components_key)
    if not components:
        print(f"未找到指数 {index_code} 的成分股信息。")
        return {"index_code": index_code, "index_avg": 0.0}

    # 按您的逻辑解析成分股数据
    try:
        index = json.loads(components)
        special_index_codes_cfg = []
        for i in index:
            special_index_codes_cfg.append(i['s'])  # 添加成分股代码
    except Exception as e:
        print(f"解析成分股失败: {e}")
        return {"index_code": index_code, "index_avg": 0.0}
    total_change_rate = 0.0  # 涨跌幅总和
    valid_components = 0  # 有效成分股计数
    for component in special_index_codes_cfg:
        try:
            comp_code, comp_suffix = component.split('.')
            component_combined_code = f"{comp_suffix}.{date_str}.{comp_code}"
            last_px = client.hget(component_combined_code, '7')  # 最新价
            close_px = client.hget(component_combined_code, '11')  # 收盘价
            if last_px is None or close_px is None:
                continue
            last_px = float(last_px)
            close_px = float(close_px)
            # 计算涨跌幅（取绝对值）
            change_rate = abs((last_px - close_px) / close_px) * 100
            total_change_rate += change_rate
            valid_components += 1
            if valid_components == 0:
                print(f"指数 {index_code} 没有有效的成分股数据。")
                return {"index_code": index_code, "index_avg": 0.0}
            avg_change_rate = total_change_rate / valid_components
            index_avg = close_px * (1 + avg_change_rate)
            return {"index_code": index_code, "index_avg": index_avg}
        except Exception as e:
            print(f"处理成分股失败: {e}, 成分股: {component}")
            continue


with open(path, 'r', encoding='utf-8') as stock:
    stock_list = json.load(stock)
    combined_codes = []
    special_codes = []
    avg_prices = []
    index_results = []
    # 分类股票代码
    for stock_i in stock_list:
        stock_s = stock_i.get('s')  # 股票代码
        stock_st = stock_i.get('st')  # 次类别
        stock_code, stock_suffix = stock_s.split('.')  # 分割股票代码
        date_str = client.get(stock_suffix)  # 获取 Redis 中的日期值
        if not stock_s or not date_str:
            continue
        # 处理特殊指数的拼接
        if stock_s in special_indices:
            special_result = calculate_special_index_avg(stock_s, date_str)
            index_results.append(special_result)
            continue
        # 普通股票的拼接逻辑
        if stock_st not in ['1400', '1420']:
            combined_code = f"{stock_suffix}.{date_str}.{stock_code}"
            combined_codes.append(combined_code)
        else:
            special_code = f"c_{stock_suffix}.{date_str}.{stock_code}_t"
            special_codes.append(special_code)
    # 计算普通股票代码的均价
    for code in combined_codes:
        volume = client.hget(code, '13')
        turnover = client.hget(code, '20')
        if volume and turnover:
            volume = float(volume)
            turnover = float(turnover)
            stock_st = None
            for stock in stock_list:
                if stock.get('s') == code.split('.')[-1]:
                    stock_st = stock.get('st')
                    break
            if stock_st in ['1300', '1311']:
                avg_price = turnover / (volume * 10)
            else:
                avg_price = turnover / volume
            avg_prices.append({"code": code, "avg_price": avg_price})

    # 使用多线程池并行处理指数代码的逻辑
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for index_code in special_codes:
            futures.append(executor.submit(process_index_data, index_code))
        for future in futures:
            index_results.append(future.result())

    # 打印结果
    print("普通拼接代码均价:")
    for avg_price in avg_prices:
        print(f"代码: {avg_price['code']}, 均价: {avg_price['avg_price']:.6f}")

    if index_code == "000001.sh":
        print("指数代码计算结果:")
        for result in index_results:
            print(f"指数代码: {result['index_code']}, 均价: {result['index_avg']:.6f}")
