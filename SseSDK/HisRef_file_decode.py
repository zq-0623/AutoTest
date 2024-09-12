# -*-coding:utf-8 -*-
import os,json
from util.logTool import logger
from Ssesdk_tool import quote_yaml
from util.base93 import decode

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


# 解码HisRef文件
def decoded_file():
    with open(HisRef_file_path,'r',encoding='utf-8') as file:
        file_txt = file.read()
        dict_txt = json.loads(file_txt)
        HisRef_dict = {}
        decoded_dict = dict()
        for key,value in dict_txt.items():
            for i in range(len(value)):
                data_key = list(data[i].keys())[0]
                data_values = list(data[i].values())[0]
                if data_values == 'Y':
                    value[i] = decode(value[i])
                decoded_dict[data_key] = value[i]
            HisRef_dict[key] = decoded_dict
    logger.info(HisRef_dict)



if __name__ == '__main__':
    yaml_path = rootPath + '/testCase/quote/HisRef.yaml'
    data = quote_yaml(yaml_path)
    HisRef_file_path = r'E:\workspace\PythonProject\AutoTest\SseSDK\TestFile\HisRef_bz20240618.txt'
    decoded_file()

