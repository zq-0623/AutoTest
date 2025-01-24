"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest 
@File    ：json_change_yaml_tool.py
@IDE     ：PyCharm 
@Author  ：ZhaoQiang
@Date    ：2024/11/19 星期二 15:21 
"""

import json

import yaml


# 读取 JSON 文件
def json_to_yaml(json_file_path, yaml_file_path):
    try:
        # 打开并读取 JSON 文件
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)  # 解析 JSON 数据

        # 打开并写入 YAML 文件
        with open(yaml_file_path, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(json_data, yaml_file, default_flow_style=False, allow_unicode=True)  # 转换并写入 YAML

        print(f"文件成功转换为 YAML 格式，保存为 {yaml_file_path}")
    except Exception as e:
        print(f"转换过程中出错: {e}")


# 示例用法
json_file = '../TestFile/setMarketValues'  # 替换为你的 JSON 文件路径
yaml_file = 'output.yaml'  # 目标 YAML 文件路径

json_to_yaml(json_file, yaml_file)
