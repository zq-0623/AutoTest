"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest 
@File    ：AP_auth_tool.py
@IDE     ：PyCharm 
@Author  ：ZhaoQiang
@Date    ：2024/11/22 星期五 13:42 
"""
import base64
import json

import openpyxl
import requests
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad


def read_data_from_excel(file_path):
    """
    从 Excel 文件中读取 bid, name, appkey 数据
    :param file_path: Excel 文件路径
    :return: [{'bid': bid, 'name': name, 'appkey': appkey}, ...]
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    records = []

    # 遍历 Excel 的内容，跳过第一行
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # 假设 bid、name 和 appkey 分别位于第一、第二、第三列
        bid, name, appkey = row[0], row[1], row[2]
        if bid and name and appkey:  # 确保非空
            records.append({"bid": str(bid), "name": str(name), "appkey": str(appkey)})
    return records


def encrypt_3des(data, key):
    """
    使用 3DES 加密
    :param data: 需要加密的完整字符串（包括 {}）
    :param key: 24字节长的密钥
    :return: 加密后的base64字符串
    """
    cipher = DES3.new(key.encode('utf-8'), DES3.MODE_ECB)
    padded_data = pad(data.encode('utf-8'), DES3.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode('utf-8')


def make_requests_with_encrypted_body():
    # 从 Excel 文件中读取数据
    file_path = "../../TestFile/token_appkey/HarmonyOS_AppKey.xlsx"  # 替换为实际文件路径
    records = read_data_from_excel(file_path)

    # 加密密钥，24字节
    encryption_key = "b68384a66092849f10f72d0e"  # 替换为实际密钥

    # HTTP 请求设置
    url = "http://114.28.169.97:22016/v2/auth"
    headers = {"Content-Type": "application/json"}

    # 遍历读取的记录，准备请求
    for idx, record in enumerate(records, start=1):
        # 准备完整的 JSON 数据
        # Android
        # raw_data = {"bid": record["bid"],"platform": "AndroidPhone","brand": "google","device": "Android SDK built for x86","os": "10","hid": "test123456","name": record["name"],"ver": "99","token": "","appkey": record["appkey"],"sdk_ver": "4.5.1","timestamp": "1732767123857"}
        # iOS
        # raw_data = {"Accept-Encoding": "gzip","bid": record["bid"],"timestamp": "1732767123857","brand": "Apple","os": "16.7.2","platform": "iPhone","ver": "1.3.50","appkey": record["appkey"],"hid": "1234567890","device": "iPhone11","name": record["name"],"sdk_ver": "4.2.11"}
        # HarmonyOS
        raw_data = {"bid": record["bid"],"platform": "HarmonyOSPhone","brand": "HUAWEI","device": "emulator","os": "2.1.6.6(Beta2)","hid": "1234567890","name": record["name"],"ver": "1000000","appkey": record["appkey"],"sdk_ver": "0.0.12","timestamp": "1732767123857"}

        # 将完整的 JSON 数据转为字符串并加密
        raw_data_str = json.dumps(raw_data, separators=(',', ':'))  # 转为紧凑的字符串
        encrypted_data = encrypt_3des(raw_data_str, encryption_key)

        # 发送请求
        response = requests.post(url, data=encrypted_data, headers=headers)

        # 输出结果
        print(f"\033[32m请求 {idx} - bid: {record['bid']}, name: {record['name']}, appkey: {record['appkey']}\033[0m")
        if response.status_code == 200:
            print(f"\033[32m请求成功\033[0m")
        else:
            res_header_msg = response.headers.get('msg', '无返回消息')
            print(f"\033[31m请求失败原因：{res_header_msg}\033[0m")
            print(f"\033[31m请求失败，状态码：{response.status_code}\033[0m")


if __name__ == "__main__":
    make_requests_with_encrypted_body()

