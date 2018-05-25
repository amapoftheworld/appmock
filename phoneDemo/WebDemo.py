# *_*coding:utf-8 *_*
from selenium import webdriver
import time
import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver = "/Applications/Google Chrome.app/Contents/MacOS/chromedriver"


def initAction(desUrl):
    t = time.time()
    browser = webdriver.Chrome(chromedriver)
    browser.get(desUrl)
    # elem = browser.find_element_by_tag_name('body')  # Find the search box
    # WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, "btn-play")))
    frameVar = browser.find_element_by_tag_name('iframe')
    browser.switch_to.frame(frameVar)
    elem = browser.find_element_by_class_name("btn-play")
    # elem = browser.find_element_by_css_selector("btn-play")
    print(elem)
    elem.click()

    # [1].click()  # 点击播放
    print(elem)
    t1 = time.time()
    print ("时间差:%s", int(round(t1 * 1000)) - int(round(t * 1000)))  # 毫秒级时间戳
    time.sleep(5)
    browser.quit()


if __name__ == '__main__':
    url = 'https://h5.qzone.qq.com/weishi/feed/IuJWmBBTPG6uOko6/wsfeed?_proxy=1&_wv=1&id=IuJWmBBTPG6uOko6'
    count = 0
    while count < 10000:
        count = count + 1
        initAction(url)
