import csv
import json
from contextlib import ExitStack

import yaml


# 读取用例模板，拼接动态参数，组合生成用例yaml文件
def env_replace_yaml(json_file, yaml_file):
    with open(json_file, 'r', encoding='utf-8') as fp:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        data = json.load(fp)
        try:
            with ExitStack() as stack:
                yml_output = stack.enter_context(open(yaml_file, 'w', encoding='utf-8'))
                for k in data:
                    if 'csv_path' in k:
                        csv_path = k['csv_path']
                        profileList = []
                        with open(csv_path, 'r', encoding='utf-8') as csv_file:
                            reader = csv.DictReader(csv_file)
                            for row in reader:
                                profileList.append(dict(row))
                        k = [k]
                        yaml_datas = yaml.dump(k, indent=5, sort_keys=False, allow_unicode=True)  # 将字典的内容转换为yaml格式的字符串
                        for i in range(0, len(profileList)):
                            # 逐行读取内容
                            for line in yaml_datas.split('\n'):
                                new_line = line
                                # 如果找到以“$csv{”开头的字符串
                                if new_line.find('$csv{') > 0:
                                    # 对字符串以“:”切割
                                    env_list = new_line.split(':')
                                    # 取“:”后面的部分，去掉首尾空格，再以“{”切割，再以“}”切割取出变量名称，比如“name”
                                    env_name = env_list[1].strip().split('{', 1)[1].split('}')[0]
                                    replacement = ""
                                    # 如果name在字典列表的key里
                                    if env_name in profileList[i].keys():
                                        # 取出name对应的值赋给replacement
                                        replacement = profileList[i][env_name]
                                        # 用replacement替换掉YAML模板中的“$csv{name}”
                                        for j in range(0, len(profileList)):
                                            new_line = new_line.replace(env_list[1].strip(), replacement)
                                # 将new_line写入到yml_output文件里
                                yml_output.write(new_line + '\n')
                            yml_output.write("\n\n")
                    else:
                        k = [k]
                        yaml_datas = yaml.dump(k, indent=5, sort_keys=False, allow_unicode=True)  # 将字典的内容转换为yaml格式的字符串
                        # 逐行读取内容
                        for line in yaml_datas.split('\n'):
                            new_line = line
                            # 将new_line写入到yml_output文件里
                            yml_output.write(new_line + '\n')
                        yml_output.write("\n\n")



        except IOError as e:
            print("Error: " + format(str(e)))
            raise
