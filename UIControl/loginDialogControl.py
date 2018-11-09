# -*- coding: utf-8 -*-
# @Time    : 18-10-19 上午10:43
# @Author  : 张帆
# @Site    : 
# @File    : loginDialogControl.py
# @Software: PyCharm
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
        self.mainFormControl.connect_to_signing_server()
        self.lineedit_empty_Label.setText("")
        loginDialogPropertyModel = LoginDialogPropertyModel(user_name=self.user_name_LineEdit.text(),
                                                       password=self.password_LineEdit.text(),
                                                       intranet_server_ip=self.intranet_server_ip_LineEdit.text(),
                                                       intranet_server_port=self.intranet_server_port_LineEdit.text(),
                                                       local_proxy_server_port=self.local_proxy_server_port_LineEdit.text(),
                                                       mainFormControl=self.mainFormControl
                                                       )
        state = loginDialogPropertyModel.check()
        if state == 1:
            return
        else:
            # 如果所有的空都有，那么把登录请求发送出去
            loginDialogPropertyModel.login()
            self.mainFormControl.change_loginDialog_lineedit_empty_label_text("登录中......")
            print("继续")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    loginDialog = LoginDialogControl()
    loginDialog.show()

    sys.exit(app.exec_())
