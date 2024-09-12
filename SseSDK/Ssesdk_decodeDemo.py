# -*-coding:utf-8 -*-
import os
from util.logTool import logger

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
    for m in range(len(res_list)- 1):
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
        "symbol":"H11082.csi",
        # 'param': '931,100,-1'
        # "param":"20050531"
    }
    response = SseOptionQuote(url, headers=headers)
    res = decode_quote(response.text)
    print(f"response_list1=====>'{res}'")


if __name__ == '__main__':
    url = "http://114.141.177.5:22016/v4/line5d"
    request_run()

















