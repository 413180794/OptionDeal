# -*- coding: utf-8 -*-
# @Time    : 18-11-8 下午3:03
# @Author  : 张帆
# @Site    : 
# @File    : dataInteraction.py
# @Software: PyCharm
import asyncio
import concurrent
import json
import logging
import pathlib
import socket
import ssl

import websockets

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("main_log.txt")
handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# ssl_context.load_verify_locations(
#     pathlib.Path(__file__).with_name('localhost.pem'))

'''
登录流程
    1.用户填写登录框信息
    2.点击登陆按钮 -- > on_login_pushButton_clicked()
        1.登录框中登录状态修改为""
        2.实例化登录属性(loginDialogPropertyModel)
        3.调用上述对象的check()方法，检查登录框中输入框是否符合要求-->不可为空
            1.如果为空，提示该输入框为空，并返回1
            2.如果不为空，返回0
        4.如果check()方法返回1，结束该函数
        5.如果check()方法返回0,调用上述对象login()方法
            1.调用登录框控制器中函数向服务器发送登录文件
            2.等待接收登录结果
            3.登录失败、超时、连接中断都会造成界面显示错误信息
        6.如果登录成功，打开主界面
        7.如果登录失败，显示失败原因，并与服务器断开连接，如果不断开连接，客户端将会持续接收服务器信息
'''


class DataInteraction:
    def __init__(self, loop, mainFormControl):
        self.loop = loop
        self.mainFormControl = mainFormControl
        self.web_socket = None
        self.url = None
        self.json = None
        # self.loop.create_task(self.data_receive())

        # asyncio.ensure_future(self.connect_to_server())  # 连接到服务器

    def connect_to_sever(self, url, login_request_json=None):
        self.url = url
        print(login_request_json)
        self.json = login_request_json
        self.loop.create_task(self._connect_to_server())

    def disconnect_to_server(self):
        ''''''

        asyncio.ensure_future(self.web_socket.close())

    async def _connect_to_server(self):
        try:
            # 有可能连接不上
            self.web_socket = await asyncio.wait_for(websockets.connect(self.url), timeout=10)

        except ConnectionRefusedError as e:
            # 如果连接被拒绝登录界面应该做出响应
            self.mainFormControl.login_pushButton_setDisabled_signal.emit(False)
            self.mainFormControl.set_loginDialog_text_signal.emit("无法连接服务器")
            logger.warning(e)
        except websockets.exceptions.InvalidURI as e:
            self.mainFormControl.login_pushButton_setDisabled_signal.emit(False)
            self.mainFormControl.set_loginDialog_text_signal.emit("无效的地址")
            logger.warning(e)
        except socket.gaierror as e:
            elf.mainFormControl.login_pushButton_setDisabled_signal.emit(False)
            self.mainFormControl.set_loginDialog_text_signal.emit("未知的名称或服务")
        except ssl.SSLError as e:
            logger.warning(e)
            elf.mainFormControl.login_pushButton_setDisabled_signal.emit(False)
            self.mainFormControl.set_loginDialog_text_signal.emit("错误的SSL证书")
        except ValueError as e:
            logger.error(e)
            elf.mainFormControl.login_pushButton_setDisabled_signal.emit(False)
            self.mainFormControl.set_loginDialog_text_signal.emit("端口号范围为0-65535")
        except concurrent.futures._base.TimeoutError as e:
            logger.warning(e)
            elf.mainFormControl.login_pushButton_setDisabled_signal.emit(False)
            self.mainFormControl.set_loginDialog_text_signal.emit("连接超时")
        except ConnectionResetError as e:
            logger.warning(e)
            self.mainFormControl.login_pushButton_setDisabled_signal.emit(False)
            self.mainFormControl.set_loginDialog_text_signal.emit("连接被对方重设")
        else:
            # 连接上以后发送一个登录请求
            print(self.json)
            if self.json is not None:
                await self._send_data(self.json)  # 发送完毕以后才执行等待接收数据
                try:

                    receive_data = await asyncio.wait_for(self.web_socket.recv(), timeout=10)
                    receive_data = json.loads(receive_data)
                    purpose = receive_data.get("purpose", None)
                    getattr(self.mainFormControl, purpose + "_signal").emit(receive_data)
                except concurrent.futures._base.TimeoutError as e:
                    '''10秒后还没有收到数据'''
                    logger.info(e)
                    self.mainFormControl.login_pushButton_setDisabled_signal.emit("网络超时")
                    self.mainFormControl.set_loginDialog_text_signal.setDisabled(False)
                except websockets.exceptions.ConnectionClosed as e:
                    elf.mainFormControl.login_pushButton_setDisabled_signal.emit("连接已经断开")
                    self.mainFormControl.set_loginDialog_text_signal.setDisabled(False)
                else:
                    await self._data_receive()  # 连接后开始等待数据

    async def _data_receive(self):
        while True:
            try:
                receive_data = await self.web_socket.recv()
                print(receive_data)
            except AttributeError as e:
                logger.warning(e)
                break
            except websockets.exceptions.ConnectionClosed as e:
                print("已经断开", self.web_socket.closed)

                logger.warning(e)
                # 断开后，提示断开连接

                break
            else:
                receive_data = json.loads(receive_data)  # 收到的json消息
                purpose = receive_data.get("purpose", None)  # 判断该包的作用
                # 根据purpose 发送相应的信号给主控制
                try:
                    getattr(self.mainFormControl, purpose + "_signal").emit(receive_data)
                except AttributeError as e:
                    logger.error(e)

    def send_data(self, data):
        self.loop.create_task(self._send_data(data))
        # asyncio.wait_for(self._send_data(data),timeout=10,loop=self.loop)

    async def _send_data(self, data):
        '''向其发送数据'''
        print("self.web_socket:", self.web_socket.closed)
        if self.web_socket.closed:  # 如果连接已经断开了,那么重新连接
            await self._connect_to_server()

        print("发送数据", data)
        try:
            await asyncio.wait_for(self.web_socket.send(data), timeout=10)
        except concurrent.futures._base.TimeoutError as e:
            # 如果10秒还没有将这个数据发送出去.则肯定出问题了.我们可以根据这个data来判断什么包没有发出去,以此来做出相应
            print(e)
