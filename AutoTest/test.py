# encoding=utf-8
import uuid

import paho.mqtt.client as mqtt
import zstd
from PyQt5.QtCore import QUrl


def on_connect(client, userdata, flags, rc):
    rc_status = ["连接成功", "协议版本不正确", "客户端标识符无效", "服务器不可用", "用户名或密码不正确", "未经授权"]
    print("connect：", rc_status[rc])


def on_message(client,userdata,msg):
    data_all = zstd.decompress(msg.payload).decode("utf-8")
    print(data_all)


def mqtt_connect():
    mqtt_min1 = mqtt.Client(str(uuid.uuid4()))
    # mqtt_min1.on_connect = on_connect
    mqtt_min1.on_message = on_message
    url = "tcp://114.80.155.61:22017"
    url_tcp = QUrl(url)
    mqtt_min1.connect(url_tcp.host(),url_tcp.port(),30)
    mqtt_min1.loop_start()
    return mqtt_min1


def on_subscribe():
    mqtt_min1 = mqtt_connect()
    mqtt_min1.subscribe("600000.sh",qos=1)
    while True:
        pass

on_subscribe()