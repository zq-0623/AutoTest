# -*-coding:GBK -*-
import os
import re
import sys

import allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from itertools import groupby
from operator import itemgetter

import pandas as pd
from deepdiff import DeepDiff

from excelCompare.build_report import file_type, data_path1, data_path2, result_path, env1, env2, time1, key, date1


# excel数据比对
def compare_excel(item):
    # print(item)
    # 获取文件名的前后缀
    file_ext = os.path.splitext(item)
    front, ext = file_ext
    # excel转dict并分组排序
    resp1 = key_sort_group(excel_dict(data_path1, item))
    resp2 = key_sort_group(excel_dict(data_path2, item))
    # 结果比对
    compare_result = DeepDiff(resp1, resp2)
    # print(compare_result.pretty())
    envList1 = []
    envList2 = []
    key_list = []
    code_list = []
    field_list = []
    json1 = {}
    # 判断比对结果
    if compare_result:
        # print("错误的：", item)
        # 获取比对不上的字段
        if 'values_changed' in compare_result:
            values_changed = compare_result['values_changed']
            key_list = list(values_changed.keys())
            val_list = list(values_changed.values())
            for i in val_list:
                old_value = i['old_value']
                new_value = i['new_value']
                envList1.append(old_value)
                envList2.append(new_value)
            # 截取股票代码以及字段
            for j in key_list:
                # print(j)
                m = re.findall(r'\[\'(.*?)\'\]', j)
                code_list.append(m[0])
                field_list.append(m[1])
        # 获取多的字段
        if 'iterable_item_added' in compare_result:
            iterable_item_added = compare_result['iterable_item_added']
            key_list.append(iterable_item_added)
        # 获取少的字段
        if 'iterable_item_removed' in compare_result:
            iterable_item_removed = compare_result['iterable_item_removed']
            key_list.append(iterable_item_removed)
        json1 = {'股票名称': code_list, '字段名': field_list, env1: envList1, env2: envList2}
        write_excel(json1, front)
        # false_result.append(front)
        return False
    else:
        print("比对结果：\n数据比对一致")
        # print("正确的：", item)
        # json1 = {'比对结果': ['完全相同']}
        # write_excel(json1, front)
        # true_result.append(front)
        return True


# excel转dict
def excel_dict(path, item):
    df = None
    if file_type == 'excel':
        df = pd.read_excel(f'{path}/{item}', dtype='object', encoding="gbk")
    elif file_type == 'csv':
        df = pd.read_csv(f'{path}/{item}', dtype='object', encoding="gbk")
    res = df.to_dict(orient="records")
    return res


#
# 排序分组
def key_sort_group(data):
    """对列表中dict数据指定key排序，分组"""
    data.sort(key=itemgetter(key))  # code排序；无返回值
    # print(data)
    result = dict()
    for code, items in groupby(data, key=itemgetter(key)):  # 按照code分组
        result[str(code)] = list(items)
    return result


# 结果写入excel
def write_excel(json, item):
    # print(time1)
    write_path = f'{result_path}/{date1}{time1}_比对结果.xlsx'
    if not os.path.exists(write_path):
        ew = pd.ExcelWriter(write_path)
        data = pd.DataFrame(json)
        data.to_excel(ew, sheet_name=item, index=False)
        ew.close()
    else:
        # wb = load_workbook(write_path, mode='a', engine='openpyxl')
        ew = pd.ExcelWriter(write_path, mode='a', engine='openpyxl')
        # ew.book = wb
        data = pd.DataFrame(json)
        data.to_excel(ew, sheet_name=item, index=False)
        ew.close()
    allure.attach.file(write_path, name=item + "比对结果", extension="xlsx")

    # if os.path.exists(write_path):
    #     pass
    # else:
    #     # 如果不存在创建文件
    #     f = open(write_path, 'w')
    #     f.close()
    # # book = load_workbook(write_path)
    # writer = pd.ExcelWriter(write_path, mode='a', engine='openpyxl')
    # # writer.book = book
    # data = pd.DataFrame(json)
    # data.to_excel(writer, sheet_name=item, index=False)
    # writer.save()

    #
    # if __name__ == '__main__':
    #     deal_excel(data_path1, data_path2)
