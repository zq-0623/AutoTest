# encoding=utf-8
import json
import re

import yaml
from PyQt5.QtCore import QUrl
import paho.mqtt.client as mqtt
from util.logTool import logger
from util.base93 import decode
import zstd

data = []
yaml_path = "../testCase/quote/mqtt_lineK.yaml"


def on_message_min1(client, userdata, msg):
    try:
        dataMapList = []
        seen_sb = set()
        unique_data = []
        data_all = zstd.decompress(msg.payload).decode('utf8')
        dataMap = {}
        for d in str(data_all).split("\x02"):
            ds = d.split('=')
            if len(ds) >= 2:
                dataMap[ds[0]] = ds[1]
        code = dataMap.get("1")
        subtype = dataMap.get("6")
        sb = dataMap.get("sb")
        h5 = json.loads(dataMap.get("h5").strip())
        # h15 = json.loads(dataMap.get("h15"))
        # h30 = json.loads(dataMap.get("h30"))
        # h60 = json.loads(dataMap.get("h60"))
        # h120 = json.loads(dataMap.get("h120"))
        # r5 = json.loads(dataMap.get("r5"))
        # r15 = json.loads(dataMap.get("r15"))
        # r30 = json.loads(dataMap.get("r30"))
        # r60 = json.loads(dataMap.get("r60"))
        # r120 = json.loads(dataMap.get("r120"))

        # print(dataMap)
        print(code)
        print(subtype)
        print(sb)
        # print("h5333333=====>", h5)
        print("h5=====>", h5)
        # print("h15=====>",decode_quote(h15))
        # print("h30=====>",decode_quote(h30))
        # print("h60=====>",decode_quote(h30))
        # print("h120=====>",decode_quote(h120))
        # print("r5=====>",decode_quote(r5))
        # print("r15=====>",decode_quote(r15))
        # print("r30=====>",decode_quote(r30))
        # print("r60=====>",decode_quote(r60))
        # print("r120=====>",decode_quote(r60))
        dataMapList.append(dataMap)
        for data in dataMapList:
            sb = data.get("sb")
            if sb not in seen_sb:
                unique_data.append(data)
        # logger.debug(unique_data)
        # logger.debug(dataMap)
        # logger.debug(sb)
    except Exception as e:
        logger.error(e)


def mqtt_connect():
    mqtt_min1_client = mqtt.Client("MQTT_MIN1")
    # mqtt_min1_client.on_connect = on_connect
    mqtt_min1_client.on_message = on_message_min1
    url = "tcp://114.80.155.61:22017"
    url_tcp = QUrl(url)
    mqtt_min1_client.connect(url_tcp.host(), url_tcp.port(), 60)
    mqtt_min1_client.loop_start()
    return mqtt_min1_client


def on_subscribe():
    mqtt_min1_client = mqtt_connect()
    mqtt_min1_client.subscribe("600000.sh_o", qos=0)


def quote_yaml(path):
    with open(path, 'r', encoding='gbk') as fp:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        return yaml.safe_load(fp)


def decode_quote(msg):
    res_list = [msg.get('a'), msg.get('c'), msg.get('ot'), msg.get('h'), msg.get('i'), msg.get('l'), msg.get('m'),
                msg.get('o'), msg.get('dt'), msg.get('r'), msg.get('t'), msg.get('v'), msg.get('r'), msg.get('ic')]
    for i in range(len(res_list)):
        data_values = list(data[i].values())[0]
        if data_values == 'Y':
            res_list[i] = decode(res_list[i])
    return res_list


while True:
    try:
        on_subscribe()
    except Exception as e:
        pass
# for i in range(1,5):
#     if i <5:
#         on_subscribe()