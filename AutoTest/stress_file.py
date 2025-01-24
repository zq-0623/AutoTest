#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：AutoTest 
@File    ：stress_file.py
@IDE     ：PyCharm 
@Author  ：Qiang zhao
@Date    ：2024/10/8 19:28 
"""
import threading
import time
from collections import defaultdict

import requests

# 请求地址
base_url = 'http://114.28.169.97:22016'

# 定义headers
base_headers = {
    'token': 'MitakeWeb',
    'hid': 'test1111'
}

# 读取文件
with open('gzc6_random.txt', 'r') as file:
    lines = file.readlines()


# 请求函数
def send_request(interface, symbol, params, metrics, lock):
    headers = base_headers.copy()
    headers['symbol'] = symbol
    headers['param'] = params
    url = f"{base_url}{interface}"

    start_time = time.time()
    try:
        response = requests.get(url, headers=headers)
        elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒

        with lock:
            metrics[interface]['total_requests'] += 1
            metrics[interface]['total_time'] += elapsed_time
            metrics[interface]['successful_requests'] += 1
    except Exception as e:
        elapsed_time = (time.time() - start_time) * 1000

        with lock:
            metrics[interface]['total_requests'] += 1
            metrics[interface]['total_time'] += elapsed_time
            metrics[interface]['failed_requests'] += 1


# 创建线程
threads = []
start_time = time.time()
duration = 60  # 持续时间（秒）
metrics = defaultdict(lambda: {
    'total_requests': 0,
    'total_time': 0,
    'successful_requests': 0,
    'failed_requests': 0
})
lock = threading.Lock()

for line in lines:
    parts = line.strip().split(';')
    if len(parts) >= 3:
        interface = parts[0]
        symbol = parts[1]
        params = parts[2]

        # 创建线程
        thread = threading.Thread(target=send_request, args=(interface, symbol, params, metrics, lock))
        threads.append(thread)
        thread.start()

        # 限制线程数为30
        if len(threads) >= 30:
            for t in threads:
                t.join()  # 等待所有线程完成
            threads.clear()  # 清空线程列表

        # 检查持续时间
        if time.time() - start_time >= duration:
            break

# 等待剩余线程完成
for t in threads:
    t.join()

# 打印结果
print("聚合报告:")
print("{:<30} {:<15} {:<15} {:<15} {:<15} {:<15}".format("接口", "请求数量", "平均响应时间(ms)", "成功请求", "失败请求",
                                                         "异常率"))
for interface, data in metrics.items():
    if data['total_requests'] > 0:
        avg_response_time = data['total_time'] / data['total_requests']
        failure_rate = (data['failed_requests'] / data['total_requests']) * 100
    else:
        avg_response_time = 0
        failure_rate = 0
    print("{:<30} {:<15} {:<15} {:<15} {:<15} {:.2f}%".format(
        interface,
        data['total_requests'],
        avg_response_time,
        data['successful_requests'],
        data['failed_requests'],
        failure_rate
    ))

# 计算吞吐量
end_time = time.time()
total_requests = sum(data['total_requests'] for data in metrics.values())
throughput = total_requests / (end_time - start_time)  # 每秒请求数
print(f"\n吞吐量: {throughput:.2f} requests/second")


