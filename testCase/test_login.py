# -- coding: utf-8 --
import os
import pytest


from appiumTest.flow.loginFlow import LoginFlow
from appiumTest.page_element.MainElement import MainElement
from appiumTest.utils.logger import log


@pytest.mark.flaky(reruns=1, reruns_delay=2)
class TestLogin():
    from appiumTest.common.DriverConfig import appDriver
    driver=appDriver.driver
    def setup_class(self):
        '''启动apk'''
        log.info('reset driver')
        self.driver.reset()
    def teardown_method(self):
        '''退出APK'''
        self.driver.reset()
        log.info('reset driver')

    @pytest.mark.run(order=3)
    def test01(self,init_driver):
        global mainele
        log.info('登录正常测试'+'*'*10)
        loginTest = LoginFlow(init_driver)
        loginTest.normalFlow()
        try:
            mainElement = MainElement(init_driver)
            mainele=mainElement.myself().text
        except Exception as e:
            print(e)
        assert "我" == mainele

    def test02(self,init_driver):
        log.info('登录异常测试:错误账号密码' + '*' * 10)
        loginTest = LoginFlow(init_driver)
        errorMessage=loginTest.abnormalFlow("errorName",'errorWord','账号')
        assert "账号" in errorMessage


    def test03(self,init_driver):
        log.info('登录异常测试:错误账号空密码' + '*' * 10)
        loginTest = LoginFlow(init_driver)
        errorMessage=loginTest.abnormalFlow("errorName",'emptyData','空')
        assert "空" in errorMessage

    def test04(self,init_driver):
        log.info('登录异常测试:空账号错误密码' + '*' * 10)
        loginTest = LoginFlow(init_driver)
        errorMessage=loginTest.abnormalFlow("emptyData",'errorWord','空')
        assert "空" in errorMessage

    def test05(self,init_driver):
        log.info('登录异常测试:正确账号错误密码' + '*' * 10)
        loginTest = LoginFlow(init_driver)
        errorMessage=loginTest.abnormalFlow("userName",'errorWord','错误')
        assert "空" in errorMessage

    def test06(self,init_driver):
        log.info('登录异常测试:错误账号正确密码' + '*' * 10)
        loginTest = LoginFlow(init_driver)
        errorMessage=loginTest.abnormalFlow("errorName",'passWord','账号不存在')
        assert "不存在" in errorMessage

    def test07(self,init_driver):
        log.info('登录异常测试:空账号正确密码' + '*' * 10)
        loginTest = LoginFlow(init_driver)
        errorMessage=loginTest.abnormalFlow("errorName",'passWord','不存在')
        assert "不存在" in errorMessage

    def test08(self,init_driver):
        log.info('登录异常测试:空账号空密码' + '*' * 10)
        loginTest = LoginFlow(init_driver)
        errorMessage=loginTest.abnormalFlow("emptyData",'emptyData','空')
        assert "空" in errorMessage

if __name__ == '__main__':
    # pytest.main(["-vs","--html=report/report0414.html"])
    # 第一步：生成json格式临时文件
    pytest.main(['-vs','--clean-alluredir','--alluredir','../report/result',])
    # 第二步：根据json格式临时文件生成allure报告
    os.system("allure generate ../report/result/ -o ../report/html --clean")
    os.system("allure serve ./report/result")