import pandas as pd


def compare_data(data1, sheetname1, data2, sheetname2):
    # 读取两个表
    dt1 = pd.read_excel(data1, sheet_name=sheetname1)
    dt2 = pd.read_excel(data2, sheet_name=sheetname2)
    # 确定基准列
    dt1_name = dt1['姓名'].values.tolist()
    dt2_name = dt2['姓名'].values.tolist()
    count = 0
    for i in dt1_name:
        if i in dt2_name:
            dt1_row = dt1.loc[dt1['name'] == i]
            dt2_row = dt2.loc[dt2['name'] == i]
            # 可以选择不做比较的列
            dt1_row_ = dt1_row.loc[:, dt1_row.columns.difference(['性别', '住址'])]
            dt2_row_ = dt2_row.loc[:, dt2_row.columns.difference(['性别', '住址'])]
            # 判断两行是否内容一致
            if dt1_row_.equals(dt2_row_):
                pass
            else:
                # count计数
                count += 1
                # 导入要保存的文件名，mode='a'可以控制连续写入csv文件
                dt1_row.to_csv(r'test.csv', index=False, mode='a', header=None)
                dt2_row.to_csv(r'test.csv', index=False, mode='a', header=None)

        else:
            print("匹配失败的姓名：", i)
    # 同理，可以反过来比较一下
    for j in dt2_name:
        if j not in dt1_name:
            print("匹配失败的姓名：", j)
    print("##############################")
