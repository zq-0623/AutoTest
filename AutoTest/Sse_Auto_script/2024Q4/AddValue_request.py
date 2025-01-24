"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest 
@File    ：AddValue_request.py
@IDE     ：PyCharm 
@Author  ：ZhaoQiang
@Date    ：2024/12/5 星期四 15:02 
"""
import time
from datetime import datetime

import requests

from util.logTool import logger

# 请求的两个URL
url_trade = "http://114.141.177.7:9267/v1/cna/list/exchange/trade"
url_all = "http://114.141.177.7:9267/v1/cna/list/exchange/all"


def make_request(url, prefix):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            current_time = datetime.now().strftime('%m%d%H%M')
            with open(f"./script_result/{prefix}_{current_time}.txt", 'w') as file:
                file.write(response.text)
            print(f"{prefix} 请求成功，结果已保存到 {prefix}_{current_time}.txt")
        else:
            print(f"{prefix} 请求失败，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"{prefix} 请求异常: {e}")


def schedule_requests():
    while True:
        current_time = datetime.now()
        if ((current_time.hour == 8 and current_time.minute >= 30) or
            (current_time.hour == 9 and current_time.minute < 59)):
            make_request(url_trade, 'trade')
            make_request(url_all, 'all')
            time.sleep(120)
        else:
            logger.info("当前不在请求时间内，等待中...")
            time.sleep(60)


if __name__ == "__main__":
    schedule_requests()
