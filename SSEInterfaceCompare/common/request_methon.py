import json,requests,traceback
from util.logTool import logger


class RequestsUtil:
    # 通过session会话去关联。session默认的情况下回自动的关联cookie
    session = requests.session()

    def __init__(self, obj):
        self.obj = obj


    def replace_value(self, data):
        if data:
            # 保存数据类型
            data_type = type(data)
            # 判断数据类型
            if isinstance(data, dict) or isinstance(data, list):
                str_data = json.dumps(data)
            else:
                str_data = str(data)
            # 替换
            for cs in range(1, str_data.count('${') + 1):
                if "${" in str_data and "}" in str_data:
                    start_index = str_data.index("${")
                    end_index = str_data.index("}", start_index)
                    old_value = str_data[start_index:end_index + 1]
                    # 反射：通过字类的对象和方法符串调用方法
                    func_name = old_value[2:old_value.index('(')]
                    args_value1 = old_value[old_value.index('(') + 1:old_value.index(')')]
                    if args_value1 != "":
                        if "," in args_value1:
                            args_value2 = args_value1.split(',')
                            new_value = getattr(self.obj, func_name)(*args_value2)
                            print(new_value)
                        else:
                            print("func_name", func_name)
                            new_value = getattr(self.obj, func_name)(args_value1)
                    else:
                        new_value = getattr(self.obj, func_name)
                    # 数字类型去掉“”
                    if isinstance(new_value, int) or isinstance(new_value, float):
                        str_data = str_data.replace('"' + old_value + '"', str(new_value))
                    else:
                        str_data = str_data.replace(old_value, str(new_value))
            # 还原数据类型
            if isinstance(data, dict) or isinstance(data, list):
                data = json.loads(str_data)
            else:
                data = data_type(str_data)
        return data


    def send_request(self, name, method, url, **kwargs):
        try:
            logger.info("--------接口测试开始--------")
            # 基础路径拼接
            url = self.replace_value(url)
            # 请求头和参数替换
            for key, value in kwargs.items():
                if key in ['params', 'data', 'json', 'headers']:
                    kwargs[key] = self.replace_value(value)
                    print(kwargs[key])
                elif key == "files":
                    for file_key, file_path in value.items():
                        value[file_key] = open(file_path, 'rb')
            # 输入信息日志
            logger.info("请求名称：%s" % name)
            logger.info("请求方式：%s" % method)
            logger.info("请求路径：%s" % url)
            if "headers" in kwargs.keys():
                logger.info("请求头：%s" % kwargs["headers"])
            if "params" in kwargs.keys():
                logger.info("请求params参数：%s" % kwargs["params"])
            elif "data" in kwargs.keys():
                logger.info("请求data参数：%s" % kwargs["data"])
            elif "json" in kwargs.keys():
                logger.info("请求json参数：%s" % kwargs["json"])
            if "files" in kwargs.keys():
                logger.info("请求files参数：%s" % kwargs["files"])
            # 请求
            rep = RequestsUtil.session.request(method, url, **kwargs)
            return rep
        except Exception as e:
            logger.error("发送请求send_request异常：%s" % str(traceback.format_exc()))

