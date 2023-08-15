import os


def get_mqtt_file_paths(mqtt_folder):
    file_paths_mqtt = []

    for folder, _, files in os.walk(mqtt_folder):
        for file in files:
            file_path = os.path.join(folder, file)
            file_paths_mqtt.append(file_path)
    return file_paths_mqtt

def get_http_file_paths(http_folder):
    file_paths_http = []
    for folder, _, files in os.walk(http_folder):
        for file in files:
            file_path = os.path.join(folder, file)
            file_paths_http.append(file_path)

    return file_paths_http


mqtt_file_path = r'C:/Users/Administrator/Desktop/mqtt_kline_data'
http_file_path = r'C:/Users/Administrator/Desktop/http_kline_data'

file_paths_mqtt = get_mqtt_file_paths(mqtt_file_path)
file_paths_http = get_mqtt_file_paths(http_file_path)

file_pairs = [
    (mqtt_file_path, http_file_path, 'r均价(a)', '均价'),
    (mqtt_file_path, http_file_path, 'r最高价(h)', '高'),
    (mqtt_file_path, http_file_path, 'r最低价(l)', '低'),
    (mqtt_file_path, http_file_path, 'r成交额(m)', '成交额'),
    (mqtt_file_path, http_file_path, 'r开盘价(o)', '开'),
    (mqtt_file_path, http_file_path, 'r参考价(r)', '参考价'),
    (mqtt_file_path, http_file_path, 'r时间(t)', '日期时间'),
    (mqtt_file_path, http_file_path, 'r成交量(v)', '量'),
    (mqtt_file_path, http_file_path, 'r最新价(ic)', '基金净值'),
]


def mqtt_file_name():
    print("File paths:")
    for path1 in file_paths_mqtt:
        pass
    return path1
def http_file_name():
    for path in file_paths_http:
        pass
    return path

print("\nFile pairs:")
# for mqtt_path, http_path, mqtt_col, http_col in file_pairs:
#     print(f"MQTT path: {mqtt_path}, HTTP path: {http_path}, MQTT column: {mqtt_col}, HTTP column: {http_col}")
print(mqtt_file_name())
print(http_file_name())
