# -- coding: utf-8 --
from appiumTest.Base.appBase import AppBase
from appiumTest.common.ParseYaml import parseyaml
from appiumTest.utils.logger import log


class Login_element:
    def __init__(self,driver):
        self.log = log
        self.driver = driver
        self.appBase=AppBase(driver)

    def user_element(self):
        ''' 获取用户名元素'''
        self.log.info('正在获取用户名元素信息---------------------------------------')
        self.LoginDict = parseyaml.find_data("LoginPage", 'locators','userName')
        type=self.LoginDict['type']
        value=self.LoginDict['value']
        element = self.appBase.find_element((type,value))
        self.log.info('用户名元素信息为：%s'%self.LoginDict)
        return element

    def password_element(self):
        ''' 获取密码元素'''
        self.log.info('正在获取密码元素信息-------------------------------------')
        self.LoginDict = parseyaml.find_data("LoginPage", 'locators', 'passWord')
        type=self.LoginDict['type']
        value=self.LoginDict['value']
        element = self.appBase.find_element((type,value))
        self.log.info('密码元素信息为：%s'%self.LoginDict)
        return element

    def login_button(self):
        ''' 获取登录按钮元素'''
        self.log.info('正在获取登录按钮元素信息-------------------------------------')
        self.LoginDict = parseyaml.find_data("LoginPage", 'locators', 'login_btn')
        type = self.LoginDict['type']
        value = self.LoginDict['value']
        element = self.appBase.find_element((type, value))
        self.log.info('登录按钮元素信息为：%s' %self.LoginDict)
        return element

    def otherLogin(self):
        ''' 获取异常设备登录弹窗提示'''
        self.log.info('正在异常设备登录弹窗提示信息-------------------------------------')
        self.LoginDict = parseyaml.find_data("alert", 'locators', 'ontherLogin')
        type = self.LoginDict['type']
        value = self.LoginDict['value']
        tip_title = self.appBase.find_element((type, value))
        self.log.info('获取异常设备登录弹窗提示信息头为：%s' % self.LoginDict)
        self.ontherLoginContent = parseyaml.find_data("alert", 'locators', 'ontherLoginContent')
        type = self.ontherLoginContent['type']
        value = self.ontherLoginContent['value']
        tip_message = self.appBase.find_element((type, value))
        self.log.info('获取异常设备登录弹窗提示信息为：%s' % tip_message.text)
        self.ontherLoginbtn = parseyaml.find_data("alert", 'locators', 'ontherLoginbtn')
        type = self.ontherLoginbtn['type']
        value = self.ontherLoginbtn['value']
        tip_commit = self.appBase.find_element((type, value))
        self.log.info('获取异常设备登录弹窗提示为：%s' % self.ontherLoginbtn)
        return tip_commit

    def toast(self,message):
        '''获取toast信息'''
        return self.appBase.toast(message)


    def register(self):
        ''' 获取注册元素'''
        self.log.info('正在获取注册元素信息-------------------------------------')
        self.LoginDict = parseyaml.find_data("LoginPage", 'locators', 'register')
        type = self.LoginDict['type']
        value = self.LoginDict['value']
        element = self.appBase.find_element((type, value))
        self.log.info('获取注册元素信息为：%s' % self.LoginDict)
        return element


    def forgetPassword(self):
        ''' 获取忘记密码元素'''
        self.log.info('正在获取忘记密码元素信息-------------------------------------')
        self.LoginDict = parseyaml.find_data("LoginPage", 'locators', 'forgeetPassword')
        type = self.LoginDict['type']
        value = self.LoginDict['value']
        element = self.appBase.find_element((type, value))
        self.log.info('获取忘记密码元素信息为：%s' % self.LoginDict)
        return element

    def otherPlatformlogin(self):
        pass



if __name__ == '__main__':
    from appiumTest.common.DriverConfig import appDriver
    loginEle=Login_element(appDriver.driver)
    # un=loginEle.user_element()
    # un.send_keys('1')
    # pw=loginEle.password_element()
    # pw.send_keys('2')
    # lb=loginEle.login_button()
    # lb.click()
    # result=loginEle.toast('错误')
    # print(result)
    register=loginEle.register()
    register.click()