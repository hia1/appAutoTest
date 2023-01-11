# -- coding: utf-8 --
import os
import yaml

from appiumTest.common.parseConfig import config


class ParseYaml():
    def __init__(self) -> None:
        yamldir=config.get('file_path','yamldir')
        yamlName=config.get('file_path','yamlName')
        projectPath=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yaml_file = os.path.join(projectPath, yamldir, yamlName)
        # print(yaml_file)
        #判断yaml文件是否存在
        if os.path.exists(yaml_file):
            self.file_path = yaml_file
        else:
            raise FileNotFoundError("%s 文件不存在" % yaml_file)
        self.data = self.read_yaml()

    def read_yaml(self):
         with open(self.file_path,'r',encoding='utf-8')as fp:
            data = fp.read()
            return data
    def get_data(self,key=None):
        result = yaml.load(self.data,Loader=yaml.FullLoader)
        if key == None:
            return result
        else:
            return result.get(key)

    def find_data(self,item,listKey,key):
        result = yaml.load(self.data, Loader=yaml.FullLoader)
        if item == None:
            return result
        else:
            if listKey == None:
                return result.get(item)
            else:
                dataDict=result.get(item)
                for dict in dataDict.get(listKey):
                    if key in dict:
                        # print(dict.get(key))
                        # return {'type': 'id', 'value': 'android:id/message'}
                        return dict.get(key)



parseyaml=ParseYaml()
if __name__ == '__main__':
    LoginPage=parseyaml.get_data("LoginPage")
    print(type(LoginPage['locators'][0]),LoginPage['locators'][0])
    parseyaml.find_data('InitPage','locators','versionContent')



