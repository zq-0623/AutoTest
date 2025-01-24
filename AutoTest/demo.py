import requests
import yaml


# 读取 YAML 文件获取字段名称（只提取每一行的第一个字段）
def load_yaml_data(yaml_file):
    with open(yaml_file, 'r', encoding='gbk') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    # 确保数据是列表类型，且每个元素是字典
    if isinstance(data, list):
        # 提取每个字典的键作为字段名
        field_names = [list(item.keys())[0] for item in data if isinstance(item, dict)]
        return field_names
    else:
        print("YAML 数据格式错误，期望列表字典格式")
        return []


# 定义请求头
headers = {
    'token': 'MitakeWeb',
    'symbol': '000001.sh',
    'Param': '1,13|1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71'
}

# 获取 YAML 文件中的字段名称
yaml_file = '../AutoTest/Sse_Auto_script/2024Q4/AddValue.yaml'  # 请替换为实际 YAML 文件路径
field_names = load_yaml_data(yaml_file)

# 如果没有提取到任何字段，输出错误并退出
if not field_names:
    print("未找到字段，无法继续操作")
    exit()

# 请求接口1
url1 = 'http://114.28.169.97:22016/v3/quote'
try:
    response1 = requests.get(url1, headers=headers)
    processed_data1 = {}
    resp_list = response1.text.split("\x03")
    if resp_list[-1] == '':
        resp_list.remove('')
    for m in range(len(resp_list)):
        split_list = resp_list[m].split("\x02")
        for n, field_name in zip(split_list, field_names):
            if "\x01" in n:
                processed_data1[field_name] = n.split("\x01")
            else:
                processed_data1[field_name] = [n]  # 存储当前数据
    # print("url1 响应内容：", processed_data1)  # 打印响应内容，检查是否为有效的JSON
except requests.exceptions.JSONDecodeError as e:
    print(f"URL1 返回的数据不是有效的JSON格式：{e}")
    processed_data1 = None

# 请求接口2
url2 = 'http://103.251.85.148:22016/v3/quote'
try:
    response2 = requests.get(url2, headers=headers)
    processed_data2 = {}
    resp_list = response2.text.split("\x03")
    if resp_list[-1] == '':
        resp_list.remove('')
    for m in range(len(resp_list)):
        split_list = resp_list[m].split("\x02")
        for n, field_name in zip(split_list, field_names):
            if "\x01" in n:
                processed_data2[field_name] = n.split("\x01")
            else:
                processed_data2[field_name] = [n]  # 存储当前数据
    # print("url2 响应内容：", processed_data2)  # 打印响应内容，检查是否为有效的JSON
except requests.exceptions.JSONDecodeError as e:
    print(f"URL2 返回的数据不是有效的JSON格式：{e}")
    processed_data2 = None

# 比较 processed_data1 和 processed_data2 的一致性
if processed_data1 and processed_data2:
    # 找出不一致的字段
    discrepancies = {}
    for field_name in processed_data1:
        if processed_data1.get(field_name) != processed_data2.get(field_name):
            discrepancies[field_name] = {
                'url1_value': processed_data1.get(field_name),
                'url2_value': processed_data2.get(field_name)
            }
    
    if discrepancies:
        print("接口返回数据不一致的字段：")
        for field_name, values in discrepancies.items():
            print(f"字段: {field_name}")
            print(f"  url1 值: {values['url1_value']}")
            print(f"  url2 值: {values['url2_value']}")
    else:
        print("两个接口的返回数据一致")
else:
    print("一个或两个接口的响应数据无效，无法比较")
