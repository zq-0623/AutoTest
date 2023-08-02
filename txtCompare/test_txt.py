# -*-coding:utf-8 -*-
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
# print(sys.path)
import allure
import pytest
import yaml
from txtCompare.txt_compare import compare_txt


@allure.feature("文件比对")
class TxtCompareTest:
    @pytest.mark.txtCompare
    @pytest.mark.flaky(reruns=0, reruns_delay=0)
    @pytest.mark.parametrize("item", yaml.safe_load(open('../testCase/txt/txt.yaml', encoding="utf-8")))
    @allure.story("码表板块文件比对")
    def txt_test(self, item):
        file_ext = item['path1']
        m = file_ext.split('\\')[-1].split('.')[0]

        # print(str(m))
        allure.dynamic.title(m)
        # allure.attach(item, name="异常文件")

        # print(item)
        assert compare_txt(item)
