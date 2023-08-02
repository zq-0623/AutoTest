# -*-coding:UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class WebTest:

    def __init__(self):
        # 初始化一个chrome浏览器(驱动谷歌浏览器时，直接使用webdriver.Chrome()可能会报错，建议使用一下方法)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.drive = webdriver.Chrome(options=options)
        # 最大化窗口
        self.drive.maximize_window()
        # 隐式等待,设置最大的等待时长,只对查找元素(find_elementXXX)生效
        self.drive.implicitly_wait(2)

    def log_on(self):
        '''代码执行'''
        # 通过get()方法打开网页
        self.drive.get('http://www.baidu.com')

        # 输入内容，点击百度一下
        self.drive.find_element(By.ID, 'kw').send_keys("软件测试")
        # 回车操作(相当于按回车键)：submit()
        self.drive.find_element(By.CSS_SELECTOR, '[id="su"]').submit()
        # self.drive.find_element(By.ID)
        # self.drive.find_element(By.CSS_SELECTOR, '[aria-label="软件测试技术，软件开发流程，百度百科"]').submit()

    def sign_out(self):
        '''退出浏览器'''
        self.drive.close()  # 关闭浏览器
        self.drive.quit()  # 关闭浏览器并且关闭驱动


if __name__ == "__main__":
    run = WebTest()
    run.log_on()
    # run.sign_out()
