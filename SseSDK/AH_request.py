#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：AutoTest
@File    ：AH_request.py
@IDE     ：PyCharm
@Author  ：Qiang zhao
@Date    ：2024/8/29 14:42
"""

import os
import sched
import time
from datetime import datetime

import requests

from util.base93 import decode

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

# 任务调度器
scheduler = sched.scheduler(time.time, time.sleep)


def start_task():
    url = "http://114.28.169.157:22017/v1/indexquote"
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.text
                resp = data.split('\x03')
                if resp[-1] == '':
                    resp.remove('')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = rootPath + f"/SseSDK/result/output_{timestamp}.txt"
                with open(filename, "w", encoding="utf-8") as file:
                    for i in resp:
                        if i:
                            data_str = i.split('\x02')
                            if data_str:
                                new_list = data_str[:]
                                new_list[2] = decode(data_str[2])
                                new_list[3] = decode(data_str[3])
                        file.write(str(new_list) + "\n")
                print(f"Data has been written to {filename} successfully.")
            else:
                print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        time.sleep(60)


# 目标开始执行的时间
target_time = datetime(2024, 8, 30, 8, 0, 0)
time_diff = (target_time - datetime.now()).total_seconds()

# 如果时间差大于0，计划任务
if time_diff > 0:
    print(f"Task scheduled to start at {target_time}")
    scheduler.enter(time_diff, 1, start_task)
    scheduler.run()
else:
    # 立即执行任务
    start_task()
