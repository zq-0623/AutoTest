# -*-coding:GBK -*-
'''
import json
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import re
import time
from threading import Thread

import pandas as pd
import requests
import yaml
from deepdiff import DeepDiff
from util.base93 import decode

# ��ǰ����
date1 = time.strftime('%Y%m%d', time.localtime())
# ��ǰʱ��
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
# �����ֶ����ļ�·��
yaml_path = rootPath + '/testCase/quote/quote.yaml'
# �������ļ�·��
stock_path = f'../testCase/AllStock'
# url�ļ�·��
url_path = f'../testCase/quote/url_quote.yaml'
# �ȶԽ�����·��
result_path = 'result'
# ÿ��������Ĺ�Ʊ����
interval = 50
# ��ſ����ֶ�
data = []
# ��Ż���1����
quote_list1 = []
# ��Ż���2����
quote_list2 = []
# �ļ�����
file_name = ""
# ����Ϊ�չ�Ʊ�б�
none_list = []
# �����쳣�Ĺ�Ʊ�б�
exception_list = []


def arr_spits(item, n):
    return [item[i:i + n] for i in range(0, len(item), n)]


# ��ȡ�����ֶ����ļ�
def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        # load()������fp(һ��֧��.read()���ļ�����󣬰���һ��JSON�ĵ�)�����л�Ϊһ��Python����
        return yaml.safe_load(fp)


# �ָ��Ʊ����
def interval_stock(path, item):
    stock_list = []
    stock_str = ''
    index = 0
    with open(path, 'r', encoding='utf-8') as stock:
        # load()������fp(һ��֧��.read()���ļ�����󣬰���һ��JSON�ĵ�)�����л�Ϊһ��Python����
        txt_list = json.load(stock)
        txt_length = len(txt_list)
        # �������Ʊ����ȡ��
        num = txt_length % interval
        # ÿintervalֻȡ���������еĹ�Ʊ����
        # �����ܱ�interval����ʱ
        if num == 0:
            for m in range(txt_length):
                stock_str = stock_str + txt_list[m]['s'] + ","
                index = index + 1
                if index >= interval:
                    stock_list.append(stock_str)
                    index = 0
                    stock_str = ''
        # ����С��intervalʱ
        elif num == txt_length:
            for m in range(txt_length):
                stock_str = stock_str + txt_list[m]['s'] + ","
                stock_list.append(stock_str)
        # �������ܱ�interval����ʱ
        else:
            for m in range(txt_length):
                stock_str = stock_str + txt_list[m]['s'] + ","
                index = index + 1
                if index >= interval:
                    stock_list.append(stock_str)
                    index = 0
                    stock_str = ''
                if m == (txt_length - 1):
                    stock_list.append(stock_str)
    thread_run(stock_list, item)


# ���߳�����ӿ�
def thread_run(stock_list, item):
    thread_array = []
    for i in range(2):
        key = "env" + str(i + 1)
        env = item[key]
        t = Thread(target=request_run, args=(stock_list, env, i))
        thread_array.append(t)
        t.start()
    for t in thread_array:
        t.join()
    compare_result(item)


# �ӿ�����
def request_run(stock_list, env, flag):
    # print(f"�ӿڵ�����....\n",{env})
    for k in stock_list:
        header = {
            'Token': 'MitakeWeb',
            'Symbol': k,
            'Param': '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,'
                     '35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,'
                     '66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,'
                     '97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125| '
        }
        try:
            resp = requests.session().get(url=env, headers=header, verify=False)
            resp_list = resp.text.split("\x03")
            if resp_list[-1] == '':
                resp_list.remove('')
            for m in range(len(resp_list)):
                split_list = resp_list[m].split("\x02")
                quote_dict = dict()
                for i in range(len(split_list)):
                    data_key = list(data[i].keys())[0]
                    data_value = list(data[i].values())[0]
                    # �жϸ��ֶ��Ƿ�ѹ��
                    if data_value == 'Y':
                        # �ֶ�valueת��
                        split_list[i] = decode(split_list[i])
                    quote_dict[data_key] = split_list[i]
                # �ҳ�����Ϊ�յĹ�Ʊ
                if split_list[1] == '':
                    codes = k.split(',')
                    none_str = "���룺" + codes[m] + ",������" + env
                    none_list.append(none_str)
                else:
                    if flag == 0:
                        quote_list1.append(quote_dict)
                    else:
                        quote_list2.append(quote_dict)
        except Exception as e:
            exception_list.append(file_name)
            raise


# ���ձȶ�
def compare_result(item):
    print("��ʼ�ȶ�....")
    print("��Ʊ������", len(quote_list1))
    print("��Ʊ������", len(quote_list2))
    # ����ȶ�
    resp_list1 = DeepDiff(quote_list1, quote_list2, group_by='����')
    # ��Ż���1����
    envList1 = []
    # ��Ż���2����
    envList2 = []
    # ��űȶԲ��ϵĹ�Ʊ��
    code_list = []
    # ��űȶԲ��ϵ��ֶ���
    field_list = []
    # �жϱȶԽ��
    # print("resp_list1",resp_list1)
    if resp_list1:
        # ��ȡ�ȶԲ��ϵ��ֶ�
        if 'values_changed' in resp_list1:
            values_changed = resp_list1['values_changed']
            key_list = list(values_changed.keys())
            val_list = list(values_changed.values())
            for i in val_list:
                old_value = i['old_value']
                new_value = i['new_value']
                envList1.append(old_value)
                envList2.append(new_value)
            # ��ȡ��Ʊ�����Լ��ֶ�
            for j in key_list:
                # print(j)
                m = re.findall(r'\[\'(.*?)\'\]', j)
                code_list.append(m[0])
                field_list.append(m[1])
        json1 = {'��Ʊ����': code_list, '�ֶ���': field_list, item['env1']: envList1, item['env2']: envList2}
        write_excel(json1, file_name)
    else:
        # print("��ȷ�ģ�", item)
        json1 = {'�ȶԽ��': ['��ȫ��ͬ']}
        write_excel(json1, file_name)
    print("�ȶ����д��excel")


def clean_data(value):
    if isinstance(value, str):
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    return value


def sanitize_data(data):
    if isinstance(data, dict):
        return {key: sanitize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(value) for value in data]
    else:
        return clean_data(data)


# ���д��excel
def write_excel(json1, item):
    # ����ļ�������
    write_path = curPath + f'\\result\\quoteResult\\{time1}_������ձȶԽ��.xlsx'
    sanitized_json = sanitize_data(json1)
    wr = pd.DataFrame(sanitized_json)
    if not os.path.exists(write_path):
        with pd.ExcelWriter(write_path) as ew:
            wr.to_excel(ew,sheet_name=item,index=False)
    # ����ļ�����
    else:
        with pd.ExcelWriter(write_path,mode="a",engine='openpyxl') as ew:
            wr.to_excel(ew,sheet_name=item,index=False)


if '__main__' == __name__:
    # �жϴ��·���Ƿ����
    if os.path.exists(result_path):
        pass
    else:
        os.makedirs(result_path)
    # ��ȡ�����ֶ��ļ�
    data = quote_yaml(yaml_path)
    # ��ȡurl�ļ�
    compare_url = quote_yaml(url_path)
    # ��ȡ�������ļ���
    dirs = os.listdir(stock_path)
    # �ȶԻ�����url
    url = None
    for url_key in compare_url.keys():
        url = None
        file = "AllStock_" + url_key + ".txt"
        file_name = url_key
        if url_key == "sh":
            url = compare_url[url_key]
        if url_key == "sz":
            url = compare_url[url_key]
        if url_key == "bz":
            url = compare_url[url_key]
        if url_key == "csi":
            url = compare_url[url_key]
        if url_key == "hk":
            url = compare_url[url_key]
        if url_key == "shl2":
            url = compare_url[url_key]
            file = "AllStock_sh.txt"
        if url_key == "szl2":
            url = compare_url[url_key]
            file = "AllStock_sz.txt"
        # ��Ż���1����
        quote_list1 = []
        # ��Ż���2����
        quote_list2 = []
        print("==============================")
        # print(f"�г���{file_name} \n����1�� {url['env1']}\n����2�� {url['env2']}")

        print("==============================")
        file_path = f'{stock_path}/{file}'
        print(url)
        interval_stock(file_path, url)
        time.sleep(5)  # ����5��
    print("==============================")
    print("����Ϊ�յĹ�Ʊ��")
    print(none_list)
    print("�����쳣�ĵ��г���")
    print(exception_list)


'''
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests
import yaml
from deepdiff import DeepDiff

