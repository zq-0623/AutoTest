# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/19 22:13
@Auth ： ZhaoQiang
@File ：test.py
@IDE ：PyCharm
"""
import json
import os
import sys

"""
import io
import time

import requests

try:
    while True:
        # url = 'http://114.80.155.134:22016/v1/cna/line/600490.sh?select=seqNo,time,bbd,ddx,ddy,ddz,ratioBS,' \
        #       'largeMoneyNetInflow,bigMoneyNetInflow,midMoneyNetInflow,smallMoneyNetInflow,largeTradeNum,' \
        #       'bigTradeNum,midTradeNum,smallTradeNum'
        # url = "http://114.80.155.134:22016/v1/cna/block/700002.bk?select=blockID,newBlockId,blockName,blockIndex"
        url = "http://114.80.155.134:22016/v1/cna/line/600157.sh?begin=48&end=-1&select=seqNo,time,bbd,ddx,ddy,ddz,\
        ratioBS,largeMoneyNetInflow,bigMoneyNetInflow"
        # url = "http://114.80.155.134:22016/v1/cna/block/700002.bk?begin=48&end=-1&select=blockID,newBlockId,blockName,blockIndex"

        headers = {'token': 'MitakeWeb', 'symbol': 'getaddvaluelinenew', 'hid': 'testIncrement'}
        filename = 'response2.txt'
        with open(filename, "ab") as file:
            with io.BufferedWriter(file) as buffer_file:
                res = requests.Session().get(url, headers=headers)
                buffer_file.write(res.text.encode() + '\n'.encode())
                # file.write(response.encode() + '\n'.encode())
            time.sleep(3)
except Exception as e:
    print(e)

"""

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

print(curPath)
print(rootPath)

stock_path = f"../../testCase/AllStock"


def test(path):
    with open(path,encoding="utf-8") as stock:
        text_list = json.load(stock)
        txt_length = len(text_list)
        print(text_list)
        print(txt_length)
        stock_list = []
        stock_str = ''
        for m in range(txt_length):
            stock_str = text_list[m]['s'] + ","
            stock_list.append(stock_str)
        print(stock_list)
        print(len(stock_list))


file = "AllStock_bz.txt"
file_path = f'{stock_path}/{file}'
test(file_path)