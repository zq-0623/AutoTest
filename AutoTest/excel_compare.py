import os
import filecmp
import pandas as pd

def compare_excel_files(folder1, folder2):
    excel_files1 = get_excel_files(folder1)
    excel_files2 = get_excel_files(folder2)

    for file1, file2 in zip(excel_files1, excel_files2):
        if filecmp.cmp(file1, file2):
            print(f"Excel files '{file1}' and '{file2}' are identical.")
        else:
            if compare_excel_contents(file1, file2):
                print(f"Excel files '{file1}' and '{file2}' have the same contents.")
            else:
                print(f"Excel files '{file1}' and '{file2}' have different contents.")

def compare_excel_contents(file1, file2):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    return df1.equals(df2)

def get_excel_files(folder):
    excel_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".xlsx") or file.endswith(".xls"):
                file_path = os.path.join(root, file)
                excel_files.append(file_path)
    return excel_files

# 设置两个文件夹路径
folder1 = f"D:\\test1"
folder2 = f"D:\\test2"

# 比较文件夹下的 Excel 文件内容
compare_excel_files(folder1, folder2)
