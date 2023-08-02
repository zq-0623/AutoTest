# -*-coding:GBK -*-
import json
import os
from contextlib import ExitStack


def deal_file(path1, path2):
    data_name1 = os.listdir(path1)
    data_name2 = os.listdir(path2)
    list1 = get_name(data_name1)
    list2 = get_name(data_name2)
    # 获取list1，list2的交集
    intersection = list(set(list1).intersection(set(list2)))
    # 获取list1中有而list2没有的
    diff1 = list(set(list1).difference(set(list2)))
    # 获取list2中有而list1没有的
    diff2 = list(set(list2).difference(set(list1)))
    if diff1:
        print(str(path1) + " 中有而 " + str(path2) + " 中没有的文件 ", diff1)
    if diff2:
        print(str(path2) + " 中有而 " + str(path1) + " 中没有的文件 ", diff2)
    # 用例写入yaml文件
    try:
        with ExitStack() as stack:
            yml_output = stack.enter_context(open('../testCase/excel/excel.yaml', 'w', encoding='utf-8'))
            yml_output.write(json.dumps(intersection))
    except IOError as e:
        print("Error: " + format(str(e)))
        raise


# 获取文件夹下所有文件名
def get_name(data_name):
    file_name = []
    for i in data_name:
        file_name.append(i)
    return file_name
