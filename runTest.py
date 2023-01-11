# -- coding: utf-8 --

import pytest
import time
import os
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import warnings

from TestSuites import HTMLTestRunner

warnings.simplefilter("ignore", ResourceWarning)
# 脚本路径
path = os.path.dirname(os.path.realpath(__file__))
# case用例
case_path = os.path.join(path,'testCase')
# 执行用例 返回discover
def add_case(rule="test*.py"):
    '''加载所有的测试用例'''
    # 如果不存在这个case文件夹，就自动创建一个
    if not os.path.exists(case_path):os.mkdir(case_path)
    # 定义discover方法的参数
    discover = pytest.defaultTestLoader.discover(case_path,pattern=rule,top_level_dir=None)
    return discover

# 执行报告
def run_case(discover):
    report_path =  os.path.join(path,'report')
    now = time.strftime("%Y-%m-%d-%H-%M-%S")  # 最新的报告
    report_abspath = os.path.join(report_path, now+"result.html")  # 报告的位置
    rp=open(report_abspath,"wb")
    runner=HTMLTestRunner.HTMLTestRunner(rp,
                                        title=u"测试报告",
                                        description=u"用例的执行情况")
    runner.run(discover)
    return report_abspath


def sen_mail(file_path):
    smtpserver = 'smtp.163.com'
    # 发送邮箱用户名密码
    user = 'xxxxxx@163.com'
    password = 'xxxxxx'
    # 发送邮箱
    sender = 'xxxxxx@163.com'
    # 接收邮箱
    receiver ='821006052@qq.com'
    #导入报告
    with open(file_path, "rb") as fp:
        mail_body = fp.read()
    msg=MIMEMultipart()
    body=MIMEText(mail_body,_subtype="html",_charset="utf-8")
    msg['Subject']=u'自动化测试报告'
    msg['from']=sender # 发送邮件
    msg['to']=receiver # 接手邮件
    msg.attach(body)
    att = MIMEText(mail_body, "base64", "utf-8")   # 生成附件
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment; filename="report.html"' # 生成附件名称
    msg.attach(att)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)   # 连接服务器
    smtp.login(user,password)  # 登录服务器
    # 发送邮件  split（','）分隔符
    smtp.sendmail(sender, receiver.split(','), msg.as_string())     # 关闭
    print ("邮件发送")

def main():
     discover = add_case() # 调用执行 执行用例
     file_path = run_case(discover) # 用例生成报告
     # sen_mail(file_path) # 发送报告

if __name__=="__main__":
    # add_case()
    t1 = threading.Thread(target=start)
    t1.start()
    time.sleep(20)
    t2 = threading.Thread(target=main)
    t2.start()