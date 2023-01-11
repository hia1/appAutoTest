# -- coding: utf-8 --
from datetime import datetime
from typing import Dict, NoReturn, Tuple, List, Union, Optional
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from appium.webdriver.webelement import WebElement as MobileWebElement
from selenium.webdriver.common.by import By
from loguru import logger
import time
from appiumTest.common.parseConfig import config
from appiumTest.utils.adb import Adb


class AppBase():
    def __init__(self, driver) -> NoReturn:
        self.driver = driver

    def get_devices(self):
        '''获取设备列表'''
        self.adb=Adb(config.get("app",'appPackage'),config.get('app','appActivity'))
        devices_list=self.adb.getDevices()
        return devices_list


    def find_element(self, element: Tuple[str, Union[str, Dict]]) -> MobileWebElement:
        """
        寻找元素
        """
        by = element[0].lower()
        value = element[1]
        try:
            if self.is_element_exist(element):
                if by == "id" :
                    return self.driver.find_element(By.ID, value)
                elif by == "name":
                    return self.driver.find_element(By.NAME, value)
                elif by == "class":
                    return self.driver.find_element(By.CLASS_NAME, value)
                elif by == "text":
                    return self.driver.find_element(By.LINK_TEXT, value)
                elif by == "partial_text":
                    return self.driver.find_element(By.PARTIAL_LINK_TEXT, value)
                elif by == "xpath":
                    return self.driver.find_element(By.XPATH, value)
                elif by == "css":
                    return self.driver.find_element(By.CSS_SELECTOR, value)
                elif by == "tag":
                    return self.driver.find_element(By.TAG_NAME, value)
                else:
                    raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")
        except Exception as e:
            logger.error(">>>>>>>> failed to find element: %s is %s. Error: %s" % (by, value, e))

    def find_elements(self, element: Tuple[str, Union[str, Dict]]) -> Union[List[MobileWebElement], List]:
        """
        寻找一组元素
        """
        by = element[0]
        value = element[1]
        try:
            if self.is_element_exist(element):
                if by == "id":
                    return self.driver.find_elements(By.ID, value)
                elif by == "name":
                    return self.driver.find_elements(By.NAME, value)
                elif by == "class":
                    return self.driver.find_elements(By.CLASS_NAME, value)
                elif by == "text":
                    return self.driver.find_elements(By.LINK_TEXT, value)
                elif by == "partial_text":
                    return self.driver.find_elements(By.PARTIAL_LINK_TEXT, value)
                elif by == "xpath":
                    return self.driver.find_elements(By.XPATH, value)
                elif by == "css":
                    return self.driver.find_elements(By.CSS_SELECTOR, value)
                elif by == "tag":
                    return self.driver.find_elements(By.TAG_NAME, value)
                else:
                    raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")
        except Exception as e:
            logger.error(">>>>>>>> failed to find elements: %s is %s. Error: %s" % (by, value, e))

    def find_all_child_element_by_xpath(self, element: Tuple[str, Union[str, Dict]]) -> Union[List[MobileWebElement], List]:
        """
        寻找元素的所有子元素
        """
        by = element[0]
        value = element[1]
        try:
            if self.is_element_exist(element):
                if by == "xpath":
                    child_value = value + '/child::*'
                    return self.driver.find_elements(By.XPATH, child_value)
                else:
                    raise NameError("Please enter the correct targeting elements 'xpath'.")
        except Exception as e:
            logger.error(">>>>>>>> failed to find elements: %s is %s. Error: %s" % (by, value, e))

    def save_screenshot(self, picture_name: str) -> NoReturn:
        """
        获取屏幕截图
        """
        fmt = '%Y%m%d%H%M%S'  # 定义时间显示格式
        date = time.strftime(fmt, time.localtime(time.time()))  # 把传入的元组按照格式，输出字符串
        picture_name = "../Result/" + picture_name + "-" + date + ".jpg"
        self.driver.get_screenshot_as_file(picture_name)

    def get_screen_size(self) -> Tuple[int, int]:
        """
        获取手机屏幕大小
        """
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def swipe_screen(self, direction: str, duration_ms: int = 800) -> NoReturn:
        """
        屏幕向上滑动
        """
        location = self.get_screen_size()
        if direction.lower() == "up":
            x = int(location[0] * 0.5)
            start_y = int(location[1] * 0.75)
            end_y = int(location[1] * 0.25)
            self.driver.swipe(x, start_y, x, end_y, duration_ms)
        elif direction.lower() == "down":
            x = int(location[0] * 0.5)
            start_y = int(location[1] * 0.25)
            end_y = int(location[1] * 0.75)
            self.driver.swipe(x, start_y, x, end_y, duration_ms)
        elif direction.lower() == "left":
            start_x = int(location[0] * 0.75)
            y = int(location[1] * 0.5)
            end_x = int(location[0] * 0.05)
            self.driver.swipe(start_x, y, end_x, y, duration_ms)
        elif direction.lower() == "right":
            start_x = int(location[0] * 0.05)
            y = int(location[1] * 0.5)
            end_x = int(location[0] * 0.75)
            self.driver.swipe(start_x, y, end_x, y, duration_ms)
        else:
            print("请输入正确的方向")

    def tap_screen(self, positions: List[Tuple[int, int]], duration: Optional[int] = None) -> NoReturn:
        """
        用最多五个手指轻拍一个特定的地方，保持一定的时间
        用法：tap_screen([(100, 20), (100, 60), (100, 100)], 500)
        """
        self.driver.tap(positions, duration)

    def click(self, element: Tuple[str, Union[str, Dict]], found_index: int = -1) -> NoReturn:
        """
        点击按钮
        """
        if found_index == -1:
            self.find_element(element).click()
        else:
            self.find_elements(element)[found_index].click()

    def send_keys(self, element: Tuple[str, Union[str, Dict]], value: str, clear_first: bool = False, click_first: bool = False, found_index: int = -1) -> NoReturn:
        """
        键盘输入
        """
        if found_index == -1:
            if click_first:
                self.find_element(element).click()
            if clear_first:
                self.find_element(element).clear()
            self.find_element(element).send_keys(value)
        else:
            if click_first:
                self.find_elements(element)[found_index].click()
            if clear_first:
                self.find_elements(element)[found_index].clear()
            self.find_elements(element)[found_index].send_keys(value)

    def scroll_to_text(self, text) -> NoReturn:
        """
        滚动到指定的text
        """
        uiautomator_cmd = "new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text(\"%s\").instance(0))" % text
        # self.driver.find_element_by_android_uiautomator(uiautomator_cmd)
        self.driver.find_element('-android uiautomator',uiautomator_cmd)

    def get_attribute(self, element: Tuple[str, Union[str, Dict]], attribute_name: str = 'text', found_index: int = -1) -> Optional[Union[str, Dict]]:
        """
        获取元素属性
        """
        if found_index == -1:
            return self.find_element(element).get_attribute(attribute_name)
        else:
            return self.find_elements(element)[found_index].get_attribute(attribute_name)

    def is_element_exist(self, element: Tuple[str, Union[str, Dict]], wait_seconds: int = 10) -> bool:
        """
        判断元素是否存在
        """
        by = element[0].lower()
        value = element[1]
        try:
            if by == "id":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.ID, value)))
            elif by == "name":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "text":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "partial_text":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, value)))
            elif by == "xpath":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, value)))
            elif by == "tag":
                WebDriverWait(self.driver, wait_seconds, 1).until(expected_conditions.presence_of_element_located((By.TAG_NAME, value)))
            else:
                raise NameError("Please enter the correct targeting elements,'id','name','class','text','xpath','css'.")
        except:
            return False
        return True

    def is_text_exist(self, text: str, wait_seconds: int = 3) -> bool:
        """
        判断text是否于当前页面存在
        """
        for i in range(wait_seconds):
            if text in self.driver.page_source:
                return True
            time.sleep(1)

        return False
    def toast(self,message):
        '''获取toast信息'''
        try:
            toast_loc = ("xpath", ".//*[contains(@text,'%s')]"%message)
            content = WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located(toast_loc)).text
            return content
        except:
            with allure.step('测试截图'):
                pngName="toast截图"+'{}.png'.format(datetime.now().strftime('%Y%m%d%H'))
                allure.attach(self.driver.get_screenshot_as_png(), pngName, allure.attachment_type.PNG)

    def quit(self) -> NoReturn:
        """
        退出驱动
        """
        self.driver.quit()

if __name__ == '__main__':
    from appiumTest.common.DriverConfig import appDriver
    ab=AppBase(appDriver.driver)
    ab.get_devices()