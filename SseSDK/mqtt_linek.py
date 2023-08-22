import os

import paho.mqtt.client as mqtt
import zstd


def on_message_min1(client,userdata,msg):
    pass


host = "114.80.155.61"
port = 9009
topic_list = ["600050.sh","000002.sz"]
client_min1 = mqtt.Client("min1K")
client_min1.on_message = on_message_min1
client_min1.connect(host, port, 60)
for topic in topic_list:
    client_min1.subscribe(topic)

client_min1.loop_start()









