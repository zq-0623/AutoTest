# 导入需要使用的模块
import json
import os
import sys

import allure
import requests

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


def smoke_run(item):
    # print(item)
    # 发送请求，获取响应
    param = None
    header = None
    body = None
    resp = None
    url = item["url"]
    request = item["request"]
    if "queryParam" in request:
        param = request["queryParam"]
    if "header" in request:
        header = request["header"]
    if "body" in request:
        body = request["body"]

    # 处理响应
    try:
        if item["method"] == "get":
            resp = requests.get(url=url, headers=header, params=param)
        elif item["method"] == "post":
            resp = requests.post(url=url, headers=header, params=param, data=json.dumps(body))
        if resp.status_code == 200:
            resp_data = resp.json()  # 返回的是 json 格式的数据
            # print("接口请求成功")
            # print("接口响应码:" + str(resp.status_code) + "\n")
            # print("response:" + str(resp_data) + "\n")
            allure.attach("接口响应码:" + str(resp.status_code) + "\n"+"response:" + str(resp_data) + "\n", name="接口请求成功")
            return True
        else:
            # print("接口请求失败")
            # print("接口响应码:" + str(resp.status_code) + "\n")
            allure.attach("接口响应码:" + str(resp.status_code) + "\n", name="接口请求失败")
            return False
    except Exception as e:
        # print("接口请求失败")
        # print("报错信息:" + str(e) + "\n")
        allure.attach("报错信息:" + str(e) + "\n", name="接口请求异常")
        return False
