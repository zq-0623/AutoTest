import pandas as pd


def compare_data(data1, sheetname1, data2, sheetname2):
    # ��ȡ������
    dt1 = pd.read_excel(data1, sheet_name=sheetname1)
    dt2 = pd.read_excel(data2, sheet_name=sheetname2)
    # ȷ����׼��
    dt1_name = dt1['����'].values.tolist()
    dt2_name = dt2['����'].values.tolist()
    count = 0
    for i in dt1_name:
        if i in dt2_name:
            dt1_row = dt1.loc[dt1['name'] == i]
            dt2_row = dt2.loc[dt2['name'] == i]
            # ����ѡ�����Ƚϵ���
            dt1_row_ = dt1_row.loc[:, dt1_row.columns.difference(['�Ա�', 'סַ'])]
            dt2_row_ = dt2_row.loc[:, dt2_row.columns.difference(['�Ա�', 'סַ'])]
            # �ж������Ƿ�����һ��
            if dt1_row_.equals(dt2_row_):
                pass
            else:
                # count����
                count += 1
                # ����Ҫ������ļ�����mode='a'���Կ�������д��csv�ļ�
                dt1_row.to_csv(r'test.csv', index=False, mode='a', header=None)
                dt2_row.to_csv(r'test.csv', index=False, mode='a', header=None)

        else:
            print("ƥ��ʧ�ܵ�������", i)
    # ͬ�����Է������Ƚ�һ��
    for j in dt2_name:
        if j not in dt1_name:
            print("ƥ��ʧ�ܵ�������", j)
    print("##############################")
