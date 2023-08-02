# -*-coding:GBK -*-
import json
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import time
from util.deal_file import deal_file

# �߳���
num = 1
date1 = time.strftime('%Y%m%d', time.localtime())  # ��ǰ����
time1 = time.strftime('%H%M%S', time.localtime())  # ��ǰʱ��
# config·��
config_path = f'F:\\testCase\\ExcelCompare\\{date1}\\config.txt'
# ��ȡ�����ļ�
with open(config_path, 'r', encoding='gbk') as fp:
    # load()������fp(һ��֧��.read()���ļ�����󣬰���һ��JSON�ĵ�)�����л�Ϊһ��Python����
    config_data = json.load(fp)
    data_path1 = config_data['data_path1']
    data_path2 = config_data['data_path2']
    env1 = config_data['env1']
    env2 = config_data['env2']
    file_type = config_data['file_type']
    key = config_data['key']
    # print(config_data)

# ��������

# �ȶԽ�����·��
result_path = 'file'
# �ļ����ͣ���ѡexcel��csv

# �����ļ����б�
file_list = []

if __name__ == '__main__':
    # �жϴ��·���Ƿ����
    if os.path.exists(result_path):
        pass
    else:
        os.makedirs(result_path)
    file_list = deal_file(data_path1, data_path2)
    os.system(f'pytest -m excelCompare -n {num} --alluredir  ./result/  --clean-alluredir')  # ���ɲ��Խ��

    # ��ӻ�������
    os.system('copy  ..\\environment.properties  result\\environment.properties')
    # os.system(f'allure generate ./result/ -o ./report/')  # ���ɲ��Ա���
