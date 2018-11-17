# -*- coding: utf-8 -*-
# @Time    : 18-11-16 下午5:34
# @Author  : 张帆
# @Site    : 
# @File    : testdll.py
# @Software: PyCharm
import ctypes
from ctypes import *

if __name__ == '__main__':
    dll = ctypes.cdll.LoadLibrary("/home/zhangfan/PycharmProjects/OptionDeal/testdll/Dll.dll")

    gBrokerID = "9999"
    gInvesterID = "ysl"
    gInvesterPassword = ""
    gMdFrontAddr = "tcp://180.168.146.187:10031"
    str_TF1706 = "ag1811"
    str_zn1705 = "al1811"
    str_cs1801 = "au1811"
    str_CF705 = "bu1811"
    g_pInstrumentID = {str_TF1706, str_zn1705, str_cs1801, str_CF705}
    instrumentNum = 4
    dll.SubMarketData(gBrokerID, gInvesterID, gInvesterPassword, 0, gMdFrontAddr, g_pInstrumentID, instrumentNum, dll.OnReturnData)