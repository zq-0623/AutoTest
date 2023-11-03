# -*-coding:GBK -*-
# 每次请求传入的股票数量
import json
interval = 50


def interval_stock(path):
    stock_list = []
    stock_str = ''
    index = 0
    with open(path, 'r', encoding='utf-8') as stock:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        txt_list = json.load(stock)
        txt_length = len(txt_list)
        # 股名表股票数量取余
        num = txt_length % interval
        # 每interval只取出股名表中的股票代码
        # 数量能被interval整除时
        if num == 0:
            for m in range(txt_length):
                stock_str = stock_str + txt_list[m]['s'] + ","
                index = index + 1
                if index >= interval:
                    stock_list.append(stock_str)
                    index = 0
                    stock_str = ''
        # 数量小于interval时
        elif num == txt_length:
            for m in range(txt_length):
                stock_str = stock_str + txt_list[m]['s'] + ","
                stock_list.append(stock_str)
        # 数量不能被interval整除时
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