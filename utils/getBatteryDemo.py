# -- coding: utf-8 --


import re
import os


def getSelectDevice():
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


def getBatteryInfo(device):
    pip = os.popen('adb -s %s shell dumpsys batterystats' % device)
    result = pip.buffer.read().decode(encoding='utf8')
    return result


def parsePowerInfo(info):
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

    return capacity


def parseResetTimeInfo(info):
    start = 0

    try:
        start = info.index('RESET:TIME:')
    except Exception:
        print('重置时间不存在')
        return -1
    if start < 0:
        print('重置时间不存在')
        return -1
    end = info.index('\n', start)

    result = info[start:end]

    capacity = re.findall('\d+\.?\d*', result)
    return capacity


def main():
    device = getSelectDevice()
    if device == -1:
        return
    print("正在获取信息...")
    betteryinfo = getBatteryInfo(device)
    if betteryinfo == -1:
        return
    print("正在解析信息...")
    result = parsePowerInfo(betteryinfo)
    if result == -1:
        return

    print("得出结果：")
    print("\t电池容量：%s mA" % (result[0]))
    print("\t计算耗电：%s mA" % (result[1]))
    print("\t实际耗电：%s mA" % (result[2]))

    timeinfo = parseResetTimeInfo(betteryinfo)
    if timeinfo == -1:
        return
    print("重置时间：%s-%s-%s %s:%s:%s" % (timeinfo[0], timeinfo[1], timeinfo[2], timeinfo[3], timeinfo[4], timeinfo[5]))
    pass


if __name__ == '__main__':
    main()
    pass

