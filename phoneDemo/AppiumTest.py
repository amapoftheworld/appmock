# -*-coding:utf8 -*-

import selenium
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from MyException import VerifyException
import time


# com.tencent.oscar.module.splash.SplashActivity
# com.tencent.oscar.module.main.MainActivity

def loginQQ(num,pwd):
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '5.1',
        'deviceName': 'm1note',
        'appPackage': 'com.tencent.mobileqq',
        'appActivity': 'com.tencent.mobileqq.activity.SplashActivity',
        'unicodeKeyboard': True,
        'resetKeyBoard': True
    }
    wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    WebDriverWait(wd, 60, 0.5).until(lambda driver: driver.find_element_by_id("com.tencent.mobileqq:id/btn_login"))
    # 点击登录
    wd.find_element_by_id('com.tencent.mobileqq:id/btn_login').click()
    # 输入登录
    # nameInput = wd.findElementByClassName("android.widget.EditText")[0]
    nameInput = wd.find_element_by_accessibility_id("请输入QQ号码或手机或邮箱")
    nameInput.click()
    nameInput.send_keys(num)
    wd.press_keycode(66)

    pwdInput = wd.find_element_by_id('com.tencent.mobileqq:id/password')
    pwdInput.click()
    pwdInput.send_keys(pwd)
    wd.press_keycode(66)

    wd.find_element_by_id('com.tencent.mobileqq:id/login').click()
    WebDriverWait(wd, 60, 0.5).until(lambda driver: wd.find_element_by_id('com.tencent.mobileqq:id/ivTitleName'))
    titleInfo = wd.find_element_by_id('com.tencent.mobileqq:id/ivTitleName')
    print(titleInfo.text)
    if titleInfo.text == u'绑定手机号码':
       wd.quit()
    else:
        raise VerifyException


def weishi():
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '5.1',
        'deviceName': 'm1note',
        # 'platformVersion': '6.0.1',
        # 'deviceName': 'angler',
        'appPackage': 'com.tencent.weishi',
        'appActivity': 'com.tencent.oscar.module.splash.SplashActivity',
        'unicodeKeyboard': True,
        'resetKeyBoard': True
    }
    wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    # wd.implicitly_wait(10)
    # 显示候选输入法
    a = wd.available_ime_engines
    print(a)
    # laoding页面
    WebDriverWait(wd, 60, 0.5).until(lambda driver: driver.find_element_by_id("com.tencent.weishi:id/splash_skip_btn"))
    if (wd.find_element_by_id('com.tencent.weishi:id/splash_skip_btn')):
        wd.find_element_by_id('com.tencent.weishi:id/splash_skip_btn').click()
    else:
        print('找不到对应控件')

    # 进入首页了
    WebDriverWait(wd, 60, 0.5).until(
        lambda driver: driver.find_element_by_id("com.tencent.weishi:id/profile_icon_text"))

    # 登录
    wd.find_element_by_id('com.tencent.weishi:id/profile_icon_text').click()
    # 出现QQ 或者登微信 btn_wechat_auth/btn_qq_auth
    WebDriverWait(wd, 60, 0.5).until(lambda driver: driver.find_element_by_id("com.tencent.weishi:id/btn_qq_auth"))
    wd.find_element_by_id('com.tencent.weishi:id/btn_qq_auth').click()

    WebDriverWait(wd, 60, 0.5).until(lambda driver: driver.find_element_by_class_name('android.widget.Button'))
    wd.find_element_by_class_name("android.widget.Button").click()

    # WebDriverWait(wd, 20, 0.5).until(lambda driver: driver.find_element_by_android_ui_automator("new UiSelector().text(\"搜索\")"))
    # wd.find_element_by_android_ui_automator("new UiSelector().text(\"搜索\")").click()
    # 发现-搜索页
    WebDriverWait(wd, 60, 0.5).until(
        lambda driver: driver.find_element_by_id('com.tencent.weishi:id/noname_base_search'))
    wd.find_element_by_id('com.tencent.weishi:id/noname_base_search').click()
    searchInput = wd.find_element_by_id('com.tencent.weishi:id/search_input')
    searchInput.click()
    searchInput.send_keys(u'150斤到90斤再到')
    wd.activate_ime_engine('com.sohu.inputmethod.sogou/.SogouIME')
    searchInput.click()
    wd.press_keycode(66)
    WebDriverWait(wd, 60, 0.5).until(lambda driver: wd.find_element_by_id("com.tencent.weishi:id/title"))
    titleResult = wd.find_element_by_id("com.tencent.weishi:id/title")
    content = titleResult.text
    if content == u'视频':
        print("存在视频")
        wd.find_element_by_id("com.tencent.weishi:id/cover").click()
        # 进入视频页面： 点击返回
        WebDriverWait(wd, 15, 1).until(lambda driver: wd.find_element_by_id("com.tencent.weishi:id/back"))
        wd.find_element_by_id("com.tencent.weishi:id/feed_like_status").click()
        wd.find_element_by_id("com.tencent.weishi:id/back").click()
    else:
        print("不存在视频")
    # count = 0
    # while count < 10000:
    #     count = count + 1
    #     titleResult = wd.find_element_by_id("com.tencent.weishi:id/title")
    #     content = titleResult.text
    #     if content == u'视频':
    #         print("存在视频")
    #         wd.find_element_by_id("com.tencent.weishi:id/cover").click()
    #         # 进入视频页面： 点击返回
    #         WebDriverWait(wd, 15, 1).until(lambda driver: wd.find_element_by_id("com.tencent.weishi:id/back"))
    #         wd.find_element_by_id("com.tencent.weishi:id/feed_like_status").click()
    #         wd.find_element_by_id("com.tencent.weishi:id/back").click()
    #
    #     else:
    #         print("不存在视频")

    # wd.keyevent(84)
    # wd.press_keycode(84)
    # wd.press_keycode(66)  # 发送keycode，功能：按键

    wd.quit()


def findElement(self, element):
    try:
        WebDriverWait(self.wd, 10).until(expected_conditions.presence_of_element_located((By.ID, element)))
        return True
    except selenium.common.exceptions.TimeoutException:
        return False
    except selenium.common.exceptions.NoSuchElementException:
        return False


def readQQ(path):
    desFile = open(path,"r")
    line=desFile.readline()
    codeArray =[]
    while line:
        strArray=line.split("----")
        num=strArray[0]
        pwd=strArray[1]
        dict = {}
        dict['num'] = num.replace(" ","")
        dict['pwd'] = pwd.replace("\r\n","")
        codeArray.append(dict)
        line = desFile.readline()
    return codeArray

if __name__ == '__main__':
    path = 'qq.txt'
    codeArray=readQQ(path)
    t = time.time()
    errCount = 0
    vqqList = []
    # t1 = time.time()
    # print (u"时间差1:%s", int(round(t1 * 1000)) - int(round(t * 1000)))  # 毫秒级时间戳
    for item in codeArray:
       num=item['num']
       pwd=item['pwd']
       try:
         loginQQ(num,pwd)
         weishi()
       except (VerifyException) :
           errCount=errCount+1
           vqqList.append(num)
           print('错误次数:%d',errCount)
    t2 = time.time()
    print ('时间差2:%d', int(round(t2 * 1000)) - int(round(t * 1000)))  # 毫秒级时间戳
