# -- coding: utf-8 --
import csv
import os
import re
import time
from appiumTest.utils.logger import log


class Adb():
    phone_IP=None
    def __init__(self,PACKAGE_NAME,START_ACTIVITY) -> None:
        #adb打开app命令
        self.startAPK='adb shell am start '+START_ACTIVITY
        #adb关闭app应用
        self.stopApk='adb shell am force-stop '+PACKAGE_NAME
        self.clearProcess='adb shell pm clear '+PACKAGE_NAME

    def sendAdb(self,msg):
        pip = os.popen(msg)
        result = pip.read()
        return result


    def startApp(self):
        os.popen(self.startAPK)
        log.info(self.startAPK)
    def stopApp(self):
        os.popen(self.stopApk)
        os.popen(self.clearProcess)

    def getDevices(self):
        pip = os.popen('adb devices')
        result = pip.read()
        devices_split = result.split('\n')
        devices = []
        for device in devices_split:
            if device == '':
                continue
            elif "\t" in device:
                devices.append(device.split("\t")[0])
        # print(devices)
        return devices
    def getSelectDevice(self):
        pip = os.popen('adb devices')
        result = pip.read()
        devices_split = result.split('\n')
        devices = []
        for device in devices_split:
            if device == '':
                continue
            devices.append(device)
        if len(devices) < 2:
            print('设备不存在')
            return -1
        if len(devices) == 2:  # 只有一台设备，直接返回
            return devices[1].split('\t')[0]
        print("选择你要操作的设备")
        for index in range(1, len(devices)):
            print("%s:\t%s" % (index, devices[index]))
        print("输入编号：")
        select = int(input())
        selectline = devices[select]
        return selectline.split('\t')[0]

    #获取内存信息
    def meminfo(self,count=1,path='readCPU.csv'):
        alldata = [("native", "dalvik", "TOTAL")]
        #设置循环次数
        while count > 0:
            # adb监控内存命令
            self.readCpu = 'adb shell dumpsys meminfo ' + PACKAGE_NAME
            lines = os.popen(self.readCpu)  # adb 查看app内存
            log.info(self.readCpu)
            bufferResult = lines.buffer.read().decode(encoding='utf8')
            if len(bufferResult)>0:
                native_heap = re.findall('Native Heap\s+\d*',bufferResult)[0]
                print("native_heap:" + str(native_heap))
                dalvik_heap = re.findall('Dalvik Heap\s+\d*',bufferResult)[0]
                print("dalvik_heap:" + str(dalvik_heap))
                total = re.findall('TOTAL\s+\d*',bufferResult)[0]
                print("total:" + str(total))
                alldata.append([native_heap, dalvik_heap, total])
                count -= 1
                print('还剩余：%s次' % count)
                time.sleep(1)  # 等待时间
                csvfile = open(path, 'w', encoding='utf8', newline='')
                writer = csv.writer(csvfile)
                writer.writerows(alldata)
                csvfile.close()
            else:
                log.info("未返回资源信息，手机监控资源失败！")


    #获取被测试的app的uid
    def getUID(self):
        adbCom_getUID='adb shell ps | grep {}' .format(PACKAGE_NAME)
        pip = os.popen(adbCom_getUID)
        result = pip.buffer.read().decode(encoding='utf8')
        log.info(adbCom_getUID)
        resultList=result.split('\n')
        uid=resultList[0].split(' ')[0]
        if "u" in uid:
            print(uid)
            return uid

    #获取设备电量
    def getBatteryService(self):
        adbCom_getBattery='adb shell dumpsys battery'
        log.info(adbCom_getBattery)
        pip = os.popen(adbCom_getBattery)
        result = pip.buffer.read().decode(encoding='utf8')
        status = re.findall('status:.\d', result)
        if '2' in status[0]:
            log.info("当前为充电状态")
        else:
            log.info("当前非充电状态")
        level=re.findall('level:.\d*', result)[0].split(':')[1]
        log.info('当前电池电量百分比:{}%'.format(level))
        temperature=re.findall('temperature:.\d*', result)[0].split(':')[1]
        temperature=int(temperature)//10
        log.info('当前电池温度:{}%'.format(temperature))
        return result

    #获取app耗电信息
    def getBatteryInfo(self,device):
        # adb -s 127.0.0.1:21503 shell dumpsys batterystats
        adbCom_getBattery='adb -s {} shell dumpsys batterystats'.format(device)
        pip = os.popen(adbCom_getBattery)
        log.info(adbCom_getBattery)
        result = pip.buffer.read().decode(encoding='utf8')

        return result

    #解析耗电信息
    def parsePowerInfo(self,info):
        start = 0
        try:
            start = info.index('Estimated power use')
        except Exception:
            print('耗电量信息不存在')
            return -1
        if start < 0:
            print('耗电量信息不存在')
            return -1
        start = info.index('Capacity', start)
        end = info.index('\n', start)
        result = info[start:end]
        capacity = re.findall('\d+\.?\d*', result)
        print(capacity)
        return capacity

    #重置电池统计信息
    def resetBattery(self):
        adbCom_resetBattery='adb shell dumpsys batterystats --reset'
        pip = os.popen(adbCom_resetBattery)
        log.info(adbCom_resetBattery)
        result = pip.buffer.read().decode(encoding='utf8')
        if 'Battery stats reset' in result:
            return result
        else:
            print("电源信息重置失败")
    def saveBatteryLog(self):
        logPath=r'C:/Users/ASUS/Desktop/battery.log'
        adbCom_saveLog='adb shell dumpsys batterystats > {}'.format(logPath)
        pip = os.popen(adbCom_saveLog)
        result = pip.buffer.read().decode(encoding='utf8')
        log.info(adbCom_saveLog)
        log.info(result)


    #获取IP
    def getIP(self):
        adbCom_getIP='adb shell ifconfig'
        pip = os.popen(adbCom_getIP)
        log.info(adbCom_getIP)
        result = pip.buffer.read().decode(encoding='utf8')
        # print(result)
        #正则表达式匹配IP
        ex=re.findall('addr:\d+\W\d+\W\d+\W\d+', result)
        ip=ex[0].split(':')[1]
        # print(ip)
        self.phone_IP = ip
        return ip

    #通过wifi连接手机
    def connnectByWifi(self):
        # 赋值给手机端口号
        adbCom_pushPort='adb tcpip 8210'
        pip = os.popen(adbCom_pushPort)
        log.info(adbCom_pushPort)
        result = pip.buffer.read().decode(encoding='utf8')
        log.info(result)
        if "restarting in TCP mode port: 8210" in result:
            #通过adb wifi 连接手机
            adbCom_connectByWifi = 'adb connect {}:8210'.format(self.phone_IP)
            log.info(adbCom_connectByWifi)
            pip = os.popen(adbCom_connectByWifi)
            result = pip.buffer.read().decode(encoding='utf8')
            log.info(result)
            if "connected to" in result:
                log.info("通过wifi连接手机成功")
                return True
            else:
                log.info("通过wifi连接手机失败")
                return False
    #断开连接
    def disconnect(self):
        adbCom_disconnect='adb disconnect {}:8210'.format(self.phone_IP)
        pip = os.popen(adbCom_disconnect)
        log.info(adbCom_disconnect)
        result = pip.buffer.read().decode(encoding='utf8')
        log.info(result)
        if "disconnected" in result:
            log.info("断开成功")
        else:
            log.error("断开失败")


    #monkeytest
    def monkeyDemo(self):
        log_path='C:/Users/ASUS/Desktop/monkeylog.log'
        adbCom_Monkey='adb shell monkey --throttle 200 --pct-touch 10  --pct-motion 20 -p {}  --kill-process-after-error -v -v -v 100  > {}'.format(PACKAGE_NAME,log_path)
        pip = os.popen(adbCom_Monkey)
        log.info(adbCom_Monkey)
        result = pip.buffer.read().decode(encoding='utf8')
        log.info(result)
        with open(log_path,'r',encoding='utf-8') as logFile:
            data=logFile.readlines()
            for i in data:
                if "ANR" in i:
                    return log.info('Application Not Responding'+i)
                elif 'GC' in i:
                    return log.info('out of memory'+i)
                elif "crash" in i:
                    return log.info('Application 崩溃'+i)
                elif "exception" in i:
                    return log.info('异常事件'+i)
            log.info('Application monkey test pass')
            logFile.close()







if __name__ == '__main__':
    PACKAGE_NAME = 'com.tal.kaoyan'
    START_ACTIVITY=PACKAGE_NAME+'/com.tal.kaoyan.ui.activity.HomeTabActivity'
    adb=Adb(PACKAGE_NAME,START_ACTIVITY)
    # adb.getUID()
    #无线测试耗电量
    # adb.getBatteryService()
    # adb.getIP()
    # adb.connnectByWifi()
    # adb.resetBattery()
    # time.sleep(60)
    # adb.saveBatteryLog()
    adb.getDevices()
    # adb.disconnect()
    #app功耗
    # reder=adb.meminfo(2)
    #monkey稳定性测试
    # adb.monkeyDemo()

