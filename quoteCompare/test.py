import os
import sys

import requests

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

# print(curPath)
write_path = curPath + f'\\result\\mqttResult'

file_name = set()
file_dict =dict()
path = f'E:\\workspace\\TestFile\\TestData\\20230906\\Allstock_bankuai\\cs_Allstock_bankuai\\cs_AllStock_BanKuai'

for root, dirs, files in os.walk(path):
    for file in files:
        path = os.path.join(root, file)
        file_name.add(file)
        file_dict[str(file)] = os.path.join(root, file)
    print(file_name)
    print(file_dict)




