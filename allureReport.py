# -- coding: utf-8 --
import os
import pytest




if __name__ == '__main__':
    # pytest.main(["-vs","--html=report/report0414.html"])
    # 第一步：生成json格式临时文件
    pytest.main(['-vs','--clean-alluredir','--alluredir','./report/result'])
    # 第二步：根据json格式临时文件生成allure报告
    os.system("allure generate report/result/ -o report/html --clean")
    #运行完成直接打开allure测试报告
    os.system("allure serve ./report/result")