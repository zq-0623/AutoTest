# -*-coding:GBK -*-
import os
import time

import requests
import yaml

from Ssesdk_tool import SseOptionQuote, quote_yaml
from util.base93 import decode

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# yaml_path = rootPath + '/testCase/quote/HisRef_file.yaml'
yaml_path = rootPath + '/testCase/quote/Kline.yaml'
data = quote_yaml(yaml_path)


def decode_quote(msg):
    res_list = msg.split("\x03")
    list_result = []
    if res_list[-1] == '':
        res_list.remove('')
    for m in range(len(res_list)- 1):
        split_list = res_list[m].split("\x02")
        for i in range(len(split_list)):
            data_key = list(data[i].keys())[0]
            data_values = list(data[i].values())[0]
            if data_values == 'Y':
                split_list[i] = decode(split_list[i])
            # print(split_list[i])
        list_result.append(split_list)
    return list_result


def request_run():
    headers = {
        "token":"MitakeWeb",
        "symbol":"600600.sh",
        "param":"20050531"
    }
    response = SseOptionQuote(url, headers=headers)
    # print(response.text)
    print(f"response_list1=====>'{decode_quote(response.text)}'")


if __name__ == '__main__':
    url = "http://114.80.155.134:22016/v3/monthk"
    request_run()























