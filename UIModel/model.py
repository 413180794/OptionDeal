# -*- coding: utf-8 -*-
# @Time    : 18-11-14 下午4:58
# @Author  : 张帆
# @Site    : 
# @File    : Model.py
# @Software: PyCharm
from abc import ABCMeta, abstractmethod


class Model(metaclass=ABCMeta):

    @abstractmethod
    def get_json(self):
        '''
        需要发送出去的包 都需要这个方法
        :return:
        '''
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, mainFormControl, json):
        '''需要接收的包,都需要这个方法'''
        pass
