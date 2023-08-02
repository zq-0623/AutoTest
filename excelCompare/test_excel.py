# -*-coding:GBK -*-
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pytest
import yaml

from excelCompare.excel_compare import compare_excel


class ExcelCompareTest:
    # def setup_method(self):
    #     print("初始化。。。")
    @pytest.mark.excelCompare
    @pytest.mark.flaky(reruns=0, reruns_delay=0)
    @pytest.mark.parametrize("item", yaml.safe_load(open('../testCase/excel/excel.yaml', encoding="utf-8")))
    def excel_test(self, item):
        assert compare_excel(item)
