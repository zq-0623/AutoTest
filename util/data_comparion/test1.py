import pandas
import json
from util import replaceYaml
path1 = r"E:/code/interfaceAutoTest/excelCompare/result/1c69d691-536c-4ca0-9802-9e142f4e7989-container.json"
path2 = "../testCase/interfaceCompare/compare.yaml"
# k = open(path,"r",encoding="utf-8")
# k= json.load(k)
# a = pandas.read_json(path)
# print(a)
replaceYaml.env_replace_yaml(path1,path2)
