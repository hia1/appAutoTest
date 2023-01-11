# -- coding: utf-8 --
import multiprocessing
import os
import threading
import time
from appium import webdriver
from Utils.logger import log
from appiumTest.common.ParseYaml import parseyaml
from appiumTest.common.parseConfig import config
from appiumTest.utils.adb import Adb


class Server():
    def __init__(self) -> None:
        self.adb=Adb(config.get("app",'appPackage'),config.get('app','appActivity'))

    #获取连接设备列表
    def get_devices(self):
        devices_list=self.adb.getDevices()
        return devices_list

    '''生成appium多启动命令列表'''
    def get_appium(self):
        appium_port=parseyaml.get_data('appium_port')
        # print((appium_port))
        appium_list=[]
        devices=self.get_devices()
        bp = 4900
        if len(devices) >= 2:
            for device in devices:
                if len(devices) == len(appium_port):
                    for port in appium_port:
                            if appium_port.index(port) == devices.index(device):
                                appium='appium -p %s  -U %s' %(port,device)
                                appium_list.append(appium)
                                bp+=1
                else:
                    log.debug("inconformity devices and appium_port")
                    return None

            # print(appium_list)
            log.info(appium_list)
            return appium_list
        else:
            log.info("devices nums <2")
            return appium_list
    '''执行appium启动'''
    def start_appium(self,start):
        print(os.system(start))

    '''多进程程启动'''
    def main(self):
        multi_list=[]
        for i in self.get_appium():
            appium_server=multiprocessing.Process(target=self.start_appium,args=(i,))
            multi_list.append(appium_server)
        for j in multi_list:
            j.start()
        # for j in multi_list:
        #     j.join()



    '''获取设备desired_caps和appium port'''
    def get_desired_caps(self):
        android_list=[]
        appium_port = parseyaml.get_data('appium_port')
        for deviceName in self.get_devices():
            for port in appium_port:
                if self.get_devices().index(deviceName) == appium_port.index(port):
                    appiumPort=port
                    desired_caps={
                    'platformName': 'Android',  # 测试版本
                    'deviceName': deviceName,  # 设备名
                    'platformVersion': config.get("simulator", "platformVersion"),  # 系统版本
                    "appPackage": config.get("app", "appPackage"),  # app包名
                    "appActivity": config.get("app", "appActivity"),
                    "noReset": bool(int(config.get("device", "noReset"))),  # 清空数据
                    "unicodeKeyboard": True,  # 使用Unicode编码方式发送字符串
                    "resetKeyboard": True,  # 键盘隐藏起来
                    'automationName' : "uiautomator2"  # 定位toast
                }
                    android= {"appium_port":appiumPort,"desired_caps":desired_caps}
                    android_list.append(android)
        print(android_list)
        return android_list



    '''启动webdriver'''
    # def start_android(self):
    #     deviceInfo=self.get_desired_caps()
    #     start_list=[]
    #     for i in deviceInfo:
    #         driver = webdriver.Remote('http://127.0.0.1:%s/wd/hub' % i['appium_port'], i['desired_caps'])
    #         log.info(driver)
    #         start_list.append(driver)
    #     return start_list
    def start_android(self,i):
        driver = webdriver.Remote('http://127.0.0.1:%s/wd/hub' % i['appium_port'], i['desired_caps'])
        log.info(driver)
        return driver



if __name__ == '__main__':
    from appiumTest.flow.loginFlow import LoginFlow
    '''实现APP同时启动'''
    # server=Server()
    # server.main()
    # time.sleep(2)
    # threadPool=[]
    # for i in server.get_desired_caps():
    #     t=threading.Thread(target=server.start_android,args=(i,))
    #     threadPool.append(t)
    # for j in threadPool:
    #     j.start()
    server=Server()
    server.main()
    time.sleep(2)
    threadPool=[]
    for i in server.get_desired_caps():
        driver=server.start_android(i)
        loginTest = LoginFlow(driver)
        t=threading.Thread(target=loginTest.normalFlow)
        threadPool.append(t)
    for j in threadPool:
        j.start()