from util.base93 import decode

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

# ��ǰ���ں�ʱ��
date1 = time.strftime('%Y%m%d', time.localtime())
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())

# �ļ�·��
yaml_path = os.path.join(rootPath, 'testCase/quote/quote.yaml')
stock_path = os.path.join(rootPath, 'testCase/AllStock')
url_path = os.path.join(rootPath, 'testCase/quote/url_quote.yaml')
result_path = os.path.join(rootPath, 'result')

interval = 200  # ÿ��������Ĺ�Ʊ����

none_list = []  # ����Ϊ�չ�Ʊ�б�
exception_list = []  # �����쳣�Ĺ�Ʊ�б�


def arr_spits(item, n):
    return [item[i:i + n] for i in range(0, len(item), n)]


# ��ȡ YAML �ļ�
def load_yaml(path, encoding='gbk'):
    with open(path, 'r', encoding=encoding) as fp:
        return yaml.safe_load(fp)


# �ָ��Ʊ����
def interval_stock(stock_path, interval, item, data, file_name):
    stock_list = []
    with open(stock_path, 'r', encoding='utf-8') as stock:
        txt_list = json.load(stock)
        stock_str = ''
        for i, stock_data in enumerate(txt_list):
            stock_str += stock_data['s'] + ","
            if (i + 1) % interval == 0:
                stock_list.append(stock_str.strip(','))  # ÿ���Ʊ����ȥ�����Ķ���
                stock_str = ''
        if stock_str:  # ����ʣ��Ĺ�Ʊ
            stock_list.append(stock_str.strip(','))
    thread_run(stock_list, item, data, file_name)


