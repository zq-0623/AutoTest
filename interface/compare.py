import decimal
import json
import os
import sys
from threading import Thread

import allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
from deepdiff import DeepDiff

# 发送请求，获取响应

result = []


# url = None


# 多线程请求接口
def thread_run(item):
    thread_array = []
    for i in range(2):
        key = "url" + str(i + 1)
        url = item[key]
        t = Thread(target=request_run, args=(item, url))
        thread_array.append(t)
        t.start()
    for t in thread_array:
        t.join()
    # print(result)
    # print("==============")
    if "响应失败" in result:
        return False
    if "响应报错" in result:
        return False
    elif result[0] == result[1]:
        return True
    else:
        json1 = result[0]
        json2 = result[1]
        # print(json2)
        """ ignore_order=True 避免列表中顺序不一致导致的比对结果不一致"""
        # if item['group_key']:
        #     compare_result = DeepDiff(json1, json2, group_by=item['group_key'])
        # else:
        compare_result = DeepDiff(json1, json2)
        if len(compare_result) == 0:
            allure.attach("数据比对一致", name="比对结果")
            return True
        else:
            # print("比对结果：\n" + compare_result.pretty())  # 使用pretty()方法获得更可读的输出
            allure.attach(compare_result.pretty(), name="比对结果")
            return False


# 发送接口请求
def request_run(item, url):
    # print(item)
    param = None
    header = None
    body = None
    resp = None
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
            resp_data = json.loads(resp.text, parse_float=decimal.Decimal)
            # 拼接接口响应结果
            result.append(resp_data)
            # print("接口请求成功")
            # print("接口响应码:" + str(resp.status_code) + "\n")
            # allure.step("接口请求成功")
            # allure.attach("接口响应码:" + str(resp.status_code) + "\n", name="接口请求成功")

            # print("response:", str(resp_data) + "\n")
            # return "true"
        else:
            print("接口请求失败\n")
            print("接口响应码:", str(resp.status_code) + "\n")
            result.append("响应失败")
            # allure.step("接口请求失败：" + str(resp.status_code))
    except Exception as e:
        print("接口请求异常\n")
        print("失败信息:" + str(e) + "\n")
        result.append("响应报错")
        # allure.step("接口请求异常：" + str(e))
        # return "false"


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
