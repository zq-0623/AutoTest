# -*-coding:GBK -*-
import json
import os
from contextlib import ExitStack


def deal_file(path1, path2):
    data_name1 = os.listdir(path1)
    data_name2 = os.listdir(path2)
    list1 = get_name(data_name1)
    list2 = get_name(data_name2)
    # ��ȡlist1��list2�Ľ���
    intersection = list(set(list1).intersection(set(list2)))
    # ��ȡlist1���ж�list2û�е�
    diff1 = list(set(list1).difference(set(list2)))
    # ��ȡlist2���ж�list1û�е�
    diff2 = list(set(list2).difference(set(list1)))
    if diff1:
        print(str(path1) + " ���ж� " + str(path2) + " ��û�е��ļ� ", diff1)
    if diff2:
        print(str(path2) + " ���ж� " + str(path1) + " ��û�е��ļ� ", diff2)
    # ����д��yaml�ļ�
    try:
        with ExitStack() as stack:
            yml_output = stack.enter_context(open('../testCase/excel/excel.yaml', 'w', encoding='utf-8'))
            yml_output.write(json.dumps(intersection))
    except IOError as e:
        print("Error: " + format(str(e)))
        raise


# ��ȡ�ļ����������ļ���
def get_name(data_name):
    file_name = []
    for i in data_name:
        file_name.append(i)
    return file_name
