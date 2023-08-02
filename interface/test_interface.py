import os
import sys

import allure
import pytest
import yaml

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
# from interface.build_report import yaml_path
from interface.build_report import new_path
from interface.compare import thread_run
from smoke import smoke_run


class InterfaceTest:
    @pytest.mark.smoke
    @pytest.mark.flaky(reruns=2, reruns_delay=2)
    @pytest.mark.parametrize("item", yaml.safe_load(open(new_path, encoding="utf-8")))
    # @allure.step("接口冒烟测试")
    @allure.description("")
    def smoke_test(self, item):
        # 请求参数定义
        allure.dynamic.epic(item["customName"]["epic"])
        allure.dynamic.feature(item["customName"]["feature"])
        allure.dynamic.story(item["customName"]["story"])
        allure.dynamic.title(item["customName"]["title"])
        assert smoke_run(item)

    @pytest.mark.compare
    @pytest.mark.flaky(reruns=0, reruns_delay=0)
    @pytest.mark.parametrize("item", yaml.safe_load(open(new_path, encoding="utf-8")))
    # @allure.step("不同环境下接口返回数据比对测试")
    @allure.description("")
    def compare_test(self, item):
        # 请求参数定义
        allure.dynamic.epic(item["customName"]["epic"])
        allure.dynamic.feature(item["customName"]["feature"])
        allure.dynamic.story(item["customName"]["story"])
        allure.dynamic.title(item["customName"]["title"])
        assert thread_run(item)

    # def test_case3(self):
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Token': 'MitakeWeb',
    #         "Symbol": "600000.sh",
    #         "Param": "-1,,20",
    #         "src": "d"
    #     }
    #     assert smoke_run(headers)
