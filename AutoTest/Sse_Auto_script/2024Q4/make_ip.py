"""
# -*- coding: UTF-8 -*-
@Project ：AutoTest 
@File    ：make_ip.py
@IDE     ：PyCharm 
@Author  ：ZhaoQiang
@Date    ：2024/11/20 星期三 14:37

"""
import random
def generate_ipv4():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


# 生成一个随机IPv6地址
def generate_ipv6():
    return ":".join(f"{random.randint(0, 65535):x}" for _ in range(8))


# 生成境内IP（中国）与境外IP的一个简单分类
def generate_ip():
    ip_type = random.choice(["domestic", "overseas"])  # 随机选择境内或境外IP
    if ip_type == "domestic":  # 境内IP（示例：使用常见的私有IP范围）
        ipv4 = generate_ipv4()  # 生成IPv4地址
        ipv6 = generate_ipv6()  # 生成IPv6地址
    else:  # 境外IP（示例：随机生成全球范围的IP）
        ipv4 = generate_ipv4()  # 生成IPv4地址
        ipv6 = generate_ipv6()  # 生成IPv6地址
    return ipv4, ipv6


# 保存到文件
def save_to_file(filename, n):
    with open(filename, "w") as file:
        for _ in range(n):
            ipv4, ipv6 = generate_ip()
            file.write(f"{ipv4} | {ipv6}\n")


# 生成10000个IP地址
save_to_file("../../TestFile/ip_addresses.txt", 10000)

print("IP地址已生成并保存到 'ip_addresses.txt'")
