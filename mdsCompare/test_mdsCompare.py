import allure
import pytest
import yaml

from mdsCompare.build_report import new_path
from mdsCompare.compare import compare_run


class MdsCompareTest:
    @pytest.mark.mdsCompare
    # @pytest.mark.flaky(reruns=0, reruns_delay=0)
    @pytest.mark.parametrize("item", yaml.safe_load(open(new_path, encoding="utf-8")))
    @allure.description("")
    # @allure.step("不同环境下接口返回数据比对测试")
    def compare_test(self, item):
        # 请求参数定义
        allure.dynamic.epic(item["customName"]["epic"])
        allure.feature = allure.dynamic.feature(item["customName"]["feature"])
        allure.dynamic.story(item["customName"]["story"])
        allure.dynamic.title(item["customName"]["title"])
        # allure.attach(body="这是一段文本,setUp", name="", attachment_type=allure.attachment_type.YAML)
        # 处理csv文件
        assert compare_run(item)
