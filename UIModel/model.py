# -*- coding: utf-8 -*-
# @Time    : 18-11-14 下午4:58
# @Author  : 张帆
# @Site    : 
# @File    : Model.py
# @Software: PyCharm
import time
from abc import ABCMeta, abstractmethod
'''
设计原则：
1、需要取的值都不显示的取，只在初始化时传入mainFormControl的实例对象，通过其取得实例对象的值
2、需要设置的值都提供函数，让mainFormControl实例对象显示调用函数修改界面中值。
'''

class Model(metaclass=ABCMeta):

    def get_json(self):
        '''
        需要发送出去的包 都需要这个方法
        :return:
        '''
        raise NotImplemented

    @classmethod
    def from_json(cls, mainFormControl, json):
        '''需要接收的包,都需要这个方法'''
        raise NotImplemented

    def str_to_time_stamp(self, date_str, format_str='%Y/%m/%d'):
        '''2018/12/12 ---> 转化为时间戳'''
        time_now = time.mktime(time.strptime(date_str, format_str))
        return time_now

    def time_stamp_to_str(self,time_stamp,format_str='%Y/%m/%d'):
        '''时间戳转化结构化的时间字符串  ---> 2018/12/12'''
        time_now = time.strftime(format_str,time.localtime(time_stamp))
        return time_now


if __name__ == '__main__':
    x = Model()
    print(x.time_stamp_to_str(1381419600))
