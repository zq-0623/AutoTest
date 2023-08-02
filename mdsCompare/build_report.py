import os
import time


from util.excel_dict import excel_dict
from util.replaceYaml import env_replace_yaml
from util.set_reportName import write_json_data, get_json_data
from util.set_title import set_title

# 线程数
num = 5
# 用例模板路径
model_path = '../testCase/mds/mds.json'
# 新生成的用例yaml路径
new_path = '../testCase/mds/mds.yaml'
# 清洗数据路径
data_path = 'C:/Users/Administrator/Desktop/Minute.csv'
# 清洗文件csv的各列名称，如果需要删除或者忽略某一列数据则命名为删除
columns_name = ['code', 'date', 'prevClose', 'open', 'high', 'low', 'close', 'volume', 'amount', 'iopv', 'fp_volume',
                'fp_amount',
                'avg', '删除', '删除']
# 报告名称
name = "接口自动化测试报告"

date1 = time.strftime('%Y%m%d', time.localtime())  # 当前日期
time1 = time.strftime('%H%M%S', time.localtime())  # 当前时间
# 处理csv文件
csv_result = excel_dict(data_path, columns_name)

if __name__ == '__main__':
    env_replace_yaml(model_path, new_path)
    os.system(f'pytest -m mdsCompare -n {num} --alluredir  ./result/{date1}/{time1}/')  # 生成测试结果
    # 添加环境参数
    os.system('copy  ..\\environment.properties  result\\' + date1 + '\\' + time1 + '\\environment.properties')
    os.system(f'allure generate ./result/{date1}/{time1}/ -o ./report/{date1}/{time1}/')  # 生成测试报告
    # 自定义网页标题
    set_title(f'report/{date1}/{time1}/index.html', "自动化测试报告")
    # 自定义报告名称
    reportName_path = f'report/{date1}/{time1}/widgets/summary.json'
    report_name = get_json_data(reportName_path, name)
    write_json_data(reportName_path, report_name)
