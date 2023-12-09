# encoding=utf-8
import os
from util.base93 import decode
import requests
import yaml
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
yaml_path = rootPath + '/testCase/quote/quote.yaml'


def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        return yaml.safe_load(fp)


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


if __name__ == '__main__':
    headers = {
        "token": "MitakeWeb",
        "symbol": "SHSZBZ1300",
        "param": "0,50,101,1,1"
    }
    url1 = "http://114.80.155.61:22016/v4/catesorting"
    response = requests.get(url=url1,headers=headers)
    json1 = response.text.split('\x03')
    if json1[-1] == '':
        json1.remove('')
    for m in range(len(json1)):
        split_list = json1[m].split("\x02")
        print(split_list)




