# # -*- coding: utf-8 -*-
# """
# @Time ： 2023/6/19 22:13
# @Auth ： ZhaoQiang
# @File ：test.py
# @IDE ：PyCharm
# """
# import io
# import time
#
# import requests
#
# try:
#     while True:
#         # url = 'http://114.80.155.134:22016/v1/cna/line/600490.sh?select=seqNo,time,bbd,ddx,ddy,ddz,ratioBS,' \
#         #       'largeMoneyNetInflow,bigMoneyNetInflow,midMoneyNetInflow,smallMoneyNetInflow,largeTradeNum,' \
#         #       'bigTradeNum,midTradeNum,smallTradeNum'
#         # url = "http://114.80.155.134:22016/v1/cna/block/700002.bk?select=blockID,newBlockId,blockName,blockIndex"
#         url = "http://114.80.155.134:22016/v1/cna/line/600157.sh?begin=48&end=-1&select=seqNo,time,bbd,ddx,ddy,ddz,\
#         ratioBS,largeMoneyNetInflow,bigMoneyNetInflow"
#         # url = "http://114.80.155.134:22016/v1/cna/block/700002.bk?begin=48&end=-1&select=blockID,newBlockId,blockName,blockIndex"
#
#         headers = {'token': 'MitakeWeb', 'symbol': 'getaddvaluelinenew', 'hid': 'testIncrement'}
#         filename = 'response2.txt'
#         with open(filename, "ab") as file:
#             with io.BufferedWriter(file) as buffer_file:
#                 res = requests.Session().get(url, headers=headers)
#                 buffer_file.write(res.text.encode() + '\n'.encode())
#                 # file.write(response.encode() + '\n'.encode())
#             time.sleep(3)
# except Exception as e:
#     print(e)
#
#

string = "This guy is a crazy guy."
print(string.find("guy"))