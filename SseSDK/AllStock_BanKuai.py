# -*- coding: utf-8 -*-
import json


def extract_stock(path):
    try:
        with open(path,'r',encoding='utf-8') as stock:
            stock_list = json.load(stock)
            stock_length = len(stock_list)
            for stock_i in stock_list:
                # stock_p = stock_i.get('p')
                # stock_st = stock_i.get('st')
                stock_s = stock_i.get('s')
                # stock_t = stock_i.get('t')
                stock_f = stock_i.get('f')
                stock_n = stock_i.get('n')
                # print("stock=====>",stock_s)
                print(stock_s)
            print("size：",stock_length)
    except IOError as e:
        print("Error：" + format(str(e)))
        raise


if __name__ == '__main__':
    stock_path = f'../testCase/AllStock/BanKuai_SZ1120.txt'
    extract_stock(stock_path)
