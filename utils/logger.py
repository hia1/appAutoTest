# -- coding: utf-8 --
import logging
import os
from datetime import datetime
from appiumTest.common.parseConfig import config


class Log():
    def __init__(self,BASE_DIR) -> None:
        self.BASE_DIR=BASE_DIR
        self.logger=logging.getLogger()
        self.logger.setLevel("INFO")
        if self.logger.handlers:
            self.logger.handlers.clear()

        #创建一个handle写入文件
        fh=logging.FileHandler(self.log_file(),encoding="utf-8")
        fh.setLevel("INFO")

        #创建一个handle输出控制台
        sh=logging.StreamHandler()
        sh.setLevel("INFO")

        #定义输出格式
        formatter = logging.Formatter(self.fmt)
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        #添加到handle
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    @property
    def fmt(self):
        return  '%(levelname)s\t%(asctime)s\t[%(filename)s:%(lineno)d]\t%(message)s'

    def log_file(self):
        """日志目录"""
        log_dir = os.path.join(self.BASE_DIR, 'results', config.get("file_path","logName"))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(datetime.now().strftime('%Y%m%d%H')))

project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
log=Log(project_path).logger

if __name__ == '__main__':
    log.info("hell world")