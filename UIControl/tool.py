# -*- coding: utf-8 -*-
# @Time    : 18-12-5 下午3:22
# @Author  : 张帆
# @Site    : 
# @File    : tool.py
# @Software: PyCharm
import hashlib
import time


def str_to_time_stamp(date_str, format_str='%Y/%m/%d'):
    '''2018/12/12 ---> 转化为时间戳'''
    time_now = time.mktime(time.strptime(date_str, format_str))
    return time_now


def time_stamp_to_str(time_stamp, format_str='%Y/%m/%d'):
    '''时间戳转化结构化的时间字符串  ---> 2018/12/12'''
    time_now = time.strftime(format_str, time.localtime(time_stamp))
    return time_now


def get_password_md5(password_real):
    '''获得登录界面密码的md5加密'''
    return hashlib.md5(password_real.encode('utf-8')).hexdigest()

def findSubStr(substr, str, i):
    count = 0
    while i > 0:
        index = str.find(substr)
        if index == -1:
            return -1
        else:
            str = str[index+1:]
            i -= 1
            count = count + index + 1
    return count - 1

def insert(original, new, pos):
    '''Inserts new inside original at pos.'''
    return original[:pos] + new + original[pos:]


if __name__ == '__main__':
    x = str_to_time_stamp("2018/12/23 ")
    print(x)
    y = time_stamp_to_str(1545494400.0,"%Y-%m-%d %H:%M:%S")
    print(y)