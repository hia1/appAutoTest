# -- coding: utf-8 --

"""
Created on Sat Nov  6 10:00:35 2021

@author: liuyunshengsir
"""

import bluetooth

print("开始搜索附近蓝牙...")

nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,flush_cache=True, lookup_class=False)

print("找到 {} 个蓝牙设备".format(len(nearby_devices)))

for addr, name in nearby_devices:
    try:
        print("  mac地址 ：{} - 蓝牙名称：{}".format(addr, name))
    except UnicodeEncodeError:
        print(" mac地址 ：{} - 蓝牙名称：{}".format(addr, name.encode("utf-8", "replace")))
