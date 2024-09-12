import time

import paho.mqtt.client as mqtt

# MQTT server information
broker_addresses = [
    "cshkapmqtt1.sj688.cn",
    "cshkapmqtt2.sj688.cn",
    "cshkapmqtt3.sj688.cn",
]
ports = [22017, 22017, 22017]
client_ids = ["ceshi01", "ceshi02", "ceshi03"]


# Callback functions for logging
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # print(f"Connected successfully to {client._host}:{client._port} with client ID {client._client_id}")
        print(
            u"Connected successfully to {}:{} with client ID {}".format(client._host, client._port, client._client_id))
    else:
        # print(f"Failed to connect, return code {rc}")
        print(u"Failed to connect, return code {}".format(rc))


def on_disconnect(client, userdata, rc):
    # print(f"Disconnected from {client._host}:{client._port} with client ID {client._client_id}")
    print(u"Disconnected from {}:{} with client ID {}".format(client._host, client._port, client._client_id))


# Function to create and start a client
def start_client(broker_address, port, client_id):
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    # Connect to the broker
    client.connect(broker_address, port)
    client.loop_start()  # Start the loop in a non-blocking way

    return client


# Start clients sequentially with a 3-second delay
clients = []
for i in range(3):
    client = start_client(broker_addresses[i], ports[i], client_ids[i])
    clients.append(client)
    if i < 2:
        time.sleep(3)

time.sleep(5)
clients[0].disconnect()  # Disconnect the first client

# Continue running the other clients
for client in clients[1:]:
    client.loop_forever()

# Wait for all threads to finish
for client in clients:
    client.loop_stop()
    client.disconnect()
