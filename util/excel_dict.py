import pandas as pd
from numpy import dtype
from operator import itemgetter
from itertools import groupby


def excel_dict(path, columns_name):
    # 读取csv并跳过第一行，header不设置表头，加入参数float_precision=“round_trip”, 所有数据会当做string读取
    df = pd.read_csv(path, skiprows=1, header=None, dtype=object)
    # print(df1)
    # 重新给出列名
    df.columns = columns_name
    df = df.drop(columns=["删除"])
    # 指定列的数据类型，避免比对时出现类型不一致的问题
    df['code'] = df['code'].astype(str)
    df['date'] = df['date'].astype(str)
    columns_name.remove('code')
    columns_name.remove('date')
    # print(columns_name)
    # 取出列名指定类型
    for i in columns_name:
        if i != "删除":
            df[i] = df[i].astype(float)
    # to_dict可以把在python中读取到的文件按照列名存入字典中。
    # df.insert(0, 'code', df1)
    # print(df)
    res = df.to_dict(orient="records")
    # print(res)
    return key_sort_group(res)


def key_sort_group(data):
    """对列表中dict数据指定key排序，分组"""
    # 排序
    data.sort(key=itemgetter('code'))  # code排序；无返回值
    # print(data)
    result = dict()
    for code, items in groupby(data, key=itemgetter('code')):  # 按照code分组
        result[str(code)] = list(items)
        data1 = result[str(code)]
        result1 = {}
        for date, items1 in groupby(data1, key=itemgetter('date')):  # 按照date分组
            result1[str(date)] = list(items1)
            result[str(code)] = result1
    return result
