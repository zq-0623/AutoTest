# from decimal import Decimal, ROUND_HALF_UP
#
# value = Decimal(-0.061650)
# B = (Decimal(value) * Decimal(100)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
# print(B)
#
# C = round(value, 2)
# print(C)

# from util.base93 import decode
#
# with open("./TestFile/test.txt", "r", encoding='utf-8') as file:
#     files = file.readlines()
#     for i in files:
#         if i:
#             data_str = i.split('\x03')
#             for j in data_str:
#                 te_str = j.split('\x02')
#                 # print(te_str)
#                 if j:
#                     new_list = te_str[:]
#                     new_list[2] = decode(te_str[2])
#                     new_list[3] = decode(te_str[3])
#                 # print(new_list[2])  # 总股本
#                 print(new_list[3])  # 流通股本


import redis
import requests

# 设置接口地址和 Redis 连接
url = "http://114.28.169.157:22017/v1/ahquote"
redis_host = 'localhost'
redis_port = 6379
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def fetch_and_process_data():
    try:
        # 请求接口数据
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.content.decode('utf-8')  # 将返回数据解码为字符串

        # 以"\x03"分割数据
        split_data = data.split("\x03")
        field_values = []

        # 遍历分割后的数据，再以"\x02"分割并提取第二个字段
        for item in split_data:
            parts = item.split("\x02")
            if len(parts) > 1:
                field_values.append(parts[1])

        # 遍历字段列表，将每个值按"."分割，并用分割后的第二个部分进行Redis查询
        for value in field_values:
            dot_split = value.split(".")
            if len(dot_split) > 1:
                first_part = dot_split[0]
                second_part = dot_split[1]
                # 从 Redis 获取与 second_part 相关的值
                redis_value = r.get(second_part)
                if redis_value:
                    # 拼接成新的 redis_key.redis_value.first_part 形式
                    redis_key = f"{second_part}.{redis_value}.{first_part}"
                    A_rate = r.get("hk.cr.CNY")
                    H_rate = r.get("hk.cr.HKD")
                    print(A_rate,H_rate)
                    print(f"Constructed Redis Key: {redis_key}")
                else:
                    print(f"Redis key '{second_part}' not found in Redis.")
            else:
                print(f"Invalid value (no '.'): {value}")

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    except redis.RedisError as e:
        print(f"Redis error: {e}")

# 调用函数
fetch_and_process_data()