# ʹ���̳߳��Ż����߳�����
def thread_run(stock_list, item, data, file_name):
    quote_list1, quote_list2 = [], []
    with ThreadPoolExecutor(max_workers=8) as executor:  # ���� max_workers�����ݻ����������������
        futures = [executor.submit(request_run, stock_list, item[f'env{i + 1}'], i, data) for i in range(2)]
        for future in as_completed(futures):
            result = future.result()
            if result[1] == 0:
                quote_list1.extend(result[0])
            else:
                quote_list2.extend(result[0])
    compare_result(item, data, quote_list1, quote_list2, file_name)


# �������Ż������������������Ի���
def request_run(stock_list, env, flag, data, max_retries=3):
    quote_list = []
    session = requests.Session()  # ʹ�� session ������������Ч��
    for k in stock_list:
        header = {
            'Token': 'MitakeWeb',
            'Symbol': k,
            'Param': '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,'
                     '35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,'
                     '66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,'
                     '97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125| '
        }
        retry_count = 0
        while retry_count < max_retries:  # ���Ի���
            try:
                print(f"����URL��{env}, ��Ʊ���룺{k}")
                resp = session.get(url=env, headers=header, verify=False, timeout=5)  # ���� timeout �� 5 ��
                resp.raise_for_status()  # ������󷵻ش����׳��쳣
                resp_list = [x for x in resp.text.split("\x03") if x]
                for m, stock_data in enumerate(resp_list):
                    split_list = stock_data.split("\x02")
                    quote_dict = {list(data[i].keys())[0]: decode(split_list[i]) if list(data[i].values())[0] == 'Y' else split_list[i] for i in range(len(split_list))}
                    if split_list[1] == '':
                        codes = k.split(',')
                        none_str = f"���룺{codes[m]}, ������{env}"
                        none_list.append(none_str)
                    else:
                        quote_list.append(quote_dict)
                break  # �ɹ��������������ѭ��
            except requests.exceptions.RequestException as e:
                retry_count += 1
                print(f"���� {env} ʧ�ܣ����� {retry_count}/{max_retries} �Σ�{e}")
                if retry_count >= max_retries:
                    exception_list.append(env)  # ���Դ����������ƣ���¼�쳣
    return quote_list, flag


