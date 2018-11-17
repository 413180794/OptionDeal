# -*- coding: utf-8 -*-
# @Time    : 18-11-2 上午9:48
# @Author  : 张帆
# @Site    : 
# @File    : fontAndColorSetting.py
# @Software: PyCharm
import itertools
from abc import ABCMeta, abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QFontDialog, QColorDialog


class Setting(metaclass=ABCMeta):
    ''' 抽象类 主题类 定义 设置字体与设置颜色的抽象父类,分析可知两种操作非常相似
    1.点击按键，触发按键的函数
    2.font弹出QFontDialog，返回font，ok --------   color弹出QColorDialog，返回color
    3.取得返回值后,拿到返回值去操作需要设置的label
    4.结束
    '''

    def __init__(self, dialog, label):
        '''

        :param dialog: 需要控制的dialog
        :param label: 需要设置的label
        '''
        self.dialog = dialog
        self.label = label

    def setting(self):
        '''操作'''
        self.createDialog()
        self.setLabel()

    @abstractmethod
    def createDialog(self):
        '''弹出字体或者颜色对话框'''
        pass

    @abstractmethod
    def setLabel(self):
        '''取得返回值操作对话框'''
        pass


class FontSetting(Setting):
    '''字体设置'''

    def __init__(self, dialog, label):
        super(FontSetting, self).__init__(dialog, label)
        self.font = None
        self.ok = None
        self.dialog = dialog
        self.label = label

    def createDialog(self):
        self.font, self.ok = QFontDialog.getFont(self.dialog)

    def setLabel(self):
        if self.ok:
            self.label.setFont(self.font)
            self.label.setText(self.font.key())


class ColorSetting(Setting):
    '''颜色设置'''

    def __init__(self, dialog, label, set_label):
        super(ColorSetting, self).__init__(dialog, label)
        self.color = None
        self.dialog = dialog
        self.label = label
        self.set_label = set_label

    def createDialog(self):
        self.color = QColorDialog.getColor(Qt.green, self.dialog, "Select Color")

    def setLabel(self, color=None):
        '''设置颜色之前，要检查颜色是否已经重复'''
        if color is None:
            if self.color.isValid():
                pa = QPalette()
                pa.setColor(self.set_label, self.color)
                self.label.setPalette(pa)
                self.label.setAutoFillBackground(True)
        else:
            if color.isValid():
                self.color = color
                pa = QPalette()
                pa.setColor(self.set_label, color)
                self.label.setPalette(pa)
                self.label.setAutoFillBackground(True)


class ColorManage:
    '''管理所有颜色设置对象'''

    def __init__(self):
        self.color_setting_list = []

    def add_color_setting(self, colorSetting: ColorSetting):
        self.color_setting_list.append(colorSetting)

    def init_color_setting(self, color_list):
        '''初始化颜色'''
        if len(color_list) != len(self.color_setting_list):
            raise Exception
        for color_setting, color in itertools.zip_longest(self.color_setting_list, color_list):
            color_setting.setLabel(color)

    def print_color(self):
        for color_setting in self.color_setting_list:
            print(color_setting.color)

    def check_color(self):
        '''检查颜色是否重复'''
        for i in range(len(self.color_setting_list)):
            for j in range(i + 1, len(self.color_setting_list)):
                print(self.color_setting_list[i].color)
                if self.color_setting_list[i].color == self.color_setting_list[j].color:
                    return 0
        return 1


if __name__ == '__main__':
    x = itertools.zip_longest("abc", 'cde')
    for x1, y in x:
        print(x1, y)
