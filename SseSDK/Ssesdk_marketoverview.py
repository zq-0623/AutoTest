# -*-coding:GBK -*-
import os
import time
from Ssesdk_tool import SseOptionQuote


def request_run():
    headers = {
        "token": "MitakeWeb",
        "symbol": "600000.sh",
        "param": "202308090930"
    }
    response = SseOptionQuote(url, headers=headers)
    res = response.text.replace("\x03", "").split("\x02")

    print(f"response_list1=====>'{response.text}'")
    print(f"response_list1=====>'{res}'")


if __name__ == '__main__':
    url = "http://114.80.155.61:22016/v3/m1"
    request_run()























