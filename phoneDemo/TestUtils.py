# coding: utf-8
import unittest
import selenium.common.exceptions
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class AppTest(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = 'angler'
        desired_caps['appPackage'] = 'com.tencent.weishi'
        desired_caps['appActivity'] = 'com.tencent.oscar.module.main.MainActivity'
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.wd.implicitly_wait(60)
        self.wd.find_element_by_id('cn.dxy.idxyer:id/start_up_welcome_enter_tv').click()

    # 向左滑动的函数
    def SwipeLeft(self, duration):
        x = self.wd.get_window_size()['width']
        y = self.wd.get_window_size()['height']
        self.wd.swipe(x * 9/10, y/2, x/10, y/2, duration)

    # 当元素找不到时
    def findElement(self, element):
        try:
            WebDriverWait(self.wd, 10).until(expected_conditions.presence_of_element_located((By.ID, element)))
            return True
        except selenium.common.exceptions.TimeoutException:
            return False
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def test_login(self):
        if self.findElement('cn.dxy.idxyer:id/start_up_welcome_image_iv'):
            for i in range(3):
                self.SwipeLeft(1000)
            self.wd.find_element_by_id('cn.dxy.idxyer:id/start_up_welcome_enter_tv').click()
        else:
            print('欢迎页不存在的')
        self.wd.implicitly_wait(60)
        self.wd.find_element_by_id('cn.dxy.idxyer:id/main_mine_rb').click()
        if self.findElement('cn.dxy.idxyer:id/tab_account'):
            self.wd.find_element_by_id('cn.dxy.idxyer:id/sso_username').set_value('1111111')
            self.wd.find_element_by_id('cn.dxy.idxyer:id/sso_password').set_value('1111111')
            self.wd.find_element_by_id('cn.dxy.idxyer:id/sso_login').click()
        else:
            print('用户已登录')

    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()
