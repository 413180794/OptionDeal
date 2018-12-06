# -*- coding: utf-8 -*-
# @Time    : 18-10-19 下午3:27
# @Author  : 张帆
# @Site    : 
# @File    : fontAndColorDialogControl.py
# @Software: PyCharm


from PyQt5.QtCore import pyqtSlot, QSettings, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QDialog, QApplication, QFontDialog, QColorDialog, QMessageBox

from UIView.fontAndColorDialog import Ui_FontAndColorDialog


class FontAndColorDialogControl(QDialog, Ui_FontAndColorDialog):
    def __init__(self,reset_ui,parent):
        super(FontAndColorDialogControl, self).__init__(parent)
        self.setupUi(self)
        # 应该有默认字体
        self.color_list = [None] * 5
        self.settings = QSettings('color_font')
        self.font = self.settings.value("font")
        self.reset_ui = reset_ui
        if self.font:
            self.set_font(self.show_font_label, self.font)

        self.font_color = self.settings.value("font_color")
        if self.font_color:
            self.set_color(self.show_font_color_label, self.font_color)
            self.color_list[0] = self.font_color

        self.background_color = self.settings.value("background_color")
        if self.background_color:
            self.set_color(self.show_interface_background_color_label, self.background_color)
            self.color_list[1] = self.background_color

        self.content_color = self.settings.value("content_color")
        if self.content_color:
            self.set_color(self.show_content_background_color_label, self.content_color)
            self.color_list[2] = self.content_color

        self.selected_color = self.settings.value("selected_color")
        if self.selected_color:
            self.set_color(self.show_selected_background_label, self.selected_color)
            self.color_list[3] = self.selected_color

        self.warn_color = self.settings.value("warn_color")
        if self.warn_color:
            self.set_color(self.show_warning_background_color_label, self.warn_color)
            self.color_list[4] = self.warn_color

    def set_font(self, label, font):
        label.setFont(font)
        label.setText(font.key())

    def set_color(self, label, color):
        pa = QPalette()
        pa.setColor(QPalette.Window, color)
        label.setPalette(pa)
        label.setAutoFillBackground(True)

    @pyqtSlot()
    def on_font_toolButton_clicked(self):
        '''点击字体设置键，触发设置字体功能'''
        font, ok = QFontDialog.getFont(self)
        print(font.family())
        print(font.weight())
        print(font.pointSize())
        if ok:
            self.font = font
            self.show_font_label.setFont(font)
            self.show_font_label.setText(font.key())
            self.settings.setValue("font", font)

    @pyqtSlot()
    def on_font_color_toolButton_clicked(self):
        '''点击字体颜色设置键，触发设置字体颜色功能'''
        color = QColorDialog.getColor(Qt.green, self)
        if color.isValid():

            if color in self.color_list:
                # 如果颜色重复了
                QMessageBox.warning(self, "错误", "颜色不可重复")
                return
            else:
                self.font_color = color
                self.color_list[0] = color
                self.settings.setValue("font_color", color)
                self.set_color(self.show_font_color_label, color)

    @pyqtSlot()
    def on_interface_background_color_toolButton_clicked(self):
        '''点击界面背景色设置键，触发设置背景颜色功能'''

        color = QColorDialog.getColor(Qt.green, self)
        if color.isValid():

            if color in self.color_list:
                # 如果颜色重复了
                QMessageBox.warning(self, "错误", "颜色不可重复")
                return
            else:
                self.background_color = color
                self.color_list[1] = color
                self.settings.setValue("background_color", color)
                self.set_color(self.show_interface_background_color_label, color)

    @pyqtSlot()
    def on_content_background_color_toolButton_clicked(self):
        '''点击内容背景色设置键，触发设置内容背景色功能'''

        color = QColorDialog.getColor(Qt.green, self)
        if color.isValid():

            if color in self.color_list:
                # 如果颜色重复了
                QMessageBox.warning(self, "错误", "颜色不可重复")
                return
            else:
                self.content_color = color
                self.color_list[2] = color
                self.settings.setValue("content_color", color)
                self.set_color(self.show_content_background_color_label, color)

    @pyqtSlot()
    def on_selected_background_toolButton_clicked(self):
        '''点击选中背景色设置键，触发设置选中背景色功能'''

        color = QColorDialog.getColor(Qt.green, self)
        if color.isValid():

            if color in self.color_list:
                # 如果颜色重复了
                QMessageBox.warning(self, "错误", "颜色不可重复")
                return
            else:
                self.selected_color = color
                self.color_list[3] = color
                self.settings.setValue("selected_color", color)
                self.set_color(self.show_selected_background_label, color)

    @pyqtSlot()
    def on_warning_background_color_toolButton_clicked(self):
        '''点击警示背景色设置键，触发设置警示背景色功能'''

        color = QColorDialog.getColor(Qt.green, self)
        if color.isValid():

            if color in self.color_list:
                # 如果颜色重复了
                QMessageBox.warning(self, "错误", "颜色不可重复")
                return
            else:
                self.warn_color = color
                self.color_list[4] = color
                self.settings.setValue("warn_color", color)
                self.set_color(self.show_warning_background_color_label, color)



    @pyqtSlot()
    def on_cancel_pushButton_clicked(self):
        self.close()

    @pyqtSlot()
    def on_confirm_change_pushButton_clicked(self):

        ui_qss = f'''QLabel{{
    font-size:{self.font.pointSize()};
    font-weight:{self.font.weight()};
    font-family:"{self.font.family()}";
    color:rgb({self.font_color.red()},{self.font_color.green()},{self.font_color.blue()});
}}
QLabel[name="warn_color"]{{
    background:rgb({self.warn_color.red()},{self.warn_color.green()},{self.warn_color.blue()});
}}
QLabel[name="tableSheet"]{{
    border:1px solid #242424;
    background:;
    padding:2px;
}}
QLable[name="font_color"]{{
    background:rgb({self.font_color.red()},{self.font_color.green()},{self.font_color.blue()})
}}
QTableView{{
    selection-background-color:rgb({self.selected_color.red()},{self.selected_color.green()},{self.selected_color.blue()});
}}'''
        with open("ui.qss","w") as f:
            f.write(ui_qss)
        print(ui_qss)
        self.reset_ui()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    loginDialog = FontAndColorDialogControl()
    loginDialog.show()

    sys.exit(app.exec_())
