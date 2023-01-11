# -- coding: utf-8 --
import os
import threading
from datetime import datetime
import allure
import pytest
from appiumTest.utils.adb import Adb

driver = None   # 定义一个全局driver对象
driverList=None
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()      # 获取测试用例执行完成之后的结果
    if rep.when == 'call' and rep.failed:   # 判断用例执行情况：被调用
        mode = "a" if os.path.exists("failures") else "w"
        with open("results/failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        # 添加allure报告截图
        with allure.step('添加失败截图...'):
            pngName = '失败截图{}.png'.format(datetime.now().strftime('%Y%m%d%H'))
            allure.attach(driver.get_screenshot_as_png(), pngName, allure.attachment_type.PNG)




# 自定义fixture实现driver初始化及赋值并且返回
# @pytest.fixture(scope='session',autouse=True)
# def init_driver():
#     global driver   # global变量，相当于给上面driver = None赋值了
#     server = Server()
#     devices=server.get_devices()
#     if driver is None and len(devices)==1:
#         from appiumTest.common.DriverConfig import appDriver
#         driver=appDriver.driver
#         return driver
#     elif(len(devices)>=2):
#         server.main()
#         threadPool = []
#         driverList=[]
#         for i in server.get_desired_caps():
#             driver = server.start_android(i)
#             driverList.append(driver)
#             t = threading.Thread(target=driver.reset)
#             threadPool.append(t)
#         yield driverList
#         for j in threadPool:
#             j.start()



@pytest.fixture(scope='session',autouse=True)
def get_driver():
    global driver
    from appiumTest.common.parseConfig import config
    adb = Adb(config.get("app", 'appPackage'), config.get('app', 'appActivity'))
    devices=adb.getDevices()
    if driver is None and len(devices)==1:
        from appiumTest.common.DriverConfig import appDriver
        driver=appDriver.driver
        return driver
    elif(len(devices)>=2):
        from appiumTest.common.Server import Server
        server = Server()
        server.main()
        threadPool = []
        global driverList
        driverList=[]
        for i in server.get_desired_caps():
            driver=server.start_android(i)
            t = threading.Thread(target=driver.reset)
            driverList.append(driver)
            threadPool.append(t)
        for j in threadPool:
            j.start()
        return driverList


@pytest.fixture(scope='session',params=driverList)
def init_driver(request):
    return request.param