# -*-coding:GBK -*-
import json
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import time
from util.deal_file import deal_file

# 线程数
num = 1
date1 = time.strftime('%Y%m%d', time.localtime())  # 当前日期
time1 = time.strftime('%H%M%S', time.localtime())  # 当前时间
# config路径
config_path = f'F:\\testCase\\ExcelCompare\\{date1}\\config.txt'
# 读取配置文件
with open(config_path, 'r', encoding='gbk') as fp:
    # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
    config_data = json.load(fp)
    data_path1 = config_data['data_path1']
    data_path2 = config_data['data_path2']
    env1 = config_data['env1']
    env2 = config_data['env2']
    file_type = config_data['file_type']
    key = config_data['key']
    # print(config_data)

# 环境名称

# 比对结果存放路径
result_path = 'file'
# 文件类型，可选excel，csv

# 共有文件名列表
file_list = []

if __name__ == '__main__':
    # 判断存放路径是否存在
    if os.path.exists(result_path):
        pass
    else:
        os.makedirs(result_path)
    file_list = deal_file(data_path1, data_path2)
    os.system(f'pytest -m excelCompare -n {num} --alluredir  ./result/  --clean-alluredir')  # 生成测试结果

    # 添加环境参数
    os.system('copy  ..\\environment.properties  result\\environment.properties')
    # os.system(f'allure generate ./result/ -o ./report/')  # 生成测试报告
