# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt

# MQTT broker 地址和端口
broker_address = "114.28.169.97"
broker_port = 22017

# 要订阅的主题列表
topics = ["000001.sh", "00002.sh", "399001.sz"]


# 定义当客户端连接到服务器时的回调函数
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 在连接成功后订阅主题
    for topic in topics:
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")


# 定义收到消息时的回调函数
def on_message(client, userdata, msg):
    print(f"Message received from topic {msg.topic}: {msg.payload.decode()}")


# 创建 MQTT 客户端实例
client = mqtt.Client()

# 绑定回调函数
client.on_connect = on_connect
client.on_message = on_message

# 连接到 MQTT broker
client.connect(broker_address, broker_port, 60)

# # 开始阻塞式循环，等待消息
client.loop_forever()
