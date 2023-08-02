import os
import sys

import requests

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

write_path = curPath + f'\\result\\mqttResult'
path1 = f'D:\\workspace\\TestFile\\EveryDayData\\20230606\\AllStock_Bankuai\\cs_AllStock_BanKuai'
file_name1 = set()
file_dict1 = dict()


request = requests.session()
request.keep_alive = False
request.get()


