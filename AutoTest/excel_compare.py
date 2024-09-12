# -*- coding: utf-8 -*-
import os
import pandas as pd
from util.logTool import logger


def compare_columns(file1_data, file2_data, file1_column, file2_column):
    # 调整行数，使两个文件行数一致
    max_rows = min(len(file1_data), len(file2_data))
    file1_data = file1_data.head(max_rows)
    file2_data = file2_data.head(max_rows)
    # 获取指定列的值并进行比较
    file1_column_values = file1_data[file1_column]
    file2_column_values = file2_data[file2_column]
    # 重置索引以确保比较
    file1_column_values = file1_column_values.reset_index(drop=True)
    file2_column_values = file2_column_values.reset_index(drop=True)
    # 找出不同的结果，包含行号
    different_results = pd.DataFrame({
        '行号': file1_column_values.index + 1,  # 为了从1开始计数
        file1_column: file1_column_values,
        file2_column: file2_column_values
    })
    different_results = different_results[different_results[file1_column] != different_results[file2_column]]
    return different_results



def read_file(file_path):
    _, file_extension = os.path.splitext(file_path)   # '_' 是一个占位符，用于存储 os.path.splitext 返回的文件名和扩展名的元组中的第一个元素
    file_extension = file_extension.lower()
    if file_extension == '.xlsx':
        return pd.read_excel(file_path)
    elif file_extension == '.csv':
        # 读取 CSV 文件
        csv_data = pd.read_csv(file_path, encoding='utf-8')
        # 将 CSV 数据保存为 XLSX 文件
        xlsx_path = file_path.replace('.csv', '.xlsx')
        csv_data.to_excel(xlsx_path, index=False)
        logger.info(f"CSV 文件 {file_path} 已转换为 XLSX 文件 {xlsx_path}")
        # 返回 XLSX 数据
        return pd.read_excel(xlsx_path)
    else:
        raise ValueError(f"不支持的文件类型: {file_extension}")


def compare_files_in_folders(folder1_file, folder2_file, file_pairs):
    for file_name in os.listdir(folder1_file):
        if file_name.endswith('.xlsx') or file_name.endswith('.csv'):
            folder1_file_path = os.path.join(folder1_file, file_name)
            folder2_file_path = os.path.join(folder2_file, file_name)
            logger.info(f"比较 {folder1_file_path} 和 {folder2_file_path} 中的差异:")
            try:
                file1_data = read_file(folder1_file_path)
                file2_data = read_file(folder2_file_path)
                for file1_column, file2_column in file_pairs:
                    result = compare_columns(file1_data, file2_data, file1_column, file2_column)
                    if not result.empty:
                        logger.info(result)
            except Exception as e:
                logger.error(f"比较 {folder1_file_path} 和 {folder2_file_path} 时发生错误: {e}")
    logger.info("=" * 60)


def main():
    folder1 = r"E:\workspace\TestFile\测试场景及记录\北证债券测试\20231216北证测试\306001"
    folder2 = r"E:\workspace\TestFile\测试场景及记录\北证债券测试\20231216北证测试\tick"
    file_pairs = [
        ('TotalVolumeTrade', '成交量'),
        ('MDEntryPx', '最新价')
        # 添加更多列名组合
    ]
    compare_files_in_folders(folder1,folder2,file_pairs)


if __name__ == '__main__':
    main()