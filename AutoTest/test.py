# # -*-coding:utf-8 -*-
# import os
# import time
# import pandas as pd
#
#
# time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
# curPath = os.path.abspath(os.path.dirname(__file__))
# file_path = r'E:\workspace\PythonProject\AutoTest\SseSDK\result\110013K线数据.xlsx'
# # 读取Excel文件
# df = pd.read_excel(file_path)
#
# # 合并两列文字
# df['交易时间111'] = df['日期'].astype(str) + df['时间'].apply(lambda x: str(x).zfill(6))
# df['交易时间111'] = df['交易时间111'].str[:-2]
#
# # 保存合并后的结果
# df.to_excel('K线数据1.xlsx',index=False)
#
import re

response_list = {
    'values_changed': {
        "root[0]['430017.bz'][43][4]": {'new_value': 10340, 'old_value': 10360},
        "root[0]['430139.bz'][34][4]": {'new_value': 10140, 'old_value': 10260},
        "root[1]['430017.bz'][43][4]": {'new_value': 10340, 'old_value': 10360},
        "root[1]['430139.bz'][34][4]": {'new_value': 10140, 'old_value': 10260},
        "root[2]['430017.bz'][43][4]": {'new_value': 10340, 'old_value': 10360},
        "root[2]['430139.bz'][34][4]": {'new_value': 10140, 'old_value': 10260},
    }
}

# 使用正则表达式提取字符串中的类似"root[0]['430139.bz'][34][4]"的数据
pattern = r"\['(\d+\.\w+)'\]"
matches = re.findall(pattern, str(response_list))

# 以提取出的数据为分组
grouped_data = {}
for match in matches:
    if match not in grouped_data:
        grouped_data[match] = []

# 将不同的数据存储在各自的分组中
for key, change in response_list['values_changed'].items():
    match = re.search(pattern, key)
    if match:
        group_key = match.group(1)
        grouped_data[group_key].append(change)

# 显示每组中不同的数据
for key, data in grouped_data.items():
    print(f"分组: {key}")
    for i, change in enumerate(data):
        print(f"不同数据 {i + 1}:")
        print(f"new_value: {change['new_value']}")
        print(f"old_value: {change['old_value']}")
