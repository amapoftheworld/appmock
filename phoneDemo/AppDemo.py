# coding: utf-8
from __future__ import division
import time
import atx
import uiautomator2 as u2


#com.tencent.mobileqq   .activity.LoginActivity

def initPhone():
    # c = atx.adb_client
    # print(c.version())  # adb version
    # deviceList = c.devices()
    # print(deviceList)

    d = u2.connect('ENU7N15C29001675')  # alias for u2.connect_wifi('10.0.0.1')
    # print(d.info)

    # d.app_start('com.tencent.mobileqq')  # start with package name
    # print(d.current_app())
    # enterActivity,pid,package_name = d.current_app()
    # d.app_start('com.tencent.weishi')  # start with package name

    # screenWith,screenHeight=d.window_size()
    xml = d.dump_hierarchy()
    print(xml)

    # d.swipe(1306,2329,1362,2362)
    #播放
    #d.click(screenWith/2,screenHeight/2)
    # d(text="我的").click()
    # widthQ=1247/screenWith
    # heightQ=84/screenHeight
    #进入搜索页
    # d.click(widthQ,heightQ)
    # xml = d.dump_hierarchy()
    # widthQ=116/screenWith
    # heightQ=334/screenHeight
    # d.click(widthQ,widthQ)
    # d(text="搜索用户 / 话题 / 视频").set_text("足球")  # set the text
    #
    # xml = d.dump_hierarchy()
    # print(xml)
    #
    #
    # d(className="android.support.v7.widget.RecyclerView", resourceId="android:id/search_with_words_list") \
    #     .child_by_text("Bluetooth", className="android.widget.LinearLayout")
    # d.press("enter")  # press the back key, with key name

    # d.find_elements_by_id("com.boohee.secret:id/search_input").__getitem__(1)

    # d(className="android.widget.EditText", resourceId="android:id/search_input").set_text("dssdsd")

if __name__ == '__main__':
    initPhone()
