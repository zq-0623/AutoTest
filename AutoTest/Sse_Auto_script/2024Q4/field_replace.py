"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest 
@File    ：field_replace.py
@IDE     ：PyCharm 
@Author  ：ZhaoQiang
@Date    ：2024/12/31 星期二 16:35 
"""
import json


def replace_s_field(json_file, mapping_file, output_file):
    """
    替换 JSON 文件 A 中的 "s" 字段值，保留 ".bz" 后缀。
    替换码表文件中北证的代码，8和4开头的所有北证代码替换成920开头的代码。

    :param json_file: 文件 A 的路径（JSON 格式）
    :param mapping_file: 文件 B 的路径（以 "|" 分隔的映射数据）
    :param output_file: 输出文件路径
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(mapping_file, 'r', encoding='utf-8') as f:
        mappings = f.readlines()

    mapping_dict = {}
    for line in mappings:
        parts = line.strip().split('|')
        if len(parts) == 2:
            key, value = parts
            mapping_dict[key] = value

    for idx, entry in enumerate(data):
        original_s = entry.get('s', '')
        if original_s.endswith('.bz'):
            base_key = original_s.split('.')[0]  # 去掉 .bz 后的键值
            if base_key in mapping_dict:
                # 替换 "s" 字段值
                new_s = f"{mapping_dict[base_key]}.bz"
                data[idx]['s'] = new_s

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"更新后的 JSON 数据已保存到 {output_file}")


json_file = 'AllStock_bz.txt'  # 文件 A 的路径
mapping_file = '1.txt'  # 文件 B 的路径
output_file = 'AllStock_bz1.txt'  # 输出文件路径

replace_s_field(json_file, mapping_file, output_file)
