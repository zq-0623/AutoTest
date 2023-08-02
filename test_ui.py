# 导入webdriver
import time
from encodings import undefined

import pytest
from appium import webdriver
# 初始化参数
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


@pytest.mark.ui
class TestDemo:

    def setup(self):
        desired_caps = {
            "platformName": "Android",
            "appium:platformVersion": "12",
            "appium:deviceName": "xiaomi",
            "appium:appPackage": "com.chi.ssetest",
            "appium:appActivity": "com.cvicse.stock.SplashActivity",
            "appium:unicodeKeyboard": False,
            "appium:resetKeyboard": True,
            "appium:noReset": True,
            "appium:newCommandTimeout": 6000,
            "appium:automationName": "UiAutomator2"
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        # 连接Appium Server，初始化自动化环境
        time.sleep(1)
        el1 = self.driver.find_element(by=AppiumBy.XPATH,
                                       value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.TextView")
        el1.click()
        time.sleep(1)
        el2 = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                       value='new UiSelector().text("浦发银行")')
        el2.click()
        time.sleep(4)

    def test_assert1(self):
        pytest.assume(self.driver.find_element(by=AppiumBy.ID, value="com.chi.ssetest:id/tev_lastPrice").text == "7.2f")
        pytest.assume(self.driver.find_element(by=AppiumBy.ID, value="com.chi.ssetest:id/tev_change").text == "-0.01")
        pytest.assume(self.driver.find_element(by=AppiumBy.ID, value="com.chi.ssetest:id/tev_max_high").text == "7.26")
        # print(self.driver.find_element(by=AppiumBy.ID, value="com.chi.ssetest:id/tev_lastPrice").text)
        pytest.assume(
            self.driver.find_element(by=AppiumBy.ID, value="com.chi.ssetest:id/tev_changeRate").text == "-0.14%")


    # def test_assert2(self):
    #     assert self.driver.find_element(by=AppiumBy.ID, value="com.chi.ssetest:id/tev_change").text == "-0.02"
    #
    # def test_assert3(self):
    #     assert self.driver.find_element(by=AppiumBy.ID, value="com.chi.ssetest:id/tev_max_high").text == "7.23"

    # def teardown(self):
    #     self.driver.quit()
