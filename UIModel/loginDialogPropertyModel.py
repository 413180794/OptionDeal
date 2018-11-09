# -*- coding: utf-8 -*-
# @Time    : 18-11-2 上午9:41
# @Author  : 张帆
# @Site    : 
# @File    : loginDialogProperty.py
# @Software: PyCharm
import json
import hashlib


class LoginDialogPropertyModel:
    '''该数据模型，完成判断界面输入是否正确。构建客户端登录请求数据包，发送请求'''
    property_to_real_name = {"user_name": "用户名", "password": "密码", "intranet_server_ip": "内网服务器IP地址",
                             "intranet_server_port": "端口号", "local_proxy_server_port": "代理服务器端口号"}

    def __init__(self, user_name: str, password: str, intranet_server_ip: str, intranet_server_port: str,
                 local_proxy_server_port: str, mainFormControl, client_type="transaction", company_name="LOL",
                 temp_password=None, date_due=None):
        self.user_name = user_name
        self.password = password
        self.intranet_server_ip = intranet_server_ip
        self.intranet_server_port = intranet_server_port
        self.local_proxy_server_port = local_proxy_server_port
        self.mainFormControl = mainFormControl
        self.client_type = client_type
        self.company_name = company_name
        self.temp_password = temp_password
        self.date_due = date_due

    def check(self):
        '''检查输入是否符合要求（是否为空）,如果不符合，返回1，否则返回0,注意client_type,company_name,temp_password,date_dute
        不可以为"",否则会显示null不可为空
        '''
        print(self.__dict__)
        count = 0
        for property_name, property_value in self.__dict__.items():
            if property_value == "":
                count += 1
                self.mainFormControl.change_loginDialog_lineedit_empty_label_text(self.property_to_real_name.get(property_name, "null") + "不可为空")
                return count
        else:
            return 0

    def login(self):
        '''向签约服务器发送请求登录ｊｓｏｎ数据包'''
        self.mainFormControl.send_to_signing_server(self.login_request_json())

    def login_request_json(self):
        '''返回登录请求json数据包'''
        return json.dumps(
            {
                "purpose": "login_request",
                "client_type": self.client_type,
                "company_name": self.company_name,
                "user_name": self.user_name,
                "password": hashlib.md5(self.password.encode('utf-8')).hexdigest(),
                "temp_password": hashlib.md5(self.temp_password.encode('utf-8')).hexdigest() if self.temp_password is not None else None,
                "date_due": self.date_due
            }
        )

    def __str__(self):
        return f'''
        user_name:{self.user_name},
        password:{self.password},
        intranet_server_ip:{self.intranet_server_ip},
        intranet_server_port:{self.intranet_server_port},
        local_porxy_server_port:{self.local_proxy_server_port}
        '''
