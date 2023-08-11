import pandas as pd


def compare_excel_columns(file1_path, file2_path, file1_column, file2_column):
    # 读取文件内容
    file1_data = pd.read_excel(file1_path)
    file2_data = pd.read_excel(file2_path)

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


# 文件和列名列表
file_pairs = [
    ('/Users/luowensai/Downloads/mqtt_line.xlsx', '/Users/luowensai/Downloads/http_line.xlsx', 'r最高价(h)', '高'),
    ('/Users/luowensai/Downloads/mqtt_line.xlsx', '/Users/luowensai/Downloads/http_line.xlsx', 'r最低价(l)', '低'),
    ('/Users/luowensai/Downloads/mqtt_line.xlsx', '/Users/luowensai/Downloads/http_line.xlsx', '日期时间2', '日期时间1'),
    # 添加更多文件和列名组合
]

# 循环比较并打印结果
for file1_path, file2_path, file1_column, file2_column in file_pairs:
    result = compare_excel_columns(file1_path, file2_path, file1_column, file2_column)
    print(f"比较 {file1_path} 中的 '{file1_column}' 和 {file2_path} 中的 '{file2_column}':")
    print(result)
    print("-" * 30)
