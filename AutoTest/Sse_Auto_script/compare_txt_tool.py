"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest 
@File    ：compare_txt_tool.py
@IDE     ：PyCharm 
@Author  ：ZhaoQiang
@Date    ：2024/11/20 星期三 10:31 
"""


def compare_files(file1, file2):
    try:
        # 读取文件1内容并去重
        with open(file1, 'r', encoding='utf-8') as f1:
            content1 = set(line.strip() for line in f1 if line.strip())

        # 读取文件2内容并去重
        with open(file2, 'r', encoding='utf-8') as f2:
            content2 = set(line.strip() for line in f2 if line.strip())

        # 比较内容
        only_in_file1 = content1 - content2  # 文件1独有内容
        only_in_file2 = content2 - content1  # 文件2独有内容
        common_content = content1 & content2  # 两个文件共有的内容

        # 输出对比结果
        # print("\033[32m文件内容对比结果：")
        # if only_in_file1:
        #     print(f"\033[31m仅存在于环境1中的IP的数量：{len(only_in_file1)}")
        #     print("\033[31m仅存在于环境1中的IP：")
        #     for line in only_in_file1:
        #         print(line)
        # else:
        #     print("\033[32m文件1中无独有内容。")

        # if only_in_file2:
        #     print(f"\033[31m仅存在于环境2中的IP的数量：{len(only_in_file2)}")
        #     # print("\033[31m仅存在于环境2中的IP：")
        #     pass
        #     for line in only_in_file2:
        #         print(line)
        # else:
        #     print("\033[32m文件2中无独有内容。")

        if common_content:
            print(f"\033[32m两个文件共有的内容数量: {len(common_content)}")
            print("\033[32m两个环境一致的IP：")
            for line in common_content:
                print(line)
        else:
            print("\033[31m两个文件没有共有内容。")

    except FileNotFoundError as e:
        print(f"\033[31m文件不存在: {e}")
    except Exception as e:
        print(f"\033[31m发生错误: {e}")


if __name__ == "__main__":
    # 输入文件路径
    # file1_path = "../TestFile/response_output.txt"  # 替换为您的文件1路径
    # file2_path = "../TestFilele/response_output.txt"  # 替换为您的文件1路径

    file1_path = "../TestFile/trade_response.txt"  # 替换为您的文件1路径
    file2_path = "../TestFile/all_response.txt"  # 替换为您的文件2路径

    # 调用对比函数
    compare_files(file1_path, file2_path)
