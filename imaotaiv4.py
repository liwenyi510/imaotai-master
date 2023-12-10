# coding:utf-8
__author__ = 'wenyi.li'
import time

import requests
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
'''
description:driver配置
'''
class Driver_configure():
    def __init__(self):
        '''获取driver'''
        try:
            self.caps = {}
            self.caps["platformName"] = "Android"
            self.caps["appium:unicodeKeyboard"] = True
            self.caps["appium:noReset"] = True
            self.caps["appium:newCommandTimeout"] = 6000
            self.caps["appium:deviceName"] = "8BN0217617010356"
            self.caps["appium:ensureWebviewsHavePages"] = True
            self.caps["appium:nativeWebScreenshot"] = True
            self.caps["appium:connectHardwareKeyboard"] = True
            self.caps["appPackage"] = "com.moutai.mall"
            self.caps['appActivity'] = "com.moutai.mall.MainActivity"
            self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",self.caps)
            print("init已经执行")
        except Exception as e :
            SendMessage().sendmsg("创建driver出错：{}".format(e))
            raise e
    # 生肖茅台申购
    def sxmt_apply(self):
        my_driver = self.driver
        print("创建driver")
        if my_driver.is_locked():
            my_weid().swipe_down(my_driver)
            print("滑动解锁")
        my_driver.implicitly_wait(10)

        my_driver.wait_activity("com.moutai.mall.MainActivity", 10)



        my_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("i购").resourceId("com.moutai.mall:id/tab_name")').click()
        my_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                               'new UiSelector().text("享约申购")').click()
        name = my_driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.Button")
        end_test = ["本场申购已结束", "申购结果公示"]
        time.sleep(5)
        if name.text in end_test:
            my_driver.lock()
            print("超过申购时间段，执行结束！")
            SendMessage().sendmsg("申购时间段为9：00~10：00，已超过申购时间段，程序执行结束！")
        else:
            num_list = [1, 2,3,4]
            for i in num_list:

                try:
                    my_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("预约申购")').click()

                    time.sleep(2)
                    shengoucode = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout[2]/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[2]/android.widget.Button"
                    my_driver.find_element(AppiumBy.XPATH, shengoucode).click()

                    print("开始点击申购")
                    time.sleep(2)
                    qdsgcode = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.Button"
                    my_driver.find_element(AppiumBy.XPATH, qdsgcode).click()

                    print("确认申购")
                    time.sleep(2)
                    my_driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                           value='new UiSelector().text("继续申购").index(0)').click()

                    print("第{}次点击。 ".format(i))
                    SendMessage().sendmsg("end:{}".format(i))
                    time.sleep(2)
                    code = 'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("预约申购"))'
                    my_driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value=code)
                    print("滚动查找元素")
                except Exception as e:
                    print(e)
                    SendMessage().sendmsg("告警：" + str(e))
            my_driver.lock()

            print("软件执行完毕！")


'''
description:手势操作
'''
class my_weid:
    def swipe_left(self,driver):
        '''左滑'''
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        driver.swipe(x*3/4,y/4,x/4,y/4)

    def swipe_right(self,driver):
        '''右滑'''
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        driver.swipe(x/4,y/4,x*3/4,y/4)

    def swipe_down(self,driver):
        '''下滑'''
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        driver.swipe(x/2,y*3/4,x/2,y/2)

    def swipe_up(self,driver):
        '''上滑'''
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        driver.swipe(x/2,y/4,x/2,y*3/4)

"""发送消息"""
class SendMessage():
    def __init__(self):
        self.webhook='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a99f29cf-60ab-43fa-9828-4991756c16d8'

    def sendmsg(self,msg):
        """
        发送文本消息
        """
        url = self.webhook
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        data_text={
            "msgtype": "text",
            "text": {
                "content": msg

            }
        }
        res = requests.post(url=url, headers=headers, json=data_text)

def run():

    Driver_configure().sxmt_apply()


if __name__ == '__main__':
    run()


