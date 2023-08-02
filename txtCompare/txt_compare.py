# -*- coding: utf-8 -*-
import json
import os
import sys

import allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
# print(sys.path)
from itertools import groupby
from operator import itemgetter
from deepdiff import DeepDiff


# 定义函数，用于比较两个文本文件
def compare_txt(item):
    # 获取路径1和路径2
    path1 = item['path1']
    path2 = item['path2']
    # 获取添加的列表（暂未使用）和打印该列表
    # add_list = item['add_list']
    # print(add_list)
    # 读取路径1和路径2的文本内容
    content1 = read_content(path1)
    content2 = read_content(path2)
    # 对文本内容进行按键排序和分组
    content1 = key_sort_group(content1)
    content2 = key_sort_group(content2)
    # 比较文本内容的不同之处
    compare_result = DeepDiff(content1, content2)

    # 如果不同之处存在
    if compare_result:
        # 如果存在环境1中有而环境2中没有的文件
        if item['set_item_removed'] != '[]':
            # print("环境1中有而环境2中没有的文件： \n" + item['set_item_removed'])
            # 在allure报告中附加此类文件列表
            allure.attach(item['set_item_removed'], name="环境1中有而环境2中没有的文件")
            # 如果存在环境1中没有而环境2中有的文件
        if item['set_item_added'] != '[]':
            # print("环境1中没有而环境2中有的文件： \n" + item['set_item_added'])
            # 在allure报告中附加此类文件列表
            allure.attach(item['set_item_added'], name="环境1中没有而环境2中有的文件")
        # 在allure报告中附加数据比对的结果
        allure.attach(compare_result.pretty(), name="比对结果")
        # 返回结果为False，表示存在不同之处
        return False
    # 如果没有不同之处
    else:
        # 如果存在环境1中有而环境2中没有的文件
        if item['set_item_removed'] != '[]':
            # print("环境1中有而环境2中没有的文件： \n" + item['set_item_removed'])
            # 在allure报告中附加此类文件列表
            allure.attach(item['set_item_removed'], name="环境1中有而环境2中没有的文件")
        # 如果存在环境1中没有而环境2中有的文件
        if item['set_item_added'] != '[]':
            # print("环境1中没有而环境2中有的文件： \n" + item['set_item_added'])
            # 在allure报告中附加此类文件列表
            allure.attach(item['set_item_added'], name="环境1中没有而环境2中有的文件")
        # 在allure报告中附加数据比对一致的结果
        allure.attach("数据比对一致", name="比对结果")
        # 返回结果为True，表示没有不同之处
        return True
    # print(len(true_list))
    # print(len(false_list))

    # # 获取文件名的前后缀
    # file_ext = os.path.splitext(item)
    # front, ext = file_ext
    # # excel转dict并分组排序
    # resp1 = key_sort_group(excel_dict(data_path1, item))
    # resp2 = key_sort_group(excel_dict(data_path2, item))
    # # 结果比对
    # compare_result = DeepDiff(resp1, resp2,ignore_order_func=lambda level: "JSONExtend(29)" in level.path())
    # envList1 = []
    # envList2 = []
    # key_list = []
    # code_list = []
    # field_list = []
    # json1 = {}
    # # 判断比对结果
    # if compare_result:
    #     # print("错误的：", item)
    #     # 获取比对不上的字段
    #     if 'values_changed' in compare_result:
    #         values_changed = compare_result['values_changed']
    #         key_list = list(values_changed.keys())
    #         val_list = list(values_changed.values())
    #         for i in val_list:
    #             old_value = i['old_value']
    #             new_value = i['new_value']
    #             envList1.append(old_value)
    #             envList2.append(new_value)
    #         # 截取股票代码以及字段
    #         for j in key_list:
    #             # print(j)
    #             m = re.findall(r'\[\'(.*?)\'\]', j)
    #             code_list.append(m[0])
    #             field_list.append(m[1])
    #     # 获取多的字段
    #     if 'iterable_item_added' in compare_result:
    #         iterable_item_added = compare_result['iterable_item_added']
    #         print(iterable_item_added)
    #         # code_list.append(iterable_item_added)
    #     # 获取少的字段
    #     if 'iterable_item_removed' in compare_result:
    #         iterable_item_removed = compare_result['iterable_item_removed']
    #         print(iterable_item_removed)
    #         # code_list.append(iterable_item_removed)
    #     # code_list.append(key_list)
    #     json1 = {'股票名称': code_list, '字段名': field_list, env1: envList1, env2: envList2}
    #     write_excel(json1, front)
    #     # false_result.append(front)
    #     return False
    # else:
    #     # print("正确的：", item)
    #     json1 = {'比对结果': ['完全相同']}
    #     write_excel(json1, front)
    #     # true_result.append(front)
    #     return True


def read_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as stock:
        txt_list = json.load(stock)
        return txt_list


# 排序分组
def key_sort_group(data):
    """对列表中dict数据指定key排序，分组"""
    data.sort(key=itemgetter('s'))  # code排序；无返回值
    # print(data)
    result = dict()
    for code, items in groupby(data, key=itemgetter('s')):  # 按照code分组
        result[str(code)] = list(items)
    return result

# # 结果写入excel
# def write_excel(json, item):
#     # print(time1)
#     write_path = f'{result_path}/{time1}_快照比对结果.xlsx'
#     if not os.path.exists(write_path):
#         ew = pd.ExcelWriter(write_path)
#         data = pd.DataFrame(json)
#         data.to_excel(ew, sheet_name=item, index=False)
#         ew.close()
#     else:
#         # wb = load_workbook(write_path, mode='a', engine='openpyxl')
#         ew = pd.ExcelWriter(write_path, mode='a', engine='openpyxl')
#         # ew.book = wb
#         data = pd.DataFrame(json)
#         data.to_excel(ew, sheet_name=item, index=False)
#         ew.close()
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
