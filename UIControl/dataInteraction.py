# -*- coding: utf-8 -*-
# @Time    : 18-11-8 下午3:03
# @Author  : 张帆
# @Site    : 
# @File    : dataInteraction.py
# @Software: PyCharm
import asyncio
import json
import pathlib
import ssl

import websockets

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(
    pathlib.Path(__file__).with_name('localhost.pem'))


class DataInteraction:
    def __init__(self, loop, mainFormControl, url):
        self.loop = loop
        self.mainFormControl = mainFormControl
        self.web_socket = None
        self.url = url
        self.connect_to_server()

        # self.loop.create_task(self.data_receive())

        # asyncio.ensure_future(self.connect_to_server())  # 连接到服务器

    def connect_to_server(self):
        self.loop.create_task(self._connect_to_server(self.url))

    async def _connect_to_server(self, url):
        try:
            # 有可能连接不上
            self.web_socket = await websockets.connect(url, ssl=ssl_context)
        except ConnectionRefusedError as e:
            # 如果连接被拒绝登录界面应该做出响应
            self.mainFormControl.change_loginDialog_lineedit_empty_label_text("无法连接服务器")
            # self.mainForm.loginDialog.lineedit_empty_Label.setText("无法连接服务器")
            print(e)
        else:
            await self.data_receive()  # 连接后开始等待后数据

    async def data_receive(self):
        while True:
            try:
                receive_data = await self.web_socket.recv()
                receive_data = json.loads(receive_data)  # 收到的json消息
                print(receive_data)
                purpose = receive_data.get("purpose", None)  # 判断该包的作用
                print(purpose)
                # 根据purpose 发送相应的信号给主控制
                getattr(self.mainFormControl,purpose+"_signal").emit()
            except AttributeError as e:
                print(e)

    def send_data(self, data):
        if self.web_socket is None:
            # 如果没有连接到服务器
            self.connect_to_server()
        self.loop.create_task(self._send_data(data))

    async def _send_data(self, data):
        '''向其发送数据'''
        await self.web_socket.send(data)
