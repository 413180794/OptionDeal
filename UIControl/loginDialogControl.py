# -*- coding: utf-8 -*-
# @Time    : 18-10-19 上午10:43
# @Author  : 张帆
# @Site    : 
# @File    : loginDialogControl.py
# @Software: PyCharm
import asyncio
import hashlib

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication

from UIModel.loginDialogPropertyModel import LoginDialogPropertyModel
from UIView.loginDialog import Ui_LoginDialog


class LoginDialogControl(QDialog, Ui_LoginDialog):
    def __init__(self, mainFormControl):
        super(LoginDialogControl, self).__init__()
        self.mainFormControl = mainFormControl
        self.setupUi(self)

    @pyqtSlot()
    def on_login_pushButton_clicked(self):
        '''
        点击登录键，做出相应的动作
        :return: 返回空
        '''

         # 如果初始化时候没有建立连接，那么点击登录键的时候再次建立一次
        # self.mainFormControl.connect_to_signing_server() 登录应该由loginDialogPropertyModel做出
        self.lineedit_empty_Label.setText("")
        loginDialogPropertyModel = LoginDialogPropertyModel(self)
        state = loginDialogPropertyModel.check()
        if state == 1:
            return
        else:
            # 如果所有的空都有，那么把登录请求发送出去
            # loginDialogPropertyModel.connect_to_server()
            loginDialogPropertyModel.login()

            self.change_loginDialog_lineedit_empty_label_text("登录中......")
            print("继续")

    def get_user_name(self):
        '''获得登录界面用户名'''
        return self.user_name_LineEdit.text()

    def get_password(self):
        '''获得登录界面密码的md5加密'''
        return hashlib.md5(self.password_LineEdit.text().encode('utf-8')).hexdigest()

    def get_intranet_server_ip(self):
        return self.intranet_server_ip_LineEdit.text()

    def get_intranet_server_port(self):
        return self.intranet_server_port_LineEdit.text()

    def get_local_proxy_server_port(self):
        return self.local_proxy_server_port_LineEdit.text()

    def change_loginDialog_lineedit_empty_label_text(self, text):
        # 改变登录框中红色标签的内容
        self.lineedit_empty_Label.setText(text)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    loginDialog = LoginDialogControl()
    loginDialog.show()

    sys.exit(app.exec_())
