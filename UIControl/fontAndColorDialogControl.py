# -*- coding: utf-8 -*-
# @Time    : 18-10-19 下午3:27
# @Author  : 张帆
# @Site    : 
# @File    : fontAndColorDialogControl.py
# @Software: PyCharm
from abc import ABCMeta, abstractmethod

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QDialog, QApplication, QFontDialog, QColorDialog
from UIpy.fontAndColorDialog import Ui_FontAndColorDialog


class Setting(metaclass=ABCMeta):
    ''' 抽象类 定义 设置字体与设置颜色的抽象父类,分析可知两种操作非常相似
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
        self.setLable()

    @abstractmethod
    def createDialog(self):
        '''弹出字体或者颜色对话框'''
        pass

    @abstractmethod
    def setLable(self):
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

    def setLable(self):
        if self.ok:
            self.label.setFont(self.font)
            self.label.setText(self.font.key())


class ColorSetting(Setting):
    '''颜色设置'''

    def createDialog(self):
        self.color = QColorDialog.getColor(Qt.green, self.dialog, "Select Color")

    def setLable(self):
        if self.color.isValid():
            pa = QPalette()
            pa.setColor(self.set_what, self.color)
            self.label.setPalette(pa)
            self.label.setAutoFillBackground(True)

    def __init__(self, dialog, label, set_what):
        super(ColorSetting, self).__init__(dialog, label)
        self.color = None
        self.dialog = dialog
        self.label = label
        self.set_what = set_what


class FontAndColorDialogControl(QDialog, Ui_FontAndColorDialog):
    def __init__(self):
        super(FontAndColorDialogControl, self).__init__()
        self.setupUi(self)
        # 应该有默认字体
        self.show_font_label.setText(self.show_font_label.font().key())

    @pyqtSlot()
    def on_font_toolButton_clicked(self):
        '''点击字体设置键，触发设置字体功能'''
        font_setting = FontSetting(self, self.show_font_label)
        font_setting.setting()

    @pyqtSlot()
    def on_font_color_toolButton_clicked(self):
        '''点击字体颜色设置键，触发设置字体颜色功能'''
        color_setting = ColorSetting(self,self.show_font_color_label,QPalette.Window)
        color_setting.setting()

    @pyqtSlot()
    def on_interface_background_color_toolButton_clicked(self):
        '''点击界面背景色设置键，触发设置背景颜色功能'''

        color_setting = ColorSetting(self, self.show_interface_background_color_label, QPalette.Window)
        color_setting.setting()
    @pyqtSlot()
    def on_content_background_color_toolButton_clicked(self):
        '''点击内容背景色设置键，触发设置内容背景色功能'''

        color_setting = ColorSetting(self, self.show_content_background_color_label, QPalette.Window)
        color_setting.setting()
    @pyqtSlot()
    def on_selected_background_toolButton_clicked(self):
        '''点击选中背景色设置键，触发设置选中背景色功能'''
        color_setting = ColorSetting(self, self.show_selected_background_label, QPalette.Window)
        color_setting.setting()
    @pyqtSlot()
    def on_warning_background_color_toolButton_clicked(self):
        '''点击警示背景色设置键，触发设置警示背景色功能'''
        color_setting = ColorSetting(self, self.show_warning_background_color_label, QPalette.Window)
        color_setting.setting()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    loginDialog = FontAndColorDialogControl()
    loginDialog.show()

    sys.exit(app.exec_())
