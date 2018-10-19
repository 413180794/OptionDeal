# -*- coding: utf-8 -*-
# @Time    : 18-10-19 上午10:43
# @Author  : 张帆
# @Site    : 
# @File    : loginDialogControl.py
# @Software: PyCharm
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication

from UIpy.loginDialog import Ui_dialog


class LoginDialogControl(QDialog, Ui_dialog):
    def __init__(self):
        super(LoginDialogControl, self).__init__()
        self.setupUi(self)

    @pyqtSlot()
    def on_login_pushButton_clicked(self):
        '''
        点击登录键，做出相应的动作
        :return: 返回空
        '''
        self.lineedit_empty_Label.setText("")
        loginDialogProperty = LoginDialogProperty(user_name=self.user_name_LineEdit.text(),
                                                  password=self.password_LineEdit.text(),
                                                  intranet_server_ip=self.intranet_server_ip_LineEdit.text(),
                                                  intranet_server_port=self.intranet_server_port_LineEdit.text(),
                                                  local_proxy_server_port=self.local_proxy_server_port_LineEdit.text()
                                                  )
        state = loginDialogProperty.check(self)
        if state == 1:
            return
        else:
            print("继续")


class LoginDialogProperty:
    property_to_real_name = {"user_name": "用户名", "password": "密码", "intranet_server_ip": "内网服务器IP地址",
                             "intranet_server_port":"端口号","local_proxy_server_port":"代理服务器端口号"}

    def __init__(self, user_name: str, password: str, intranet_server_ip: str, intranet_server_port: str,
                 local_proxy_server_port: str):
        self.user_name = user_name
        self.password = password
        self.intranet_server_ip = intranet_server_ip
        self.intranet_server_port = intranet_server_port
        self.local_proxy_server_port = local_proxy_server_port

    def check(self, dialog: LoginDialogControl):
        '''检查输入是否符合要求（是否为空）,如果为空，返回该属性的值和属性名'''
        # print(self.__dict__)
        count = 0
        for property_name, property_value in self.__dict__.items():
            if property_value == "":
                count+=1
                dialog.lineedit_empty_Label.setText(self.property_to_real_name.get(property_name,"null")+"不可为空")
                return count
        else:
            return 0

    def __str__(self):
        return f'''
        user_name:{self.user_name},
        password:{self.password},
        intranet_server_ip:{self.intranet_server_ip},
        intranet_server_port:{self.intranet_server_port},
        local_porxy_server_port:{self.local_proxy_server_port}
        '''


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    loginDialog = LoginDialogControl()
    loginDialog.show()

    sys.exit(app.exec_())
