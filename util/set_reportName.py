import json


# 测试报告文案获取的文件地址

# 获取 summary.json 文件的数据内容
def get_json_data(path, name):
    # 定义为只读模型，并定义名称为f
    with open(path, 'rb') as f:
        # 加载json文件中的内容给params
        params = json.load(f)
        # 修改内容
        params['reportName'] = name
        # 将修改后的内容保存在dict中
        dict = params
    # 关闭json读模式
    f.close()

    # 返回dict字典内容
    return dict


# 写入json文件
def write_json_data(path,dict):
    # 定义为写模式，名称定义为r
    with open(path, 'w', encoding="utf-8") as r:
        # 将dict写入名称为r的文件中
        json.dump(dict, r, ensure_ascii=False, indent=4)
    # 关闭json写模式
    r.close()
