# -*- coding: utf-8 -*-
import hashlib
import os
from util.base93 import decode
import yaml


def md5(msg):
    # 使用 hashlib.md5() 创建MD5 hash 对象。
    md5_hash = hashlib.md5()
    # 调用 update() 方法将要加密的消息作为参数传递给它，并使用 encode('utf-8') 将字符串编码为字节串
    md5_hash.update(msg.encode('utf-8'))
    # 使用 hexdigest() 方法获取加密后的结果，以十六进制字符串的形式返回
    md5_msg = md5_hash.hexdigest()
    return md5_msg

# mdg = "赵公子"
# print(md5(msg=mdg))


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        return yaml.safe_load(fp)


yaml_path = rootPath + '/testCase/quote/line.yaml'
data = quote_yaml(yaml_path)


def decode_quote(msg):
    res_list = msg.split("\x03")
    list_result = []
    # print("第1步=======   %s" % (res_list[-1]))
    if res_list[-1] == '':
        res_list.remove('')
    for m in range(len(res_list)- 1):
        split_list = res_list[m].split("\x02")
        # print("第2步=======   %s" % (split_list))
        for i in range(len(split_list)):
            data_key = list(data[i].keys())[0]
            data_values = list(data[i].values())[0]
            # print("第3步=======   %s" % (data_key))
            # print("第4步=======   %s" % (data_values))
            if data_values == 'Y':
                split_list[i] = decode(split_list[i])
        # print("第66666步=======   %s" % (split_list))
        list_result.append(split_list)
        # print("第5步=======   %s" % (split_list[i]))
    print(len(list_result))