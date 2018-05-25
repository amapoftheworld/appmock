# coding:utf-8


import os
import re
import time
import tempfile
import xml.etree.cElementTree as ET
from AndroidKeyEvent import Keycode


class Utils(object):
    """docstring for Utils"""

    def __init__(self):
        super(Utils, self).__init__()

    def find_devices(self):
        rst = os.popen('adb devices').read()
        devices = re.findall(r'(.*?)\s+device', rst)
        if len(devices) > 1:
            return devices[1:]
        else:
            # raise Exception('DeviceNotFound')
            return []

class Device(object):
    # 元素内部类
    class Element(object):
        """docstring for Element"""

        def __init__(self, x, y, device_id):
            self.x = str(int(x))
            self.y = str(int(y))
            self.device_id = device_id

        def click(self):
            Device(self.device_id).click(self.x, self.y)

        def input(self, text):
            self.click()
            Device(self.device_id).input_text(text)

    # 设备未找到异常类
    class DeviceNotFoundException(Exception):
        def __init__(self, err='设备未找到' ):
            Exception.__init__(self, err)

    # 元素未找到异常类
    class ElementNotFoundException(Exception):
        def __init__(self, err='未找到此元素'):
            Exception.__init__(self, err)

    # activity未找到异常类
    class ActivityNotFoundException(Exception):
        def __init__(self, err='未找到此activity'):
            Exception.__init__(self, err)

    # 设备初始化方法

    def __init__(self, device_id):

        super(Device, self).__init__()

        self.device_id = device_id
        devices = re.findall(r'(.*?)\s+device', os.popen('adb devices').read())[1:]

        # print devices
        if device_id not in devices:
            self.DeviceNotFoundException()

        self.tempFile = tempfile.gettempdir()
        self.pattern = re.compile(r"\d+")
        # 安装unicode输入法并激活
        # self.install_app(os.getcwd() + '/bin/apk/MobInput.apk')
        # self.shell_cmd('ime enable org.mobtest.input/.InputService')
        # self.shell_cmd('ime set org.mobtest.input/.InputService')

    # 辅助类
    def get_abi(self):
        return self.shell_cmd('getprop ro.product.cpu.abi').strip()

    def get_sdk(self):
        return self.shell_cmd('getprop ro.build.version.sdk').strip()

    def shell_cmd(self, cmd):
        return os.popen('adb -s ' + str(self.device_id) + ' shell ' + cmd).read()

    def push_file(self, local_path, remote_path):
        os.popen('adb -s ' + str(self.device_id) + ' push ' + local_path + ' ' + remote_path)

    def pull_file(self, local_path, remote_path):
        os.popen('adb -s ' + str(self.device_id) + ' pull ' + local_path + ' ' + remote_path)

    def check_root(self):
        os.popen('adb -s ' + self.device_id + ' root')
        ret = os.popen('adb -s ' + self.device_id + ' remount').read().strip()
        if 'remount succeeded' in ret:
            return True
        else:
            return False

    # 截图方法先获取系统tmp目录全路径
    tempDir = tempfile.gettempdir()

    def save_screenshot(self, save_path=tempDir):
        self.shell_cmd('screencap /sdcard/sc.png')
        self.pull_file('/sdcard/sc.png', save_path)

    # device methods
    def get_screensize(self):
        temp = self.shell_cmd('wm size').split(':')[1].strip()
        return {'width': int(temp.split('x')[0]), 'height': int(temp.split('x')[1])}

    def get_device_datetime(self):
        return self.shell_cmd('date "+%Y-%m-%d_%H:%M:%S"').strip()

    def get_current_activity(self):
        ret = self.shell_cmd('dumpsys activity top').split('ACTIVITY')[1].split('\n')[0].split()[0].strip()
        return ret.split('/')[0] + '/' + ret.split('/')[0] + ret.split('/')[1]

    def get_current_pkg(self):
        return self.get_current_activity().split('/')[0].strip()

    def wait_for_activity(self, activity, waitMs=5000):
        time.sleep(waitMs/1000)
        if self.get_current_activity() == activity:
            return True
        else:
            raise self.ActivityNotFoundException()

    def get_current_input_method(self):
        return self.shell_cmd('ime list -s')

    # 应用相关方法
    def reset_app(self, pkgname):
        self.shell_cmd('pm clear ' + pkgname)

    def start_activity(self, app_pkg, app_main):
        self.shell_cmd('am start -n ' + app_pkg + '/' + app_main)

    def stop_app(self, app_pkg):
        self.shell_cmd('am force-stop ' + app_pkg)

    def install_app(self, apk_path):
        os.popen('adb -s ' + self.device_id + ' install -r ' + apk_path)

    def uninstall_app(self, pkgname):
        self.shell_cmd('pm uninstall ' + pkgname)

    def get_installed_app(self):
        ret = self.shell_cmd('pm list packages')
        pkgs = []
        for x in xrange(0, len(ret)):
            pkgs[x] = pkgs[x].split(':')[1].strip('\r\n')
        return pkgs

    def get_pkgs_by_type(self, app_type):
        if app_type == 'sys':
            ret = os.popen('adb -s ' + self.device_id + ' shell pm list packages -s').readlines()
        elif app_type == 'user':
            ret = os.popen('adb -s ' + self.device_id + ' shell pm list packages -3').readlines()
        pkgs = []
        for x in xrange(0, ret):
            pkgs[x] = ret[x].split(':')[1].strip('\r\n')
        return pkgs

    def is_app_installed(self, pkg):
        pkgs = self.get_installed_app()
        if pkg in pkgs:
            return True
        else:
            return False

    # 用户事件相关方法
    def click(self, x, y):
        self.shell_cmd("input tap " + str(x) + ' ' + str(y))

    def press_keycode(self, keyname):
        self.shell_cmd('input keyevent ' + str(Keycode().get(keyname)))

    def swipe(self, start_x, start_y, end_x, end_y, duration=50):
        self.shell_cmd('input swipe ' + start_x + ' ' + start_y + ' ' + end_x + ' ' + end_y + ' ' + str(duration))

    def input_text(self, text):
        # self.shell_cmd('input text "' + text + '"')
        print isinstance(text, unicode)
        if not isinstance(text, unicode):
            import unicodedata
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
        print text
        self.shell_cmd('am broadcast -a MOB_INPUT_TEXT --es text ' + text)

    def reboot(self, to=None):
        if to == 'recovery':
            # recovery mode
            self.shell_cmd('reboot recovery')
        elif to == 'bootloader':
            # fastboot mode
            self.shell_cmd('reboot bootloader')

    # UI元素相关方法
    def __uidump__(self):
        # Dump Current control tree  --compressed
        temp = self.shell_cmd('"uiautomator dump /data/local/tmp/uidump.xml|cat /data/local/tmp/uidump.xml"')
        with open(self.tempFile + '\\uidump.xml', 'w') as f:
            f.write(str(temp))
            f.close()
        # os.popen("adb -s " + self.device_id + " pull /data/local/tmp/uidump.xml " + self.tempFile)

    def __element__(self, attrib, name):
        # 同属性单个元素，返回单个坐标元组
        self.__uidump__()
        tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
        for elem in tree.iter(tag="node"):
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                x = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                y = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                ele = self.Element(x, y, self.device_id)
                return ele

    def __elements__(self, attrib, name):
        # 同属性多个元素，返回坐标元组列表
        elements = []
        self.__uidump__()
        tree = ET.ElementTree(file=self.tempFile + "\\uidump.xml")
        for elem in tree.iter(tag="node"):
            if elem.attrib[attrib] == name:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                x = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                y = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                ele = self.Element(x, y, self.device_id)
                elements.append(ele)
        return elements

    def find_element_by_id(self, res_id):
        element = self.__element__('resource-id', res_id)
        if element is None:
            raise self.ElementNotFoundException()
        return element

    def find_elements_by_id(self, res_id):
        elements = self.__elements__('resource-id', res_id)
        if elements is None:
            raise self.ElementNotFoundException()
        return elements

    def find_element_by_name(self, name):
        element = self.__element__('text', name)
        if element is None:
            raise self.ElementNotFoundException()
        return element

    def find_elements_by_name(self, name):
        elements = self.__elements__('text', name)
        if elements is None:
            raise self.ElementNotFoundException()
        return elements

    def find_element_by_class(self, classname):
        element = self.__element__('class', classname)
        if element is None:
            raise self.ElementNotFoundException()
        return element

    def find_elements_by_class(self, classname):
        elements = self.__elements__('class', classname)
        if elements is None:
            raise self.ElementNotFoundException()
        return elements

    '''
    def find_element_by_xpath(self, xpath):
        return Element.findElementByName(xpath)

    def find_elements_by_xpath(self, res_id):
        return self.find_element_by(xpath)
    '''

# 微框架方法测试
if __name__ == '__main__':
    util = Utils()
    device_id = util.find_devices()[0]
    device = Device(device_id)
    device.__uidump__()
    xy = device.find_element_by_name(u'相机')
    print xy.x, xy.y
    print device.check_root()
    # 演示获取sdk level
    print device.get_sdk()
    # 演示获取abi
    print device.get_abi()
    # 演示获取屏幕分辨率
    print device.get_screensize()
    # 演示获取设备时间
    print device.get_device_datetime()
    # 演示获取设备截屏
    device.save_screenshot()
    # 演示获取当前activity
    print device.get_current_activity()
    # 演示获取当前包
    print device.get_current_pkg()
    # 演示等待activity启动
    device.wait_for_activity('net.oneplus.launcher/net.oneplus.launcher.Launcher', 2)
    # # 演示等待activity启动未找到抛异常
    # device.wait_for_activity('aa')
    # 演示列出当前输入法
    print device.get_current_input_method()