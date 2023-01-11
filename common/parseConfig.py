# -- coding: utf-8 --

'''用于读取解析config下面的配置文件'''
import os
from configparser import ConfigParser

class ReadConfig():
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ini_file=os.path.join(BASE_DIR, 'config', 'config.ini')

        self.configParser=ConfigParser()
        self.configParser.read(self.ini_file,encoding="utf-8")

    #读取配置文件
    def get(self,section,option):
        return self.configParser.get(section,option)


    #更新配置文件
    def set(self,section,option,value):
        self.configParser.set(section,option,value)
        with open(self.ini_file,"w") as fp:
            self.configParser.write(fp)


config=ReadConfig()

if __name__ == '__main__':
    print(bool(int(config.get("device", "noReset"))))