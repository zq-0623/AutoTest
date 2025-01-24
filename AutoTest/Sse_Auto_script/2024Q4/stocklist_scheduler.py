"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest 
@File    ：stocklist_scheduler.py
@IDE     ：PyCharm 
@Author  ：ZhaoQiang
@Date    ：2024/12/9 星期一 16:10 
"""
import os
import time
from datetime import datetime

import requests
import schedule

url = "http://114.28.169.97:22016/v2/stocklist"
headers = {
    "token": "MitakeWeb",
    "symbol": "0"
}

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)


def read_params(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            params = [line.strip() for line in file.readlines()]
        return params
    except Exception as e:
        print(f"读取param文件失败: {e}")
        return []


def fetch_and_save(param):
    try:
        headers["param"] = param
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查响应状态码
        current_time = datetime.now().strftime("%H:%M")
        filename = f"{current_time.replace(':', '')}_{param}.txt"
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"[{current_time}] 数据成功保存到 {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")


# schedule_times = ["08:32", "08:44", "08:55", "09:06", "09:17", "09:28", "09:30"]
schedule_times = ["16:57", "16:59"]

param_file = "params.txt"
params = read_params(param_file)

if not params:
    print("没有读取到有效的param参数，脚本退出")
    exit(1)


def validate_schedule_times(times):
    valid_times = []
    for time_str in times:
        try:
            datetime.strptime(time_str, "%H:%M")
            valid_times.append(time_str)
        except ValueError:
            print(f"无效的时间格式: {time_str}，跳过该时间点")
    return valid_times


schedule_times = validate_schedule_times(schedule_times)

for schedule_time in schedule_times:
    for param in params:
        schedule.every().day.at(schedule_time).do(fetch_and_save, param=param)

print("任务已调度，等待运行...")

while True:
    schedule.run_pending()
    time.sleep(1)
