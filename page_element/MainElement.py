# -- coding: utf-8 --
from appiumTest.Base.appBase import AppBase
from appiumTest.common.ParseYaml import parseyaml
from appiumTest.utils.logger import log


class MainElement():
    def __init__(self,driver) -> None:
        self.driver=driver
        self.log=log
        self.appBase = AppBase(self.driver)

    def iKnow(self):
        '''获取我知道了的按钮'''
        self.log.info('正在获取我知道了的按钮提示信息---------------------------------------')
        InitPage = parseyaml.find_data("alert", 'locators','know')
        type=InitPage['type']
        value=InitPage['value']
        element = self.appBase.find_element((type,value))
        self.log.info('获取我知道了的按钮提示信息为：%s' % InitPage)
        return element
    def myself(self):
        '''获取导航栏我按钮'''
        self.log.info('正在获取导航栏"我"按钮的提示信息---------------------------------------')
        InitPage = parseyaml.find_data("MainPage", 'locators','myself')
        type=InitPage['type']
        value=InitPage['value']
        element = self.appBase.find_element((type,value))
        self.log.info('获取获取导航栏"我"按钮的提示信息为：%s' % InitPage)
        return element

