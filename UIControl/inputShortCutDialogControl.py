# -*- coding: utf-8 -*-
# @Time    : 18-12-14 下午3:07
# @Author  : 张帆
# @Site    : 
# @File    : inputShortCutDialogControl.py
# @Software: PyCharm
from PyQt5.QtCore import QRegExp, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QRegExpValidator, QKeyEvent, QKeySequence
from PyQt5.QtWidgets import QDialog, QKeySequenceEdit

from UIView.inputShortCutDialog import Ui_inputShortCutDialog


class InputShortCutDialogControl(QDialog, Ui_inputShortCutDialog):
    change_set_who_label_signal = pyqtSignal(str)

    def __init__(self, parent):
        super(InputShortCutDialogControl, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowModality(Qt.ApplicationModal)
        self.callback = None
        self.change_set_who_label_signal.connect(self.change_set_who_label)

    def set_callback(self, callback):
        self.callback = callback


    def get_keysequence(self):

        return self.lineEdit.keySequence()


    @pyqtSlot(str)
    def change_set_who_label(self, text):
        self.set_who_label.setText(text)
