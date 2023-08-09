# -*-coding:GBK -*-
import os
import time
from Ssesdk_tool import SseOptionQuote


def request_run():
    headers = {
        "token": "MitakeWeb"
    }
    response = SseOptionQuote(url, headers=headers)
    res = response.text.replace("\x03", "").split("\x02")
    for i in res:
        if i == '':
            res.remove('')
    print(f"response_list1=====>'{res}'")


if __name__ == '__main__':
    url = "http://114.80.155.61:22016/v1/marketoverview"
    request_run()























