# -*- coding: utf-8 -*-
# @Time    : 18-12-14 下午2:49
# @Author  : 张帆
# @Site    : 
# @File    : shortCutSetDialogControl.py
# @Software: PyCharm
from PyQt5.QtCore import pyqtSlot, Qt, QSettings, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QMessageBox

from UIControl.inputShortCutDialogControl import InputShortCutDialogControl
from UIView.shortCutSetDialog import Ui_shortCutDialog


class ShortCutSetDialogControl(QDialog, Ui_shortCutDialog):
    reset_shortcut_signal = pyqtSignal()
    def __init__(self, parent):
        super(ShortCutSetDialogControl, self).__init__(parent)
        self.setupUi(self)
        # self.setAttribute(Qt.WA_DeleteOnClose)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.shortcut_settings = QSettings("short_cut")
        self.input_short_cut_dialog_control = InputShortCutDialogControl(self)
        self.key_seq_list = [None] * 16
        self.move_right_label.setText(QKeySequence(Qt.ALT + Qt.Key_Space).toString())
        self.switch_behind_label.setText(QKeySequence(Qt.ALT + Qt.Key_Down).toString())
        self.switch_front_label.setText(QKeySequence(Qt.ALT + Qt.Key_Up).toString())
        self.hide_detail_company_label.setText(QKeySequence(Qt.ALT + Qt.Key_Z).toString())
        #
        self.sell_new_option_label.setText(QKeySequence(Qt.CTRL + Qt.Key_Insert).toString())
        self.this_module_confirm_label.setText(QKeySequence(Qt.CTRL + Qt.Key_Enter).toString())
        self.add_price_label.setText(QKeySequence(Qt.CTRL + Qt.Key_PageUp).toString())
        self.recove_price_label.setText(QKeySequence(Qt.CTRL + Qt.Key_Home).toString())

        # self.show_hide_detail_seq = self.shortcut_settings.value("show_hide_detail")
        # if self.show_hide_detail_seq:
        #     self.show_hide_detail_label.setText(self.show_hide_detail_seq)
        #
        # self.show_hide_company_seq = self.shortcut_settings.value("show_hide_company")
        # if self.show_hide_company_seq:
        #     self.show_hide_company_label.setText(self.show_hide_company_seq)
        #
        # self.page_down_seq = self.shortcut_settings.value("page_down")
        # if self.page_down_seq:
        #     self.page_down_label.setText(self.page_down_seq)
        #
        # self.page_up_seq = self.shortcut_settings.value("page_up")
        # if self.page_up_seq:
        #     self.page_up_label.setText(self.page_up_seq)
        #
        # self.location_up_seq = self.shortcut_settings.value("location_up")
        # if self.location_up_seq:
        #     self.location_up_label.setText(self.location_up_seq)
        #
        # self.location_right_seq = self.shortcut_settings.value("location_right")
        # if self.location_right_seq:
        #     self.location_right_label.setText(self.location_right_seq)
        #
        # self.location_left_seq = self.shortcut_settings.value("location_left")
        # if self.location_left_seq:
        #     self.location_left_label.setText(self.location_left_seq)
        #
        # self.location_down_seq = self.shortcut_settings.value("location_down")
        # if self.location_down_seq:
        #     self.location_down_label.setText(self.location_down_seq)
        self.show_hide_detail_seq = None
        self.show_hide_company_seq = None
        self.page_down_seq = None
        self.page_up_seq =None
        self.location_up_seq = None
        self.location_right_seq = None
        self.location_left_seq = None
        self.location_down_seq = None

    def set_seq(self):
        # self.move_right_label.setText(QKeySequence(Qt.ALT + Qt.Key_Tab).toString())
        # self.switch_behind_label.setText(QKeySequence(Qt.ALT + Qt.Key_Down).toString())
        # self.switch_front_label.setText(QKeySequence(Qt.ALT + Qt.Key_Up).toString())
        # self.hide_detail_company_label.setText(QKeySequence(Qt.ALT + Qt.Key_Z).toString())
        # #
        # self.sell_new_option_label.setText(QKeySequence(Qt.CTRL + Qt.Key_Insert).toString())
        # self.this_module_confirm_label.setText(QKeySequence(Qt.CTRL + Qt.Key_Enter).toString())
        # self.add_price_label.setText(QKeySequence(Qt.CTRL + Qt.Key_PageUp).toString())
        # self.recove_price_label.setText(QKeySequence(Qt.CTRL + Qt.Key_Home).toString())

        self.show_hide_detail_seq = QKeySequence(self.shortcut_settings.value("show_hide_detail"))

        if self.show_hide_detail_seq:

            self.show_hide_detail_label.setText(self.show_hide_detail_seq.toString())

        self.show_hide_company_seq = QKeySequence(self.shortcut_settings.value("show_hide_company"))
        if self.show_hide_company_seq:
            self.show_hide_company_label.setText(self.show_hide_company_seq.toString())

        self.page_down_seq = QKeySequence(self.shortcut_settings.value("page_down"))
        if self.page_down_seq:
            self.page_down_label.setText(self.page_down_seq.toString())

        self.page_up_seq = QKeySequence(self.shortcut_settings.value("page_up"))
        if self.page_up_seq:
            self.page_up_label.setText(self.page_up_seq.toString())

        self.location_up_seq = QKeySequence(self.shortcut_settings.value("location_up"))
        if self.location_up_seq:
            self.location_up_label.setText(self.location_up_seq.toString())

        self.location_right_seq = QKeySequence(self.shortcut_settings.value("location_right"))
        if self.location_right_seq:
            self.location_right_label.setText(self.location_right_seq.toString())

        self.location_left_seq = QKeySequence(self.shortcut_settings.value("location_left"))
        if self.location_left_seq:

            self.location_left_label.setText(self.location_left_seq.toString())

        self.location_down_seq = QKeySequence(self.shortcut_settings.value("location_down"))
        if self.location_down_seq:

            self.location_down_label.setText(self.location_down_seq.toString())

        self.key_seq_list = [QKeySequence(Qt.ALT + Qt.Key_Tab), QKeySequence(Qt.ALT + Qt.Key_Down),
                             QKeySequence(Qt.ALT + Qt.Key_Up), self.show_hide_detail_seq, self.show_hide_company_seq,
                             QKeySequence(Qt.ALT + Qt.Key_Z), self.page_down_seq, self.page_up_seq,
                             self.location_up_seq, self.location_right_seq, self.location_left_seq,
                             self.location_down_seq, QKeySequence(Qt.CTRL + Qt.Key_Insert),
                             QKeySequence(Qt.CTRL + Qt.Key_Enter), QKeySequence(Qt.CTRL + Qt.Key_PageUp),
                             QKeySequence(Qt.CTRL + Qt.Key_Home)]
    @pyqtSlot()
    def on_show_hide_detail_toolButton_clicked(self):
        ''''''
        self.input_short_cut_dialog_control.change_set_who_label_signal.emit("显/隐明细")
        self.input_short_cut_dialog_control.lineEdit.setFocus()
        self.input_short_cut_dialog_control.exec_()
        key_seq = self.input_short_cut_dialog_control.get_keysequence()
        self.input_short_cut_dialog_control.lineEdit.clear()
        if key_seq:
            if key_seq in self.key_seq_list:
                QMessageBox.warning(self, "错误", "快捷键不可重复")
                return
            else:
                self.key_seq_list[3] = key_seq
                # self.shortcut_settings.setValue("show_hide_detail", key_seq)
                self.show_hide_detail_label.setText(key_seq.toString())

    @pyqtSlot()
    def on_show_hide_company_toolButton_clicked(self):
        ''''''
        self.input_short_cut_dialog_control.change_set_who_label_signal.emit("显/隐对公")
        self.input_short_cut_dialog_control.lineEdit.setFocus()
        self.input_short_cut_dialog_control.exec_()
        key_seq = self.input_short_cut_dialog_control.get_keysequence()
        self.input_short_cut_dialog_control.lineEdit.clear()
        if key_seq:
            if key_seq in self.key_seq_list:
                QMessageBox.warning(self, "错误", "快捷键不可重复")
                return
            else:
                self.key_seq_list[4] = key_seq
                # self.shortcut_settings.setValue("show_hide_company", key_seq)
                self.show_hide_company_label.setText(key_seq.toString())

    @pyqtSlot()
    def on_page_down_toolButton_clicked(self):
        ''''''
        self.input_short_cut_dialog_control.change_set_who_label_signal.emit("向下翻页")
        self.input_short_cut_dialog_control.lineEdit.setFocus()
        self.input_short_cut_dialog_control.exec_()
        key_seq = self.input_short_cut_dialog_control.get_keysequence()
        self.input_short_cut_dialog_control.lineEdit.clear()
        if key_seq:
            if key_seq in self.key_seq_list:
                QMessageBox.warning(self, "错误", "快捷键不可重复")
                return
            else:
                self.key_seq_list[6] = key_seq
                # self.shortcut_settings.setValue("page_down", key_seq)
                self.page_down_label.setText(key_seq.toString())

    @pyqtSlot()
    def on_page_up_toolButton_clicked(self):
        ''''''
        self.input_short_cut_dialog_control.change_set_who_label_signal.emit("向上翻页")
        self.input_short_cut_dialog_control.lineEdit.setFocus()
        self.input_short_cut_dialog_control.exec_()
        key_seq = self.input_short_cut_dialog_control.get_keysequence()
        self.input_short_cut_dialog_control.lineEdit.clear()
        if key_seq:
            if key_seq in self.key_seq_list:
                QMessageBox.warning(self, "错误", "快捷键不可重复")
                return
            else:
                self.key_seq_list[7] = key_seq
                # self.shortcut_settings.setValue("page_up", key_seq)
                self.page_up_label.setText(key_seq.toString())
    @pyqtSlot()
    def on_location_up_toolButton_clicked(self):
        ''''''
        self.input_short_cut_dialog_control.change_set_who_label_signal.emit("定位最上")
        self.input_short_cut_dialog_control.lineEdit.setFocus()
        self.input_short_cut_dialog_control.exec_()
        key_seq = self.input_short_cut_dialog_control.get_keysequence()
        self.input_short_cut_dialog_control.lineEdit.clear()
        if key_seq:
            if key_seq in self.key_seq_list:
                QMessageBox.warning(self, "错误", "快捷键不可重复")
                return
            else:
                self.key_seq_list[8] = key_seq
                # self.shortcut_settings.setValue("location_up", key_seq)
                self.location_up_label.setText(key_seq.toString())
    @pyqtSlot()
    def on_location_down_toolButton_clicked(self):
        ''''''
        self.input_short_cut_dialog_control.change_set_who_label_signal.emit("定位最下")
        self.input_short_cut_dialog_control.lineEdit.setFocus()
        self.input_short_cut_dialog_control.exec_()
        key_seq = self.input_short_cut_dialog_control.get_keysequence()
        self.input_short_cut_dialog_control.lineEdit.clear()
        if key_seq:
            if key_seq in self.key_seq_list:
                QMessageBox.warning(self, "错误", "快捷键不可重复")
                return
            else:
                self.key_seq_list[9] = key_seq
                print(key_seq)
                # self.shortcut_settings.setValue("location_down",key_seq)
                self.location_down_label.setText(key_seq.toString())

    @pyqtSlot()
    def on_location_left_toolButton_clicked(self):
        ''''''
        self.input_short_cut_dialog_control.change_set_who_label_signal.emit("定位最左")
        self.input_short_cut_dialog_control.lineEdit.setFocus()
        self.input_short_cut_dialog_control.exec_()
        key_seq = self.input_short_cut_dialog_control.get_keysequence()
        self.input_short_cut_dialog_control.lineEdit.clear()
        if key_seq:
            if key_seq in self.key_seq_list:
                QMessageBox.warning(self, "错误", "快捷键不可重复")
                return
            else:
                self.key_seq_list[10] = key_seq
                # self.shortcut_settings.setValue("location_left", key_seq)
                self.location_left_label.setText(key_seq.toString())

    @pyqtSlot()
    def on_location_right_toolButton_clicked(self):
        ''''''
        self.input_short_cut_dialog_control.change_set_who_label_signal.emit("定位最右")
        self.input_short_cut_dialog_control.lineEdit.setFocus()
        self.input_short_cut_dialog_control.exec_()
        key_seq = self.input_short_cut_dialog_control.get_keysequence()
        self.input_short_cut_dialog_control.lineEdit.clear()
        if key_seq:
            if key_seq in self.key_seq_list:
                QMessageBox.warning(self, "错误", "快捷键不可重复")
                return
            else:
                self.key_seq_list[11] = key_seq
                # self.shortcut_settings.setValue("location_right", key_seq)
                self.location_right_label.setText(key_seq.toString())

    def accept(self):
        print(self.key_seq_list)
        self.shortcut_settings.setValue("show_hide_detail", self.key_seq_list[3])
        self.shortcut_settings.setValue("show_hide_company", self.key_seq_list[4])
        self.shortcut_settings.setValue("page_down", self.key_seq_list[6])
        self.shortcut_settings.setValue("page_up", self.key_seq_list[7])
        self.shortcut_settings.setValue("location_up", self.key_seq_list[8])
        self.shortcut_settings.setValue("location_down", self.key_seq_list[9])
        self.shortcut_settings.setValue("location_left", self.key_seq_list[10])
        self.shortcut_settings.setValue("location_right", self.key_seq_list[11])
        # 接下来 要那拿着这些设置去配置快捷键
        self.reset_shortcut_signal.emit()
        super(ShortCutSetDialogControl, self).accept()









if __name__ == '__main__':
    x = QKeySequence(Qt.CTRL + Qt.Key_Insert)
    y = QKeySequence(Qt.CTRL + Qt.Key_Insert)
    print(x == y)
    print(str(x))
    print(x.toString())
