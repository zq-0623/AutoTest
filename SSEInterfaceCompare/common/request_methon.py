import json,requests,traceback
from util.logTool import logger


class RequestsUtil:
    # ͨ��session�Ựȥ������sessionĬ�ϵ�����»��Զ��Ĺ���cookie
    session = requests.session()

    def __init__(self, obj):
        self.obj = obj


    def replace_value(self, data):
        if data:
            # ������������
            data_type = type(data)
            # �ж���������
            if isinstance(data, dict) or isinstance(data, list):
                str_data = json.dumps(data)
            else:
                str_data = str(data)
            # �滻
            for cs in range(1, str_data.count('${') + 1):
                if "${" in str_data and "}" in str_data:
                    start_index = str_data.index("${")
                    end_index = str_data.index("}", start_index)
                    old_value = str_data[start_index:end_index + 1]
                    # ���䣺ͨ������Ķ���ͷ����������÷���
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
                    # ��������ȥ������
                    if isinstance(new_value, int) or isinstance(new_value, float):
                        str_data = str_data.replace('"' + old_value + '"', str(new_value))
                    else:
                        str_data = str_data.replace(old_value, str(new_value))
            # ��ԭ��������
            if isinstance(data, dict) or isinstance(data, list):
                data = json.loads(str_data)
            else:
                data = data_type(str_data)
        return data


    def send_request(self, name, method, url, **kwargs):
        try:
            logger.info("--------�ӿڲ��Կ�ʼ--------")
            # ����·��ƴ��
            url = self.replace_value(url)
            # ����ͷ�Ͳ����滻
            for key, value in kwargs.items():
                if key in ['params', 'data', 'json', 'headers']:
                    kwargs[key] = self.replace_value(value)
                    print(kwargs[key])
                elif key == "files":
                    for file_key, file_path in value.items():
                        value[file_key] = open(file_path, 'rb')
            # ������Ϣ��־
            logger.info("�������ƣ�%s" % name)
            logger.info("����ʽ��%s" % method)
            logger.info("����·����%s" % url)
            if "headers" in kwargs.keys():
                logger.info("����ͷ��%s" % kwargs["headers"])
            if "params" in kwargs.keys():
                logger.info("����params������%s" % kwargs["params"])
            elif "data" in kwargs.keys():
                logger.info("����data������%s" % kwargs["data"])
            elif "json" in kwargs.keys():
                logger.info("����json������%s" % kwargs["json"])
            if "files" in kwargs.keys():
                logger.info("����files������%s" % kwargs["files"])
            # ����
            rep = RequestsUtil.session.request(method, url, **kwargs)
            return rep
        except Exception as e:
            logger.error("��������send_request�쳣��%s" % str(traceback.format_exc()))

