# -*- coding: utf-8 -*-
# @Time    : 18-11-29 上午9:44
# @Author  : 张帆
# @Site    : 
# @File    : setTempSecretDialogControl.py
# @Software: PyCharm
import json

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox

from UIControl.tool import get_password_md5, str_to_time_stamp
from UIView.setTempSecretDialog import Ui_setTempSecretDialog


class SetTempSecretDialogControl(QDialog, Ui_setTempSecretDialog):
    set_temp_password_failed_signal = pyqtSignal(dict)
    set_temp_password_success_signal = pyqtSignal(dict)
    def __init__(self, client_type, user_name, send_to_server,parent):
        super(SetTempSecretDialogControl, self).__init__(parent)
        self.setupUi(self)
        self.client_type = client_type
        self.user_name = user_name
        self.userid = self.user_name + "_" + self.client_type
        self.send_to_server = send_to_server

        self.set_temp_password_failed_signal.connect(self.on_set_temp_password_failed_signal)
        self.set_temp_password_success_signal.connect(self.on_set_temp_password_success_signal)

    @pyqtSlot(dict)
    def on_set_temp_password_failed_signal(self,json):
        QMessageBox.critical(self, "修改失败",
                             self.tr(json['failure_reason']))
    @pyqtSlot(dict)
    def on_set_temp_password_success_signal(self,json):
        QMessageBox.information(self, "修改成功", "修改成功")

    @pyqtSlot()
    def on_submit_pushButton_clicked(self):
        temp_password = self.temp_password_LineEdit.text()
        temp_password_again = self.temp_password_again_LineEdit.text()
        old_password = self.old_password_LineEdit.text()
        valid_time = self.valid_time_dateEdit.text()
        if temp_password != temp_password_again:
            # 如果两次输入的密码不同
            QMessageBox.critical(self, "错误!", "两次输入密码不相同!")
            return
        else:
            msg_json = json.dumps({
                "purpose": "set_temp_password",
                "user_name": self.user_name,
                "temp_password": get_password_md5(temp_password),
                "password": get_password_md5(old_password),
                "valid_time": str_to_time_stamp(valid_time),
                "client_type": self.client_type,
                "userid": self.userid
            })
        self.send_to_server(msg_json)
