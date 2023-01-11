# -- coding: utf-8 --
import time
from appiumTest.common.parseConfig import config
from appiumTest.page_element.InitElement import InitPage
from appiumTest.page_element.Login_element import Login_element
from appiumTest.page_element.MainElement import MainElement
from appiumTest.utils.logger import log


class LoginFlow():
    def __init__(self,driver) -> None:
        self.driver =driver
        self.log = log
        self.initPage = InitPage(self.driver)
        self.loginEle = Login_element(self.driver)
        self.mainEle = MainElement(self.driver)

    def normalFlow(self):
        try:
            self.initPage.newversion()
            cancele_ele = self.initPage.versionCancle()
            cancele_ele.click()
            skip_ele = self.initPage.skipEle()
            skip_ele.click()
        except :
            self.log.info("第一次进入APP")
        finally:
            loginEle = self.loginEle
            un = loginEle.user_element()
            un.send_keys(config.get('login','userName'))
            pw = loginEle.password_element()
            pw.send_keys(config.get('login','passWord'))
            lb = loginEle.login_button()
            lb.click()
            time.sleep(2)
            #其他设备登陆通知
            otherELE=loginEle.otherLogin()
            if otherELE != False:
                otherELE.click()
            else:
                self.log.info('不存在%s元素'%otherELE)



    def abnormalFlow(self,userName,password,message):
        ele = self.initPage.newversion()
        if ele is not None:
            cancele_ele = self.initPage.versionCancle()
            cancele_ele.click()
            skip_ele = self.initPage.skipEle()
            skip_ele.click()
            self.log.info("第一次进入APP")
            loginEle = self.loginEle
            un = loginEle.user_element()
            un.send_keys(config.get('testdata', userName))
            pw = loginEle.password_element()
            pw.send_keys(config.get('testdata', password))
            lb = loginEle.login_button()
            lb.click()
            #获取toast
            errorMessage=loginEle.toast(message)
            self.log.info(errorMessage)
            return errorMessage
        else:
            loginEle = self.loginEle
            un = loginEle.user_element()
            un.send_keys(config.get('testdata', userName))
            pw = loginEle.password_element()
            pw.send_keys(config.get('testdata', password))
            lb = loginEle.login_button()
            lb.click()
            #获取toast
            errorMessage=loginEle.toast(message)
            self.log.info(errorMessage)
            return errorMessage



if __name__ == '__main__':
    loginTest=LoginFlow()
    loginTest.normalFlow()
