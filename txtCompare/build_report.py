# -*- coding: utf-8 -*-
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
# print(sys.path)

import json
import time
from contextlib import ExitStack
from deepdiff import DeepDiff

date1 = time.strftime('%Y%m%d', time.localtime())  # 当前日期
time1 = time.strftime('%H%M%S', time.localtime())  # 当前时间
# 线程数y
num = 5

path1 = r'E:\AllStock_BanKuai\20241128\cs_AllStock_BanKuai\cs_AllStock_BanKuai'
path2 = r'E:\AllStock_BanKuai\20241128\qz_AllStock_BanKuai\qz_AllStock_BanKuai'
# 比对结果存放路径
result_path = 'result'

name = "码表板块文件比对测试报告"

file_name1 = set()
file_name2 = set()
file_dict1 = dict()
file_dict2 = dict()
true_list = []
false_list = []
case_list = []
set_item_removed = []
set_item_added = []

# # 当前时间
# time1 = time.strftime('%H%M%S', time.localtime())
# # 比对结果存放路径
# result_path = 'result'

if __name__ == '__main__':
    # 输出所有文件和文件夹
    for root, dirs, files in os.walk(path1):
        for file in files:
            path = os.path.join(root, file)
            file_name1.add(file)
            file_dict1[str(file)] = os.path.join(root, file)

    for root, dirs, files in os.walk(path2):
        for file in files:
            path = os.path.join(root, file)
            # print(path, file)
            file_name2.add(file)
            file_dict2[str(file)] = os.path.join(root, file)
            # with open(path, 'r', encoding='utf-8') as stock:
            #     txt_list = json.load(stock)
    add_list = DeepDiff(file_name1, file_name2)
    if 'set_item_removed' in add_list:
        set_item_removed = add_list['set_item_removed']
    if 'set_item_added' in add_list:
        set_item_added = add_list['set_item_added']
    same_list = list(file_name1.intersection(file_name2))
    same_list.sort()  # code排序；无返回值
    # print(same_list)
    for i in same_list:
        json1 = {'path1': str(file_dict1[i]), 'path2': str(file_dict2[i]),
                 'set_item_removed': str(set_item_removed),
                 'set_item_added': str(set_item_added)}
        case_list.append(json1)
        # case_list[str(i)] = file_dict2[i]
    # print(case_list)
    # 用例写入yaml文件
    try:
        with ExitStack() as stack:
            yml_output = stack.enter_context(open(rootPath + '/testCase/txt/txt.yaml', 'w', encoding='gbk'))
            yml_output.write(json.dumps(case_list))
    except IOError as e:
        print("Error: " + format(str(e)))
        raise
    os.system(f'pytest -m txtCompare -n {num} --alluredir  ./result/  --clean-alluredir')  # 生成测试结果
    # 添加环境参数
    os.system('copy  ..\\environment.properties  result\\environment.properties')
    os.system(f'allure generate ./result/ -o ./report/{date1}/{time1}/  ')  # 生成测试报告

# os.system(f'allure generate ./result/{date1}/{time1}/ -o ./report/{date1}/{time1}/')  # 生成测试报告
os.system(f'allure serve ./result/')  # allure server开启http服务
# # 自定义网页标题
# set_title(f'report/{date1}/{time1}/index.html', name)
# # #

# reportName_path = f'report/{date1}/{time1}/widgets/summary.json'
# report_name = get_json_data(reportName_path, name)
# sys.path.append(os.path.dirname(sys.path[0]))
# # 判断存放路径是否存在
# if os.path.exists(result_path):
#     pass
# else:
#     os.makedirs(result_path)
