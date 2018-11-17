# -*- coding: utf-8 -*-
# @Time    : 18-11-8 下午3:03
# @Author  : 张帆
# @Site    : 
# @File    : dataInteraction.py
# @Software: PyCharm
import asyncio
import json
import logging
import pathlib
import socket
import ssl

import websockets


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("main_log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(
    pathlib.Path(__file__).with_name('localhost.pem'))


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
        self.json = login_request_json
        self.loop.create_task(self._connect_to_server())
    def disconnect_to_server(self):
        ''''''

        asyncio.ensure_future(self.web_socket.close())
    async def _connect_to_server(self):
        try:
            # 有可能连接不上

            self.web_socket = await websockets.connect(self.url, ssl=ssl_context,timeout=10)
        except ConnectionRefusedError as e:
            # 如果连接被拒绝登录界面应该做出响应
            self.mainFormControl.change_loginDialog_lineedit_empty_label_text("无法连接服务器")
            # self.mainForm.loginDialog.lineedit_empty_Label.setText("无法连接服务器")
            logger.warning(e)
        except websockets.exceptions.InvalidURI as e:
            self.mainFormControl.change_loginDialog_lineedit_empty_label_text("无效的地址")
            logger.warning(e)
        except socket.gaierror as e:
            self.mainFormControl.change_loginDialog_lineedit_empty_label_text("未知的名称或服务")
        else:
            # 连接上以后发送一个登录请求
            if self.json is not None:
                await self._send_data(self.json) # 发送完毕以后才执行等待接收数据

            await self._data_receive()  # 连接后开始等待数据

    async def _data_receive(self):
        while True:
            try:
                receive_data = await self.web_socket.recv()
            except AttributeError as e:
                logger.warning(e)
                break
            except websockets.exceptions.ConnectionClosed as e:
                print("已经断开",self.web_socket.closed)
                logger.warning(e)
                break
            else:
                receive_data = json.loads(receive_data)  # 收到的json消息
                purpose = receive_data.get("purpose", None)  # 判断该包的作用
                # 根据purpose 发送相应的信号给主控制
                getattr(self.mainFormControl,purpose+"_signal").emit(receive_data)
    def send_data(self, data):
        self.loop.create_task(self._send_data(data))

    async def _send_data(self, data):
        '''向其发送数据'''
        print("self.web_socket:",self.web_socket)
        if self.web_socket.closed:# 如果连接已经断开了,那么重新连接
            await self._connect_to_server()
        else:
            print("发送数据")
            await self.web_socket.send(data)
