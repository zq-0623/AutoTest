import os
import time

# from replaceYaml import env_replace_yaml
# from set_reportName import write_json_data, get_json_data
# from set_title import set_title
from util.replaceYaml import env_replace_yaml
from util.set_reportName import write_json_data, get_json_data
from util.set_title import set_title

# class Testrun:
#     def run(self):
# from interface.test_interface import get_case

# runType 可填两种值，smoke代表冒烟测试，compare代表数据比对
runType = "compare"
# 线程数
num = 5
# 用例模板路径
model_path = '../testCase/interfaceCompare/compare.json'
# 新生成的用例yaml路径
new_path = '../testCase/interfaceCompare/compare.yaml'
# 报告名称
name = "接口自动化测试报告"

date1 = time.strftime('%Y%m%d', time.localtime())  # 当前日期
time1 = time.strftime('%H%M%S', time.localtime())  # 当前时间

if __name__ == '__main__':
    # 替换yaml中的动态参数
    env_replace_yaml(model_path, new_path)
    os.system(f'pytest -m {runType} -n {num} --alluredir  ./result/{date1}/{time1}/')  # 生成测试结果
    # 添加环境参数
    os.system('copy  ..\\environment.properties  result\\' + date1 + '\\' + time1 + '\\environment.properties')
    os.system(f'allure generate ./result/{date1}/{time1}/ -o ./report/{date1}/{time1}/')  # 生成测试报告
    # os.system(f'allure serve ./result/{date1}/{time1}/')  # allure server开启http服务
    # 自定义网页标题
    set_title(f'report/{date1}/{time1}/index.html', "自动化测试报告")
    # 自定义报告名称
    reportName_path = f'report/{date1}/{time1}/widgets/summary.json'
    report_name = get_json_data(reportName_path, name)
    write_json_data(reportName_path, report_name)
    # os.system(f'http-server  ./report/{date1}/{time1}')
