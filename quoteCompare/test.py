# -*-coding:GBK -*-
# ÿ��������Ĺ�Ʊ����
import json
interval = 50


def interval_stock(path):
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
    print(stock_list)


interval_stock("../testCase/AllStock/AllStock_sz.txt")