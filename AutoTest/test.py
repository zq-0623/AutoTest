# -*-coding:utf-8 -*-
import os
import time
import pandas as pd


time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
curPath = os.path.abspath(os.path.dirname(__file__))
file_path = r'E:\workspace\PythonProject\AutoTest\SseSDK\result\110013K线数据.xlsx'
# 读取Excel文件
df = pd.read_excel(file_path)

# 合并两列文字
df['交易时间111'] = df['日期'].astype(str) + df['时间'].apply(lambda x: str(x).zfill(6))
df['交易时间111'] = df['交易时间111'].str[:-2]

# 保存合并后的结果
df.to_excel('K线数据1.xlsx',index=False)

