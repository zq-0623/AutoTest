# -*- coding: utf-8 -*-
# @Time : 2024/10/21 星期一 15:10
# @Author : Zhao Qiang
# @File ：OHLC_quote_compare_shl2.py
# @IDE ：PyCharm
import re

# 定义日志文件路径
DFLOG = './TestFile/OHLC_LOG/df-sh.log'
OHLC_FILE = './TestFile/OHLC_LOG/df_ohlc.log'
QUOTE_FILE = './TestFile/OHLC_LOG/df_lastpx.log'


def extract_ohlc(log_file_path, ohlc_output_path):
    """从日志中提取OHLC数据并保存到输出文件中。"""
    SID = '601162'
    OHLC_PARSER = 'OHLC--'

    try:
        with open(DFLOG, 'r', encoding='utf-8') as infile, \
                open(OHLC_FILE, 'w', encoding='utf-8') as ohlc_outfile:

            for line in infile:
                if re.search(SID, line) and re.search(OHLC_PARSER, line):
                    ohlc_outfile.write(line)

        print("OHLC 数据处理完成，结果已保存到", OHLC_FILE)
    except FileNotFoundError:
        print(f"错误: 文件 {DFLOG} 不存在。")
    except Exception as e:
        print(f"发生错误: {e}")


def extract_lastpx(log_file_path, quote_output_path):
    """从日志中提取LastPx数据并保存到输出文件中。"""
    SID = '601162'
    QUOTE_PARSER = 'LastPx'

    try:
        with open(DFLOG, 'r', encoding='utf-8') as infile, \
                open(QUOTE_FILE, 'w', encoding='utf-8') as quote_outfile:

            for line in infile:
                if re.search(SID, line) and re.search(QUOTE_PARSER, line):
                    quote_outfile.write(line)

        print("LastPx 数据处理完成，结果已保存到", quote_output_path)
    except FileNotFoundError:
        print(f"错误: 文件 {log_file_path} 不存在。")
    except Exception as e:
        print(f"发生错误: {e}")


# def extract_ohlc_values(ohlc_log_file_path):
#     ohlc_list = []
#     """从OHLC数据中提取开高低收的值并打印。"""
#     try:
#         with open(OHLC_FILE, 'r', encoding='utf-8') as infile:
#             for line in infile:
#                 match_data = re.search(r'\{.*?\}', line)
#                 if match_data:
#                     json_data = match_data.group(0)
#                     data_dict = json.loads(json_data)
#                     ohlc_list.append(data_dict)
#             # 使用字典存储每个时间的最后一根 K 线数据
#             latest_data = {}
#             for entry in ohlc_list:
#                 time = entry['t']
#                 latest_data[time] = entry  # 更新字典，保持最后一根数据
#             # 打印输出每个时间的 K 线数据
#             for time, entry in latest_data.items():
#                 print(
#                     f"{time}的K线数据：o(开盘价):{entry['o']}，h(最高价):{entry['h']}，l(最低价):{entry['l']}，c(收盘价):{entry['c']}，a(均价):{entry['a']}，v(成交量):{entry['v']}")
#     except FileNotFoundError:
#         print(f"错误: 文件 {ohlc_log_file_path} 不存在。")
#     except Exception as e:
#         print(f"发生错误: {e}")


# def extract_lastpx(file_name):
#     data_list = []
#     with open(file_name, 'r', encoding='utf-8') as file:
#         for line in file:
#             # 提取时间
#             time_pattern = r'(\d{14})'
#             time_match = re.search(time_pattern, line)
#             time_values = time_match.group(1) if time_match else None
#
#             # 提取LastPx
#             last_px_pattern = r'LastPx=(\d+)'
#             last_px_match = re.search(last_px_pattern, line)
#             last_px_value = last_px_match.group(1) if last_px_match else None
#
#             # 提取 avgPrice
#             avg_price_pattern = r'avgPrice:(\d+)'
#             avg_price_match = re.search(avg_price_pattern, line)
#             avg_price_value = avg_price_match.group(1) if avg_price_match else None
#
#             # 提取totalVolumeTrade
#             total_volume_pattern = r'totalVolumeTrade:(\d+)'
#             total_volume_match = re.search(total_volume_pattern, line)
#             total_volume_value = total_volume_match.group(1) if total_volume_match else None
#             # 创建字典并保存到列表中
#             if total_volume_value and int(total_volume_value) > 0:
#                 snapshot_data = {
#                     "time": time_values,
#                     "LastPx": last_px_value,
#                     "avgPrice": avg_price_value,
#                     "totalVolumeTrade": total_volume_value
#                 }
#                 data_list.append(snapshot_data)
#         for data in data_list:
#             print("快照数据：", data)


if __name__ == '__main__':
    # 执行数据提取
    extract_ohlc(DFLOG, OHLC_FILE)
    extract_lastpx(DFLOG, QUOTE_FILE)

    # 从OHLC数据中提取值并打印
    # extract_ohlc_values(OHLC_FILE)
    # extract_lastpx(QUOTE_FILE)
