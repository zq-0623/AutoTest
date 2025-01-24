"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest 
@File    ：CheckIP_make.py
@IDE     ：PyCharm 
@Author  ：ZhaoQiang
@Date    ：2024/11/20 星期三 15:14 
"""
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods =["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# 定义请求方法
def send_request_and_process(ip, ip_type, url, headers_template, output_file, session):
    headers = headers_template.copy()
    headers[ip_type] = ip

    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if "isc" in response_data and response_data["isc"] == "y":
                with open(output_file, "a") as file:
                    file.write(f"{ip} | isc: y\n")
                print(f"\033[32m成功处理: {ip}")
            else:
                print(f"\033[31m不匹配 isc: y: {ip}")
        else:
            print(f"\033[31m请求失败: {ip}，状态码: {response.status_code}")
    except Exception as e:
        print(f"\033[31m请求或处理失败: {ip}，错误: {e}")


def process_requests(file_path, url, headers_template, output_file, max_workers=30):
    try:
        with open(file_path, "r") as file:
            next(file)
            ipv4_list = []
            ipv6_list = []
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 2:
                    ipv4, ipv6 = parts[0].strip(), parts[1].strip()
                    ipv4_list.append(ipv4)
                    ipv6_list.append(ipv6)
                else:
                    print(f"\033[31m行格式错误，跳过: {line.strip()}")

        with open(output_file, "w") as file:
            file.write("IP | Result\n")
        session = create_session()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            ipv4_futures = [
                executor.submit(send_request_and_process, ip, "IPv4", url, headers_template, output_file, session)
                for ip in ipv4_list
            ]
            ipv6_futures = [
                executor.submit(send_request_and_process, ip, "IPv6", url, headers_template, output_file, session)
                for ip in ipv6_list
            ]
            for future in ipv4_futures + ipv6_futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"\033[31m任务执行失败: {e}")

    except FileNotFoundError:
        print(f"\033[31m文件未找到: {file_path}")
    except Exception as e:
        print(f"\033[31m发生错误: {e}")


# 配置参数
# url = "http://114.28.169.97:22016/v1/service/ipinfo"
url = "http://114.141.177.5:22016/v1/service/ipinfo"
headers_template = {
    "token": "MitakeWeb",
    "symbol": "observe",
    "hid": "test123456"
}
file_path = "../../TestFile/ip_addresses.txt"
output_file = "../../TestFile/filtered_ips1.txt"
start_time = time.time()
process_requests(file_path, url, headers_template, output_file, max_workers=20)
end_time = time.time()
print(f"总耗时: {end_time - start_time:.2f} 秒")
