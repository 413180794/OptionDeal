# -*- coding: utf-8 -*-
# @Time    : 18-10-19 下午3:27
# @Author  : 张帆
# @Site    : 
# @File    : fontAndColorDialogControl.py
# @Software: PyCharm


from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QDialog, QApplication

from UIModel.fontAndColorSettingModel import FontSetting, ColorSetting, ColorManage
from UIView.fontAndColorDialog import Ui_FontAndColorDialog


class FontAndColorDialogControl(QDialog, Ui_FontAndColorDialog):
    def __init__(self):
        super(FontAndColorDialogControl, self).__init__()
        self.setupUi(self)
        # 应该有默认字体
        self.show_font_label.setText(self.show_font_label.font().key())
        self.font_setting = FontSetting(self, self.show_font_label)
        self.font_color_setting = ColorSetting(self, self.show_font_color_label, QPalette.Window)
        self.interface_background_color_setting = ColorSetting(self, self.show_interface_background_color_label,
                                                               QPalette.Window)
        self.content_background_color_setting = ColorSetting(self, self.show_content_background_color_label,
                                                             QPalette.Window)

        self.selected_background_color_setting = ColorSetting(self, self.show_selected_background_label,
                                                              QPalette.Window)
        self.warning_background_color_setting = ColorSetting(self, self.show_warning_background_color_label,
                                                             QPalette.Window)

        self.color_manage = ColorManage()
        self.color_manage.add_color_setting(self.font_color_setting)
        self.color_manage.add_color_setting(self.interface_background_color_setting)
        self.color_manage.add_color_setting(self.content_background_color_setting)
        self.color_manage.add_color_setting(self.selected_background_color_setting)
        self.color_manage.add_color_setting(self.warning_background_color_setting)
        self.color_manage.init_color_setting(
            [QColor(0, 0, 0), QColor(0, 255, 0), QColor(255, 0, 0), QColor(0, 0, 255), QColor(255, 7, 0)])
        self.state = 0 # 如果state状态为0，表明当前的颜色不重复，允许点击确认修改，否则不允许点击确认修改
    @pyqtSlot()
    def on_font_toolButton_clicked(self):
        '''点击字体设置键，触发设置字体功能'''
        self.font_setting.setting()

    @pyqtSlot()
    def on_font_color_toolButton_clicked(self):
        '''点击字体颜色设置键，触发设置字体颜色功能'''
        self.font_color_setting.setting()
        self.state = self.color_manage.check_color()
        print(self.state)

    @pyqtSlot()
    def on_interface_background_color_toolButton_clicked(self):
        '''点击界面背景色设置键，触发设置背景颜色功能'''

        self.interface_background_color_setting.setting()
        self.state = self.color_manage.check_color()
        print(self.state)

    @pyqtSlot()
    def on_content_background_color_toolButton_clicked(self):
        '''点击内容背景色设置键，触发设置内容背景色功能'''

        self.content_background_color_setting.setting()
        self.state = self.color_manage.check_color()
        print(self.state)

    @pyqtSlot()
    def on_selected_background_toolButton_clicked(self):
        '''点击选中背景色设置键，触发设置选中背景色功能'''

        self.selected_background_color_setting.setting()
        self.state = self.color_manage.check_color()
        print(self.state)

    @pyqtSlot()
    def on_warning_background_color_toolButton_clicked(self):
        '''点击警示背景色设置键，触发设置警示背景色功能'''

        self.warning_background_color_setting.setting()
        self.state = self.color_manage.check_color()
        print(self.state)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    loginDialog = FontAndColorDialogControl()
    loginDialog.show()

    sys.exit(app.exec_())
