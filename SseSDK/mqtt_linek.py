import paho.mqtt.client as mqtt
import zstd


def on_message_min1(client,userdata,msg):
    pass


client_min1 = mqtt.Client("min1K")
client_min1.on_message = on_message_min1
client_min1.connect("tcp://114.80.155.61", "9009", 60)




