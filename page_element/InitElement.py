# -- coding: utf-8 --
from appiumTest.Base.appBase import AppBase
from appiumTest.common.ParseYaml import parseyaml
from appiumTest.utils.logger import log


class InitPage():
    def __init__(self,driver) -> None:
        self.log = log
        self.driver = driver
        self.appBase = AppBase(self.driver)


    def newversion(self):
        '''获取版本更新提示'''
        self.log.info('正在获取版本更新提示信息---------------------------------------')
        InitPage = parseyaml.find_data("InitPage", 'locators', 'versionCancle')
        type = InitPage['type']
        value = InitPage['value']
        element = self.appBase.find_element((type, value))
        self.log.info('版本更新提示元素为：%s' % element)
        InitPage = parseyaml.find_data("InitPage", 'locators', 'versionContent')
        type = InitPage['type']
        value = InitPage['value']
        message = self.appBase.find_element((type, value))
        self.log.info('版本更新提示信息为：%s'% message.text)
        return element

    def versionCancle(self):
        '''获取取消版本更新按钮'''
        self.log.info('正在获取取消版本更新按钮提示信息---------------------------------------')
        InitPage = parseyaml.find_data("InitPage", 'locators','versionCancle')
        type=InitPage['type']
        value=InitPage['value']
        element = self.appBase.find_element((type,value))
        self.log.info('取消版本更新按钮提示信息为：%s' % InitPage)
        return element

    def versionAccept(self):
        '''获取确认版本更新按钮'''
        self.log.info('正在获取确认版本更新按钮提示信息---------------------------------------')
        InitPage = parseyaml.find_data("InitPage", 'locators','versionAccept')
        type=InitPage['type']
        value=InitPage['value']
        element = self.appBase.find_element((type,value))
        self.log.info('确认版本更新按钮提示信息为：%s' % InitPage)
        return element

    #获取tips
    def skipEle(self):
        '''获取跳过提示'''
        self.log.info('正在获取跳过提示信息---------------------------------------')
        self.LoginDict = parseyaml.find_data("InitPage", 'locators','skipbtn')
        type=self.LoginDict['type']
        value=self.LoginDict['value']
        element = self.appBase.find_element((type,value))
        self.log.info('版本更新提示信息为：%s' %InitPage)
        return element



if __name__ == '__main__':
    from appiumTest.common.DriverConfig import appDriver
    initPage=InitPage(appDriver.driver)
    ele=initPage.newversion()
    cancele_ele=initPage.versionCancle()
    cancele_ele.click()
    skip_ele=initPage.skipEle()
    skip_ele.click()



