# -*- coding: UTF-8 -*-
"""
@Project ：AutoTest
@File    ：mqtt_stress_test.py
@IDE     ：PyCharm
@Author  ：Qiang Zhao
@Date    ：2024/9/23 10:58
"""
import logging
import threading
import time

import paho.mqtt.client as mqtt
import zstd

# MQTT服务器地址与端口
MQTT_BROKER = "114.28.169.97"
MQTT_PORT = 22017

# 固定订阅的topic列表
subscription_topics = ["601099.sh"]
# subscription_topics = ["600157.sh","601162.sh","601398.sh","601288.sh","601099.sh","600550.sh","600383.sh","601668.sh","600010.sh","601989.sh","600030.sh","600611.sh","600048.sh","600187.sh","601138.sh","601988.sh","600839.sh","601818.sh","601328.sh","601929.sh",]
# subscription_topics = ["600157.sh","601162.sh","601398.sh","601288.sh","601099.sh","600550.sh","600383.sh","601668.sh","600010.sh","601989.sh","600030.sh","600611.sh","600048.sh","600187.sh","601138.sh","601988.sh","600839.sh","601818.sh","601328.sh","601929.sh","002607.sz", "000750.sz", "300059.sz", "000158.sz", "002717.sz", "002583.sz", "000617.sz", "002640.sz", "000981.sz", "000560.sz", "000793.sz", "300072.sz", "000069.sz", "000002.sz", "000627.sz", "300180.sz", "002423.sz", "002936.sz", "000932.sz", "000725.sz","839719.bz","920099.bz","834021.bz","830799.bz","430198.bz","832023.bz","832149.bz","839946.bz","833171.bz","837592.bz"]

# 控制参数
num_clients = 10000  # 客户端数量
max_connections_per_client = 2  # 每个客户端允许的最大连接数

# 日志配置
logging.basicConfig(filename='mqtt_stress_test.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


# 用于生成唯一的client ID
def generate_client_id(index):
    return f"Ceshizhao{index:03d}"


# 锁对象用于控制日志写入顺序
log_lock = threading.Lock()


# 当客户端连接到服务器时回调
def on_connect(client, userdata, flags, rc):
    with log_lock:
        if rc == 0:
            logging.info(f"客户端 {client._client_id.decode()} 成功连接到服务器。")
            client.subscribe([(topic, 0) for topic in subscription_topics])
            logging.info(f"客户端 {client._client_id.decode()} 成功订阅主题: {subscription_topics}")
        else:
            error_messages = {
                1: "不可接受的协议版本",
                2: "由于达到最大连接限制被拒绝",
                3: "服务器不可用",
                4: "不允许的用户名或密码",
                5: "未授权"
            }
            error_message = error_messages.get(rc, "未知错误")
            logging.error(f"客户端 {client._client_id.decode()} 连接失败，错误码: {rc} - {error_message}")


# 当收到消息时回调
def on_message(client, userdata, message):
    with log_lock:
        try:
            msg_content = zstd.decompress(message.payload).decode('utf-8')
            logging.info(f"客户端 {client._client_id.decode()} 收到消息，主题: {message.topic}, 内容: {msg_content}")
        except Exception as e:
            logging.error(f"客户端 {client._client_id.decode()} 解压消息时出错: {e}")


# MQTT客户端线程函数
def mqtt_client_thread(client_id):
    client = mqtt.Client(client_id=client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    retries = 0
    max_retries = 3  # 设置最大重试次数

    while retries < max_retries:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)  # 连接时设置60秒超时
            break  # 连接成功后退出循环
        except TimeoutError:
            retries += 1
            logging.error(f"客户端 {client_id} 连接超时，重试次数: {retries}")
            time.sleep(2)  # 等待2秒后再次尝试连接

    if retries == max_retries:
        logging.error(f"客户端 {client_id} 无法连接到服务器，已达到最大重试次数。")
        return

    client.loop_start()

    try:
        while True:
            time.sleep(1)
    except Exception as e:
        logging.error(f"客户端 {client_id} 遇到错误: {e}")
    finally:
        client.loop_stop()


# 启动多线程MQTT客户端
def run_mqtt_test(num_clients, max_connections):
    threads = []
    for i in range(1, num_clients + 1):
        client_id = generate_client_id(i)

        # 每个client_id建立指定数量的连接
        for j in range(max_connections):
            thread = threading.Thread(target=mqtt_client_thread, args=(client_id,))
            threads.append(thread)
            thread.start()

            # 在每个客户端连接之间增加短暂延迟，避免服务器过载
            time.sleep(1)  # 每个连接之间间隔 1000 毫秒

        # 限流：每500个线程启动后等待一段时间
        if i % 500 == 0:
            time.sleep(30)  # 等待30秒

    for thread in threads:
        thread.join()


# 调用函数进行测试
if __name__ == "__main__":
    run_mqtt_test(num_clients, max_connections_per_client)
