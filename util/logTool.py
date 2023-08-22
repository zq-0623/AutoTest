# -*- coding: utf-8 -*-
import logging
import time,os

import colorlog as colorlog

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# print(time.strftime("%y%m%d%H%M%S"))

# 创建日志文件路径
LOG_PATH = os.path.join(BASE_PATH,"log")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class Logger():
    def __init__(self):
        # 创建以年月日为日志文件名
        self.logname = os.path.join(LOG_PATH, "{}_{}.log".format(time.strftime("%y%m%d"),"mqtt_kline"))

        log_colors_config = {
            'DEBUG': 'fg_thin_cyan',  # cyan white
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        # 创建日志对象
        self.logger = logging.getLogger()
        # 设置日志显示级别
        self.logger.setLevel(logging.DEBUG)

        # 添加控制台，用于输出日志到控制台
        self.console_handler = logging.StreamHandler()
        # 设置控制台输出日志级别
        self.console_handler.setLevel(logging.DEBUG)

        # 添加日志文件，用于输出日志文件
        self.file_handler = logging.FileHandler(self.logname, mode="a", encoding="utf-8")
        # 设置文件输出日志级别
        self.file_handler.setLevel(logging.DEBUG)

        # 将handler添加至日志器中
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)

        # 自定义日志显示格式
        self.file_formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S'
        )
        self.console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=log_colors_config
        )

        # 将自定义日志格式赋予日志器handler
        self.console_handler.setFormatter(self.console_formatter)
        self.file_handler.setFormatter(self.file_formatter)


logger = Logger().logger


# logger.debug("==========调试信息==========")
# logger.info("==========调试信息==========")
# logger.warning("==========调试信息==========")
# logger.error("==========调试信息==========")
# logger.critical("==========调试信息==========")
