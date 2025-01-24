import json
import os

import yaml

from util.logTool import logger


def get_object_path():
    # print(os.path.abspath(os.getcwd()))
    return os.path.abspath(os.getcwd())


def read_testcase_yaml(yaml_path):
    with open(str(get_object_path()) + yaml_path ,'r',encoding='utf-8') as f:
        caseinfo = yaml.load(stream=f,Loader=yaml.FullLoader)
        logger.info(caseinfo)
        # 单纯复制修改参数的模式
        if len(caseinfo) >= 2:
            return caseinfo
        else:  # 有数据驱动的场合
            if "parameterize" in dict(*caseinfo).keys():
                new_caseinfo = ddt(*caseinfo)
                return new_caseinfo
            else:
                return caseinfo


def ddt(caseinfo):
    if "parameterize" in caseinfo.keys():
        caseinfo_str =json.load(caseinfo)
        for parma_key,parma_value in caseinfo_str.items():
            logger.info(parma_key)
            logger.info(parma_value)


yaml_path = "./sentences.yaml"
read_testcase_yaml(yaml_path)
