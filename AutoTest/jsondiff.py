# encoding=utf-8
import json
from deepdiff import DeepDiff

# 加载json文件内容
with open('TestFile/setServerIp.json', 'r') as file:
    json1 = json.load(file)

with open('TestFile/setServerIp1.json', 'r') as file:
    json2 = json.load(file)

# 比较json内容
diff = DeepDiff(json1, json2, ignore_order=True)

# 输出不同之处
print("不一致的json数据:")
print(diff)

