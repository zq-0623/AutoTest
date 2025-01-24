# -*- coding: UTF-8 -*-
"""
@Project ：AutoTest
@File    ：AddValue_compare_all.py
@IDE     ：PyCharm
@Author  ：ZhaoQiang
@Date    ：2024/12/6 星期五 15:49
"""
import json
import time

import requests
import yaml

from util.logTool import logger

# stock_path = r'../../../testCase/AllStock/AllStock_sz.txt'
stock_path = r'../../../testCase/AllStock/AllStock_sh.txt'
yaml_file = 'AddValue.yaml'  # 请替换为实际 YAML 文件路径


def load_yaml_data(yaml_file):
    with open(yaml_file, 'r', encoding='gbk') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    if isinstance(data, list):
        field = [list(item.keys())[0] for item in data if isinstance(item, dict)]
        return field
    else:
        print("YAML 数据格式错误，期望列表字典格式")
        return []


def extract_stock(path):
    try:
        with open(path, 'r', encoding='utf-8') as stock:
            stock_list = json.load(stock)
            stock_list = [stock_i.get('s') for stock_i in stock_list]
    except IOError as e:
        print("Error：" + format(str(e)))
        raise
    return stock_list


stock_symbols = extract_stock(stock_path)
symbols_per_request = 15  # 可以设置为需要的数量
headers = {
    'token': 'MitakeWeb',
    'Param': '1,13|1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71'
}
field_names = load_yaml_data(yaml_file)
if not field_names:
    print("未找到字段，无法继续操作")
    exit()
start_time = time.time()
url1 = 'http://114.28.169.97:22016/v3/quote'
url2 = 'http://114.141.177.5:22016/v3/quote'


# 修改 parse_response 以捕获字段解析错误
def parse_response(response_text, symbols, field_names):
    """解析接口返回数据，并按 symbol 分类"""
    parsed_data = {symbol: {field: None for field in field_names} for symbol in symbols}
    try:
        resp_list = response_text.split("\x03")
        if resp_list[-1] == '':
            resp_list.pop()
        for entry in resp_list:
            split_list = entry.split("\x02")
            if len(split_list) > 1 and split_list[0] in symbols:  # 确保 symbol 存在
                symbol = split_list[0]
                values = split_list[1:]
                # 检查字段和值的数量是否匹配
                if len(values) != len(field_names):
                    logger.error(f"Symbol {symbol} 字段数量和 YAML 定义的字段不匹配")
                for field_name, value in zip(field_names, values):
                    parsed_data[symbol][field_name] = value.split("\x01") if "\x01" in value else [value]
    except Exception as e:
        logger.error(f"解析接口响应数据时发生错误：{e}")
    return parsed_data


for i in range(0, len(stock_symbols), symbols_per_request):
    batch_symbols = stock_symbols[i:i + symbols_per_request]  # 获取当前批次的 symbol 列表
    symbols_str = ','.join(batch_symbols)  # 将股票符号连接成一个字符串
    logger.info(f"正在处理股票：{symbols_str}")
    headers['symbol'] = symbols_str
    try:
        response1 = requests.get(url1, headers=headers)
        data1 = parse_response(response1.text, batch_symbols, field_names)
    except requests.exceptions.RequestException as e:
        logger.error(f"请求接口1时发生错误：{e}")
        data1 = None
    try:
        response2 = requests.get(url2, headers=headers)
        data2 = parse_response(response2.text, batch_symbols, field_names)
    except requests.exceptions.RequestException as e:
        logger.error(f"请求接口2时发生错误：{e}")
        data2 = None
    if data1 and data2:
        for symbol in batch_symbols:
            discrepancies = {}
            for field_name in field_names:
                value1 = data1.get(symbol, {}).get(field_name)
                value2 = data2.get(symbol, {}).get(field_name)
                if value1 != value2:
                    discrepancies[field_name] = {
                        'url1_value': value1,
                        'url2_value': value2
                    }
                # 记录字段缺失
                if value1 is None:
                    logger.warning(f"股票 {symbol} 字段 {field_name} 在接口1的响应中缺失")
                if value2 is None:
                    logger.warning(f"股票 {symbol} 字段 {field_name} 在接口2的响应中缺失")
            if discrepancies:
                logger.error(f"股票 {symbol} 接口返回数据不一致的字段：")
                for field_name, values in discrepancies.items():
                    logger.error(f"{field_name}: {values['url1_value']} , {values['url2_value']}")
                logger.info("==========================================================")
            else:
                logger.info(f"股票 {symbol} 两个接口的返回数据一致")
    else:
        logger.error(f"{symbols_str} 一或两个接口的响应数据无效，无法比较")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\n代码运行结束，总共耗时：{elapsed_time:.2f} 秒")