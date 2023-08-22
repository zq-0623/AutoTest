# -*- coding: utf-8 -*-
import os.path

import pandas as pd
from util.logTool import logger
current_path = os.path.abspath(__file__)
log_flag = os.path.split(current_path)[1].split(".py")[0]


def compare_excel_columns(file1_path, file2_path, file1_column, file2_column):
    # 读取文件内容
    file1_data = pd.read_excel(file1_path)
    file2_data = pd.read_excel(file2_path)

    # 调整行数，使两个文件行数一致
    max_rows = min(len(file1_data), len(file2_data))
    file1_data = file1_data.head(max_rows)
    file2_data = file2_data.head(max_rows)

    # 获取指定列的值并进行比较
    file1_column_values = file1_data[file1_column]
    file2_column_values = file2_data[file2_column]

    # 重置索引以确保比较
    file1_column_values = file1_column_values.reset_index(drop=True)
    file2_column_values = file2_column_values.reset_index(drop=True)

    # 找出不同的结果，包含行号
    different_results = pd.DataFrame({
        '行号': file1_column_values.index + 1,  # 为了从1开始计数
        file1_column: file1_column_values,
        file2_column: file2_column_values
    })
    different_results = different_results[different_results[file1_column] != different_results[file2_column]]

    return different_results

# mqtt
# r均价(a)	r最新价(c)	r第一笔资料时间(ot)	r最高价(h)	r索引(i)	r最低价(l)
# r成交额(m)	r开盘价(o)	r资料确认时间(dt)	r参考价(r)	r时间(t)	r成交量(v)	r参考价(ir)	r最新价(ic)

# http
# 日期时间	开	高	低	收	量	参考价	成交额	盘后成交量	盘后成交额	前一根收盘价	基金净值	均价

'''
000001
000656
131810
159792
200625
204001
300059
513060
600050
688223
837592
900901
10005650
90002344
H30455
'''


mqtt_file_path = r'C:/Users/Administrator/Desktop/mqtt_kline_data/min120_mqtt_line_000001.xlsx'
http_file_path = r'C:/Users/Administrator/Desktop/http_kline_data/min120_http_line_000001.xlsx'


# 文件和列名列表
file_pairs = [
    (mqtt_file_path, http_file_path, 'r均价(a)', '均价'),
    (mqtt_file_path, http_file_path, 'r最高价(h)', '高'),
    (mqtt_file_path, http_file_path, 'r最低价(l)', '低'),
    (mqtt_file_path, http_file_path, 'r成交额(m)', '成交额'),
    (mqtt_file_path, http_file_path, 'r开盘价(o)', '开'),
    (mqtt_file_path, http_file_path, 'r参考价(r)', '参考价'),
    (mqtt_file_path, http_file_path, 'r时间(t)', '日期时间'),
    (mqtt_file_path, http_file_path, 'r成交量(v)', '量'),
    (mqtt_file_path, http_file_path, 'r最新价(ic)', '基金净值'),
    # 添加更多文件和列名组合
]



# file_pairs = [
#     (mqtt_file_path, http_file_path, '时间', '日期时间'),
#     (mqtt_file_path, http_file_path, '最新价', '收'),
#     (mqtt_file_path, http_file_path, '成交量', '量'),
#     (mqtt_file_path, http_file_path, '参考价', '参考价2'),
#     (mqtt_file_path, http_file_path, '均价', '均价2'),
#     (mqtt_file_path, http_file_path, '成交额', '成交额2'),
#     (mqtt_file_path, http_file_path, '开盘价', '开'),
#     (mqtt_file_path, http_file_path, '最高价', '高'),
#     (mqtt_file_path, http_file_path, '最低价', '低'),
#     # 添加更多文件和列名组合
# ]
# 循环比较并打印结果
logger.info("文件名===================》"+ os.path.basename(mqtt_file_path))
for file1_path, file2_path, file1_column, file2_column in file_pairs:
    result = compare_excel_columns(file1_path, file2_path, file1_column, file2_column)
    logger.info(f"比较 {file1_path} 中的 '{file1_column}' 和 {file2_path} 中的 '{file2_column}':")
    logger.info(result)
logger.info("=" * 60)
