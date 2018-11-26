# -*- coding: utf-8 -*-
# @Time    : 18-10-19 上午10:43
# @Author  : 张帆
# @Site    : 
# @File    : loginDialogControl.py
# @Software: PyCharm
import asyncio
import atexit
import hashlib
import os
import sys

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, qApp
from quamash import QEventLoop

from UIControl.dataInteraction import DataInteraction
from UIControl.mainWindowControl import MainFormControl
from UIModel.loginDialogPropertyModel import LoginDialogPropertyModel
from UIModel.loginFailedModel import LoginFailedModel
from UIModel.loginSuccessModel import LoginSuccessModel
from UIView.loginDialog import Ui_LoginDialog

def findSubStr(substr, str, i):
    count = 0
    while i > 0:
        index = str.find(substr)
        if index == -1:
            return -1
        else:
            str = str[index+1:]
            i -= 1
            count = count + index + 1
    return count - 1

def insert(original, new, pos):
    '''Inserts new inside original at pos.'''
    return original[:pos] + new + original[pos:]

class LoginDialogControl(QDialog, Ui_LoginDialog):
    login_success_signal = pyqtSignal(dict)  # 登录成功信号
    login_failed_signal = pyqtSignal(dict)  # 登录失败信号

    def __init__(self, loop):
        super(LoginDialogControl, self).__init__()

        self.loop = loop
        self.login_success_signal.connect(self.on_login_success_signal)
        self.login_failed_signal.connect(self.on_login_failed_signal)
        self.setupUi(self)
        self.MainForm = MainFormControl(self.loop)
        self.data_interaction_signing_server = DataInteraction(self.loop, self.MainForm, self)
        self.MainForm.data_interaction_signing_server = self.data_interaction_signing_server

    def login_to_signing_server(self, url, port, login_request_json):
        '''登录到到签约服务器'''
        # logger.info("登录到签约服务器-->" + str(self.if_connect_to_signing_server()))
        # print(self.if_connect_to_signing_server())
        index = findSubStr("/",url,3)
        print(index)
        if index != -1:
            url = insert(url, ":"+port, index)
        else:
            url = url + ":" + port
        print(url)
        self.data_interaction_signing_server.connect_to_sever(url, login_request_json)

    @pyqtSlot()
    def on_login_pushButton_clicked(self):
        '''
        点击登录键，做出相应的动作
        :return: 返回空
        '''
        # 如果初始化时候没有建立连接，那么点击登录键的时候再次建立一次
        # self.mainFormControl.connect_to_signing_server() 登录应该由loginDialogPropertyModel做出
        self.lineedit_empty_Label.setText("")
        self.lineedit_empty_Label.repaint()
        loginDialogPropertyModel = LoginDialogPropertyModel(self)
        state = loginDialogPropertyModel.check()
        if state == 1:
            print("无效")

        else:
            # 如果所有的空都有，那么把登录请求发送出去
            # loginDialogPropertyModel.connect_to_server()
            self.login_pushButton.setDisabled(True)
            loginDialogPropertyModel.login()

            self.change_loginDialog_lineedit_empty_label_text("登录中......")
            print("继续")

    def get_user_name(self):
        '''获得登录界面用户名'''
        return self.user_name_LineEdit.text()

    def get_password(self):
        '''获得登录界面密码的md5加密'''
        return hashlib.md5(self.password_LineEdit.text().encode('utf-8')).hexdigest()
    def get_password_real(self):
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

    def on_login_failed_signal(self, json):
        '''触发登录失败'''
        login_failed_model = LoginFailedModel.from_json(self, json)
        # 在登录界面中显示失败的原因
        self.change_loginDialog_lineedit_empty_label_text(login_failed_model.failure_reason)
        self.data_interaction_signing_server.disconnect_to_server()
        self.login_pushButton.setDisabled(False)


    def on_login_success_signal(self, json):
        '''
        触发登录成功,登录成功后,需要做出以下步骤:
            1.关闭登录界面
            2.由发送而来的json数据,构建登录成功模型
                1.该模型对象自动完成动态构建控件
                2.该模型对象自动将userid,lineEdit_dict,dateEdit_dict分配给主控制对象
                    以下四条数据是成功登录以后签约服务器发送而来的, 代表的意思分别是:
                    1.用户id,唯一标识
                    2.主力合约中需要填写的价格,键为该价格中文含义,值为该价格输入框的变量名
                    3.次主力合约中需要填写的价格,键为该价格中文含义,值为该价格输入框的变量名
                    4.需要填写的日期,键为该日期的中文含义,值为该日期输入框的变量名
                    self.userid = None
                    self.main_lineEdit_dict = None
                    self.second_lineEdit_dict = None
                    self.dateEdit_dict = None
        '''
        # self.setVisible(False)  # 隐藏登录界面
        self.close()

        LoginSuccessModel.from_json(self.MainForm, json)  #
        # print(self.userid)
        # print(self.main_lineEdit_dict)
        # print(self.second_lineEdit_dict)
        # print(self.dateEdit_dict)
        self.MainForm.show()  # 打开主界面


class LoginApp(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        loop = QEventLoop(self)
        self.loop = loop

        asyncio.set_event_loop(self.loop)
        self.gui = LoginDialogControl(self.loop)
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
