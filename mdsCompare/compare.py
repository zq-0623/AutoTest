import decimal
import json

from deepdiff import DeepDiff
import requests

from util.excel_dict import key_sort_group
from mdsCompare.build_report import csv_result


# 请求接口
def compare_run(item):
    # print("用例",item)

    response = request_run(item)
    code = item['code']
    # print('代码',code)
    field = item['field']
    print("==============")
    if "响应失败" in response:
        return False
    if "响应报错" in response:
        return False
    if response:

        # print(csv_result)
        # 取出返回列表的各值的字段名
        field_list = item['field_list']
        # print取出清洗文件中要比对的股票
        # (csv_result)
        list1 = csv_result[str(code)]
        # 处理请求结果
        list2 = deal_result(response, field, field_list, code)[str(code)]
        # print(list1)
        # print(list2)
        """ cutoff_distance_for_pairs 用于结果中展示差异的深度。值越高，则结果中展示的差异深度越高
            ignore_type_in_groups=DeepDiff.numbers 避免数据类型不一致导致的比对结果不一致 
            ignore_order=True 避免列表中顺序不一致导致的比对结果不一致"""
        compare_result = DeepDiff(list1, list2, ignore_order=True, cutoff_distance_for_pairs=0.6,
                                  ignore_type_in_groups=DeepDiff.numbers)
        if len(compare_result) == 0:
            print("数据比对一致\n")
            return True
        else:
            print("比对结果：\n", compare_result.pretty())
            return False
    else:
        print("接口响应数据为空" + "\n")
        return False


# 发送接口请求
def request_run(item):
    param = None
    header = None
    body = None
    resp = None
    url = None
    code = None
    request_result = []
    request = item["request"]
    if "code" in item:
        code = item["code"]
    if "url" in item:
        url = item["url"] + str(code)
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
            # resp.text保留返回数据原格式
            # resp = resp.text()
            # print(resp.text)
            resp_data = json.loads(resp.text, parse_float=decimal.Decimal)
            # 拼接接口响应结果
            # print(resp_data)
            request_result.append(resp_data)
            # print("接口请求成功")
            print("接口响应码:", str(resp.status_code) + "\n")
            # print("response:", str(resp_data) + "\n")
            # return "true"
        else:
            # print("接口请求失败")
            # print("接口响应码:", str(resp.status_code) + "\n")
            request_result.append("响应失败")
    except Exception as e:
        # print("接口请求失败")
        print("失败信息:", str(e) + "\n")
        request_result.append("响应报错")
    return request_result


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


# 处理请求返回的数据
def deal_result(data, field, field_list, code):

    resp = data[0][field]
    index = len(field_list)
    resp_list = []
    for i in resp:
        resp_json = {}
        for m in range(index):
            key = field_list[m]
            if key == 'date':
                value = str(i[m])
                resp_json[key] = value
            else:
                value = float(i[m])
                resp_json[key] = value
            resp_json['code'] = str(code)
        resp_list.append(resp_json)
    # print(resp_list)
    resp_list = key_sort_group(resp_list)
    # print(resp_list)
    return resp_list
