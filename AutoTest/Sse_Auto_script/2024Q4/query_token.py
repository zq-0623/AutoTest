"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest 
@File    ：query_token.py
@IDE     ：PyCharm 
@Author  ：ZhaoQiang
@Date    ：2024/11/22 星期五 14:45 
"""


def extract_values_from_txt(input_file, output_file):
    """
    从输入文件中提取指定的值并保存到输出文件中
    :param input_file: 输入 TXT 文件路径
    :param output_file: 输出 TXT 文件路径
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                # 提取时间值，格式为 YYYY-MM-DD HH:MM:SS
                time_part = line.split(" ")[0] + " " + line.split(" ")[1].split(".")[0]

                # 提取 token 值
                token_section = line.split(" ")[2]  # 第三部分内容
                token_parts = token_section.split("-")  # 按 '-' 分割
                token_value = token_parts[2] if len(token_parts) > 2 else "无效token"

                # 将结果写入输出文件
                outfile.write(f"{time_part}, {token_value}\n")

            except IndexError:
                print(f"解析失败的行: {line.strip()}")  # 如果行解析失败则跳过


if __name__ == "__main__":
    input_file_path = "../../TestFile/token_appkey/authlog-20241122.txt"  # 输入文件路径
    output_file_path = "../../TestFile/token_appkey/token_time.txt"  # 输出文件路径
    extract_values_from_txt(input_file_path, output_file_path)
