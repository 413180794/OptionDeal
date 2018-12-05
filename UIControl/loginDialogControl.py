# -*- coding: utf-8 -*-
# @Time    : 18-10-19 上午10:43
# @Author  : 张帆
# @Site    : 
# @File    : loginDialogControl.py
# @Software: PyCharm
import asyncio
import atexit
import hashlib
import json
import os
import sys

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog, QApplication, qApp
from quamash import QEventLoop


from UIControl.tool import get_password_md5

from UIView.loginDialog import Ui_LoginDialog


class LoginDialogControl(QDialog, Ui_LoginDialog):

    disconnect_signal = pyqtSignal()
    def __init__(self, client_type, login_to_signing_server,parent):
        super(LoginDialogControl, self).__init__(parent)

        self.setupUi(self)
        self.client_type = client_type

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.login_to_signing_server = login_to_signing_server

    @pyqtSlot()
    def on_login_pushButton_clicked(self):
        '''
        点击登录键，做出相应的动作
        :return: 返回空
        '''
        # 如果初始化时候没有建立连接，那么点击登录键的时候再次建立一次
        # self.mainFormControl.connect_to_signing_server() 登录应该由loginDialogPropertyModel做出
        self.lineedit_empty_Label.setText("")
        self.user_name = self.get_user_name()
        password = self.get_password()
        intranet_server_ip = self.get_intranet_server_ip()
        intranet_server_port = self.get_intranet_server_port()
        local_proxy_server_port = self.get_local_proxy_server_port()

        if not self.user_name:
            self.lineedit_empty_Label.setText("用户名不可为空")
        elif not password:
            self.lineedit_empty_Label.setText("密码不可为空")
        elif not intranet_server_ip:
            self.lineedit_empty_Label.setText("内网服务器IP地址不可为空")
        elif not intranet_server_port:
            self.lineedit_empty_Label.setText("端口号不可为空")
        elif not local_proxy_server_port:
            self.lineedit_empty_Label.setText("代理服务器端口号不可为空")
        else:
            # 如果所有的空都有，那么把登录请求发送出去
            # loginDialogPropertyModel.connect_to_server()
            self.login_pushButton.setDisabled(True)

            self.login_to_signing_server(intranet_server_ip, intranet_server_port, json.dumps(
                {
                    "purpose": "login_request",
                    "client_type": self.client_type,
                    "user_name": self.user_name,
                    "password": get_password_md5(password),
                }
            ))

            self.lineedit_empty_Label.setText("登录中......")

    def get_user_name(self):
        '''获得登录界面用户名'''
        return self.user_name_LineEdit.text()

    def get_password(self):
        '''获得登录界面密码的md5加密'''
        return self.password_LineEdit.text()

    def get_intranet_server_ip(self):
        return self.intranet_server_ip_LineEdit.text()

    def get_intranet_server_port(self):
        return self.intranet_server_port_LineEdit.text()

    def get_local_proxy_server_port(self):
        return self.local_proxy_server_port_LineEdit.text()

    def change_loginDialog_lineedit_empty_label_text(self, text):
        # 改变登录框中红色标签的内容
        self.lineedit_empty_Label.setText(text)
        '''
        通过立即调用paintEvent()来直接重新绘制窗口部件，如果erase为真，Qt在paintEvent()调用之前擦除区域(x,y,w,h)。 
        如果w是负数，它被width()-x替换，并且如果h是负数，它被height()-y替换。 如果你需要立即重新绘制，建议使用repaint()，
        '''
        self.lineedit_empty_Label.repaint()




class LoginApp(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        loop = QEventLoop(self)
        self.loop = loop

        asyncio.set_event_loop(self.loop)
        self.gui = LoginDialogControl()
        self.gui.show()
        exit_code = self.exec_()
        if exit_code == 888:
            self.restart_program()
        else:
            sys.exit()

        loop.run_forever()

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    # url = 'ws://39.96.20.147:8000/ws/OptionsFuturesTradingPlatform/ll/'
    #
    # x = findSubStr("/",url,3)
    # print(url)
    # x = insert(url,":8000",x)
    # print(x)
    LoginApp()
