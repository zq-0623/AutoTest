#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：AutoTest 
@File    ：txt_excel.py
@IDE     ：PyCharm 
@Author  ：Qiang zhao
@Date    ：2024/10/8 11:16 
"""
from deepdiff import DeepDiff


def compare_lists(list1, list2):
    diff = DeepDiff(list1, list2, ignore_order=True)
    if not diff:
        print("{}对比结果一致")
    else:
        if 'values_changed' in diff:
            values_changed = diff['values_changed']
            for key, change in values_changed.items():
                index = int(key.split('[')[-1].split(']')[0])
                old_value = change['old_value']
                new_value = change['new_value']
                print('环境1：{}，环境2：{}'.format(old_value, new_value))

        if 'iterable_item_added' in diff:
            items_added = diff['iterable_item_added']
            for key, new_value in items_added.items():
                # print("iterable_item_added_new_value:",new_value)
                # results.append({'代码': symbol, url1: None, url2: new_value})
                print('环境2比环境1新增字段：{}'.format( new_value, ))

        if 'iterable_item_removed' in diff:
            items_removed = diff['iterable_item_removed']
            for key, old_value in items_removed.items():
                # print("iterable_item_removed_old_value:",old_value)
                # results.append({'代码': symbol, '字段': field_name, url1: old_value, url2: None})
                print('环境2比环境1移除字段：{}'.format( old_value))


list1 = [
    ['S', 14552360, 10420, 10420, 10430, 5000, 0],
    ['B', 14551805, 10430, 10420, 10430, 1600, 0],
    ['S', 14551597, 10420, 10420, 10430, 2800, 0],
    ['S', 14551357, 10420, 10420, 10430, 2700, 0],
    ['B', 14551027, 10430, 10420, 10430, 1500, 0],
    ['S', 14550872, 10420, 10420, 10430, 17800, 0],
    ['B', 14550427, 10430, 10420, 10430, 2500, 0],
    ['S', 14550238, 10420, 10420, 10430, 4200, 0],
    ['B', 14545936, 10430, 10420, 10430, 24700, 0]
]

list2 = [
    ['S', 14552360, 10420, 10450, 10430, 5000, 0],
    ['B', 14551805, 10430, 10420, 10430, 1600, 0],
    ['S', 14551597, 10420, 10420, 10430, 2800, 0],
    ['S', 14551357, 10420, 10420, 10430, 2700, 0],
    ['S', 14550872, 10420, 10420, 10430, 17800, 0],
    ['B', 14550427, 10430, 10420, 10430, 2500, 0],
    ['S', 14550238, 10420, 10450, 10430, 4200, 0],
    ['B', 14545555, 10430, 10420, 10430, 2600, 0]
]

# 进行比较
compare_lists(list1, list2)