# ���ձȶ�
def compare_result(item, data, quote_list1, quote_list2, file_name):
    print("��ʼ�ȶ�....")
    print(f"��Ʊ���� ����1��{len(quote_list1)}")
    print(f"��Ʊ���� ����2��{len(quote_list2)}")

    diff = DeepDiff(quote_list1, quote_list2, group_by='����')
    if diff:
        if 'values_changed' in diff:
            values_changed = diff['values_changed']
            code_list, field_list, envList1, envList2 = [], [], [], []
            for key, value in values_changed.items():
                envList1.append(value['old_value'])
                envList2.append(value['new_value'])
                code, field = re.findall(r"\['(.*?)'\]", key)
                code_list.append(code)
                field_list.append(field)
            result_data = {
                '��Ʊ����': code_list,
                '�ֶ���': field_list,
                item['env1']: envList1,
                item['env2']: envList2
            }
            write_excel(result_data, file_name)
    else:
        result_data = {'�ȶԽ��': ['��ȫ��ͬ']}
        write_excel(result_data, file_name)
    print("�ȶ����д��excel")


# �����ַ����еķǷ��ַ�
def clean_data(value):
    if isinstance(value, str):
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    return value


def sanitize_data(data):
    if isinstance(data, dict):
        return {key: sanitize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(value) for value in data]
    else:
        return clean_data(data)


def write_excel(json1, file_name):
    # ����ļ�������
    write_path = curPath + f'\\result\\quoteResult\\{time1}_������ձȶԽ��.xlsx'
    sanitized_json = sanitize_data(json1)
    wr = pd.DataFrame(sanitized_json)
    if not os.path.exists(write_path):
        with pd.ExcelWriter(write_path) as ew:
            wr.to_excel(ew, sheet_name=file_name, index=False)
    # ����ļ�����
    else:
        with pd.ExcelWriter(write_path, mode="a", engine='openpyxl') as ew:
            wr.to_excel(ew, sheet_name=file_name, index=False)


if __name__ == '__main__':
    # �������·��
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # ��ȡ����
    data = load_yaml(yaml_path)
    compare_url = load_yaml(url_path)

    all_start_time = time.time()  # Start timing for the entire process

    for url_key, url_item in compare_url.items():
        start_time = time.time()  # Start timing for the current market

        if url_key == 'shl2':
            file_name = 'AllStock_sh.txt'
        elif url_key == 'szl2':
            file_name = 'AllStock_sz.txt'
        else:
            file_name = f"AllStock_{url_key}.txt"

        file_path = os.path.join(stock_path, file_name)
        print(f"�����Ʊ�ļ���{file_name}")
        interval_stock(file_path, interval, url_item, data, url_key)

        end_time = time.time()  # End timing for the current market
        elapsed_time = end_time - start_time
        print(f"�г� {url_key} �����ʱ: {elapsed_time:.2f} ��")

    all_end_time = time.time()  # End timing for the entire process
    all_elapsed_time = all_end_time - all_start_time
    print("==============================")
    print(f"����������̺�ʱ: {all_elapsed_time:.2f} ��")
    print("����Ϊ�յĹ�Ʊ��", none_list)
    print("�����쳣���г���", exception_list)

