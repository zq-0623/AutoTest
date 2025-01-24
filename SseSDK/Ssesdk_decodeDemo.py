# -*-coding:utf-8 -*-
import os

from Ssesdk_tool import SseOptionQuote, quote_yaml
from util.base93 import decode

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
yaml_path = rootPath + '/testCase/quote/line.yaml'
data = quote_yaml(yaml_path)


def decode_quote(msg):
    res_list = msg.split("\x03")
    list_result = []
    if res_list[-1] == '':
        res_list.remove('')
    for m in range(len(res_list)):
        split_list = res_list[m].split("\x02")
        for i in range(len(split_list)):
            data_key = list(data[i].keys())[0]
            data_values = list(data[i].values())[0]
            if data_values == 'Y':
                split_list[i] = decode(split_list[i])
        list_result.append(split_list)
    return list_result


def request_run():
    headers = {
        "token":"MitakeWeb",
        "symbol":"000002.sz",
        'param': '-1,20,0'
        # "param":"20050531"
    }
    response = SseOptionQuote(url, headers=headers)
    res = decode_quote(response.text)
    print(response.headers['params'])
    print(f"response_list1=====>'{res}'")


if __name__ == '__main__':
    url = "http://114.141.177.5:22016/v2/tick"
    request_run()

















