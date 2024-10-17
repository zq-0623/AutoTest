# from decimal import Decimal, ROUND_HALF_UP
#
# value = Decimal(-0.061650)
# B = (Decimal(value) * Decimal(100)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
# print(B)
#
# C = round(value, 2)
# print(C)

# from util.base93 import decode
#
# with open("./TestFile/test.txt", "r", encoding='utf-8') as file:
#     files = file.readlines()
#     for i in files:
#         if i:
#             data_str = i.split('\x03')
#             for j in data_str:
#                 te_str = j.split('\x02')
#                 # print(te_str)
#                 if j:
#                     new_list = te_str[:]
#                     new_list[2] = decode(te_str[2])
#                     new_list[3] = decode(te_str[3])
#                 # print(new_list[2])  # 总股本
#                 print(new_list[3])  # 流通股本

#
# import redis
# import requests
#
# # 设置接口地址和 Redis 连接
# url = "http://114.28.169.157:22017/v1/ahquote"
# redis_host = 'localhost'
# redis_port = 6379
# r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
#
# def fetch_and_process_data():
#     try:
#         # 请求接口数据
#         response = requests.get(url)
#         response.raise_for_status()  # 检查请求是否成功
#         data = response.content.decode('utf-8')  # 将返回数据解码为字符串
#
#         # 以"\x03"分割数据
#         split_data = data.split("\x03")
#         field_values = []
#
#         # 遍历分割后的数据，再以"\x02"分割并提取第二个字段
#         for item in split_data:
#             parts = item.split("\x02")
#             if len(parts) > 1:
#                 field_values.append(parts[1])
#
#         # 遍历字段列表，将每个值按"."分割，并用分割后的第二个部分进行Redis查询
#         for value in field_values:
#             dot_split = value.split(".")
#             if len(dot_split) > 1:
#                 first_part = dot_split[0]
#                 second_part = dot_split[1]
#                 # 从 Redis 获取与 second_part 相关的值
#                 redis_value = r.get(second_part)
#                 if redis_value:
#                     # 拼接成新的 redis_key.redis_value.first_part 形式
#                     redis_key = f"{second_part}.{redis_value}.{first_part}"
#                     A_rate = r.get("hk.cr.CNY")
#                     H_rate = r.get("hk.cr.HKD")
#                     print(A_rate,H_rate)
#                     print(f"Constructed Redis Key: {redis_key}")
#                 else:
#                     print(f"Redis key '{second_part}' not found in Redis.")
#             else:
#                 print(f"Invalid value (no '.'): {value}")
#
#     except requests.RequestException as e:
#         print(f"Error fetching data: {e}")
#     except redis.RedisError as e:
#         print(f"Redis error: {e}")
#
# # 调用函数
# fetch_and_process_data()

#
# import matplotlib.pyplot as plt
# import pandas as pd
#
# # 设置字体，确保中文显示
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
#
# # 加载 CSV 文件到 DataFrame 中 (修改为你的文件路径)
# df = pd.read_csv('./TestFile/process_monitor_2_50.csv')
#
# # 去除列名中的空格
# df.columns = df.columns.str.strip()
#
# # 确保 'Timestamp' 列被正确解析为时间格式
# df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%H:%M:%S')
#
# # 清理 RES 列，去除空格和单位，并转换为浮点数
# df['RES'] = df['RES'].str.strip().str.replace('g', '').astype(float)
#
# # 绘制 %CPU 趋势图
# plt.figure(figsize=(20, 6))
# plt.plot(df['Timestamp'], df['%CPU'], label='CPU使用率', marker='o')
# plt.xlabel('时间')
# plt.ylabel('数值')
# plt.title('50只股票3秒间隔的CPU使用率趋势')
# plt.xticks(ticks=df['Timestamp'][::10], labels=df['Timestamp'].dt.strftime('%H:%M:%S')[::10], rotation=45)
# plt.yticks(ticks=range(0, int(df['%CPU'].max()) + 50, 50))
# plt.legend()
# plt.tight_layout()
# plt.show()


import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# 读取 Excel 文件
file_path = './TestFile/compare.xlsx'  # 替换为实际文件路径
df = pd.read_excel(file_path)

# 将 '时间' 列转换为 datetime 对象
df['时间'] = pd.to_datetime(df['时间'], format='%Y%m%d-%H:%M:%S')

# 设置时间列为索引
df.set_index('时间', inplace=True)

# 按10秒间隔重采样数据，使用前向填充法补充数据
df_resampled = df.resample('60S').ffill()

# 设置字体为支持中文的字体，如黑体 SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号

# 创建图形
plt.figure(figsize=(30, 10))

# 绘制折线图
plt.plot(df_resampled.index, df_resampled['生产'], label='生产', marker='o')
plt.plot(df_resampled.index, df_resampled['T6'], label='T6', marker='o')

# 设置横轴显示时间格式
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

# 动态设置 x 轴的显示范围，选择每隔5个数据点显示一个时间刻度
plt.xticks(df_resampled.index[::3], rotation=45)

# 添加标题和标签
plt.title('生产和T6随时间变化图')
plt.xlabel('时间')
plt.ylabel('值')

# 显示图例
plt.legend()

# 显示网格
plt.grid(True)

# 显示图形
plt.show()
