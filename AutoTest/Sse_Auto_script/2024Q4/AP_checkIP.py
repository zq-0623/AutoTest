"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest
@File    ：AP_checkIP.py
@IDE     ：PyCharm
@Author  ：ZhaoQiang
@Date    ：2024/11/19 星期二 11:10
"""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# 定义输入文件路径和输出文件路径
input_file = "../../TestFile/log-20241114.txt"  # 替换为您的输入文件路径
output_file = "../../TestFile/response_output1.txt"  # 定义输出文件路径

# 打开输入文件并读取内容
try:
    with open(input_file, "r") as file:
        lines = file.readlines()  # 按行读取文件内容
except FileNotFoundError:
    print(f"\033[31m文件 {input_file} 不存在，请检查路径！")
    exit()

# 按顺序提取第一个字段（IP 地址）并去重，取前500个
ip_set = set()  # 使用集合来去重
ip_list = []
for line in lines:
    stripped_line = line.strip()
    if stripped_line:  # 忽略空行
        ip = stripped_line.split()[0]  # 提取 IP 地址
        if ip not in ip_set:  # 如果 IP 不重复
            ip_set.add(ip)
            ip_list.append(ip)
        if len(ip_list) == 1000:  # 取前10000个IP
            break

if not ip_list:
    print(f"\033[31m文件 {input_file} 中没有可用的 IP 地址！")
    exit()

# 接口 URL 和固定请求头
url = "http://114.28.169.97:22016/v1/service/ipinfo"
# url = "http://114.141.177.5:22016/v1/service/ipinfo"
headers_template = {
    "token": "MitakeWeb",
    "symbol": "observe",
    "hid": "test123456"
}


def send_request(ip):
    """
    向接口发送请求并提取 "isc" 值。
    """
    headers = headers_template.copy()
    headers["param"] = ip  # 动态设置 param 为当前 IP
    try:
        response = requests.get(url, headers=headers, timeout=5)  # 设置超时时间为 1 秒
        # 提取 "isc" 的值
        if response.status_code == 200:
            try:
                content = response.json()  # 转换为字典
                isc_value = content.get("isc", "N/A")  # 提取 "isc" 的值
                return ip, response.status_code, isc_value
            except json.JSONDecodeError:
                return ip, response.status_code, "Invalid JSON"
        else:
            return ip, response.status_code, "Request failed"
    except Exception as e:
        return ip, "ERROR", str(e)


# 流式处理请求
def process_requests(ip_list, output_file, max_threads=50):
    """
    使用线程池按顺序处理 IP 请求。
    """
    results = []

    with ThreadPoolExecutor(max_threads) as executor:
        # 提交任务并获取结果
        futures = {executor.submit(send_request, ip): ip for ip in ip_list}

        # 实时处理返回结果
        with open(output_file, "a", encoding="utf-8") as output:
            for future in as_completed(futures):
                ip, status, isc_value = future.result()
                results.append((ip, status, isc_value))
                if status == 200 and isc_value != "N/A":
                    output.write(f"IP: {ip}, ISC: {isc_value}\n")
                print(f"\033[32mIP: {ip}, ISC: {isc_value}, 状态码: {status}")

    return results


# 主程序
if __name__ == "__main__":
    results = process_requests(ip_list, output_file)
    print(f"\033[32m所有请求已完成，结果已写入 {output_file}")
