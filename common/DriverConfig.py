# -- coding: utf-8 --
from appium  import webdriver
from appiumTest.common.parseConfig import config

#获取驱动配置
class AppiumDriver():

    def __init__(self) -> None:
        self.driver = webdriver.Remote(self.get_command_executor(),self.get_desired_caps())

    def get_command_executor(self):
        command_executor=config.get("executor", "command_executor")
        return command_executor
    def get_desired_caps(self):
        desired_caps = {
            'platformName': 'Android',  # 测试版本
            'deviceName': config.get("simulator", "deviceName"),  # 设备名
            'platformVersion': config.get("simulator", "platformVersion"),  # 系统版本
            "appPackage": config.get("app", "appPackage"),  # app包名
            "appActivity": config.get("app", "appActivity"),
            "noReset": bool(int(config.get("device", "noReset"))),  # 清空数据
            "unicodeKeyboard": True,  # 使用Unicode编码方式发送字符串
            "resetKeyboard": True,  # 键盘隐藏起来
            'automationName' : "uiautomator2"  # 定位toast
        }
        return desired_caps
appDriver=AppiumDriver()
if __name__ == '__main__':
    print(appDriver.driver)