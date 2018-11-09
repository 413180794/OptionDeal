import json
import pathlib
import ssl
import sys
import logging

import websockets
from quamash import QEventLoop
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from UIControl.dataInteraction import DataInteraction
from UIControl.loginDialogControl import LoginDialogControl
from UIModel.optionInformationModel import OptionInformationModel
from UIView.mainWindow import Ui_MainWindow
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(
    pathlib.Path(__file__).with_name('localhost.pem'))


class MainFormControl(QMainWindow, Ui_MainWindow):
    '''在设计上，我们认为MainFormControl是一个上帝角色，它不仅显示了自己，还可以控制所有的子窗口，我们
    要在这个类中写出控制其他子窗口的函数，以此来达到“最小知识原则” '''
    testSigal = pyqtSignal()
    login_success_signal = pyqtSignal()  # 登录成功信号
    login_failed_signal = pyqtSignal()  # 登录失败信号

    def __init__(self, loop):
        super(MainFormControl, self).__init__()
        self.setupUi(self)
        self.loop = loop
        self.loginDialog = LoginDialogControl(self)
        self.data_interaction_signing_server = DataInteraction(self.loop, self, "wss://localhost:8765")
        self.loginDialog.show()

        # signal
        self.testSigal.connect(self.on_test_signal)
        self.login_success_signal.connect(self.on_login_success_signal)
        self.login_failed_signal.connect(self.on_login_failed_signal)
        #

        # 注意这个六个赋值，原来QTableWidget是没有option_info_obj_list的，这是我强行添加的属性，用于保存每一条信息对象
        # 在on_on_way_for_guest_tableWidget_cellClicked 函数中可以体现出它的好处，方便的取到每一条表格中的数据对象
        self.on_way_for_guest_tableWidget.option_info_obj_list = []
        self.on_way_for_company_tableWidget.option_info_obj_list = []
        self.today_close_for_company_tableWidget.option_info_obj_list = []
        self.today_close_for_guest_tableWidget.option_info_obj_list = []
        self.today_open_for_guest_tableWidget.option_info_obj_list = []
        self.today_open_for_company_tableWidget.option_info_obj_list = []
        self.tab_name_dict = {"对客在途": "on_way_for_guest_tableWidget", "对公在途": "on_way_for_company_tableWidget",
                              "对客今开": "today_open_for_guest_tableWidget", "对公今开": "today_open_for_company_tableWidget",
                              "对客今止": "today_close_for_guest_tableWidget",
                              "对公今止": "today_close_for_company_tableWidget"}

        self.old_option_info_obj = None  # 防止一直在点击同一行，一直在触发函数

        self.test()

        # self.loop.create_task(self.connect_test())

        # self.on_way_for_guest_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # async def connect_test(self):
    #     self.websocket = await websockets.connect("wss://192.168.0.112:8888/traecho")
    def on_login_failed_signal(self):
        '''触发登录失败'''

    def on_login_success_signal(self):
        '''触发登录成功'''
        print("登录成功")
        self.loginDialog.setVisible(False)  # 隐藏登录界面
        self.show()  # 打开主界面

    def send_to_signing_server(self, json):
        '''向签约服务器发送数据'''
        self.data_interaction_signing_server.send_data(json)

    def change_loginDialog_lineedit_empty_label_text(self, text):
        # 改变登录框中红色标签的内容
        self.loginDialog.lineedit_empty_Label.setText(text)

    def if_connect_to_signing_server(self):
        '''判断是否连接到签约服务器'''
        return False if self.data_interaction_signing_server.web_socket is None else True

    def connect_to_signing_server(self):
        '''连接到签约服务器'''
        if self.if_connect_to_signing_server():  # 如果没有连接到签约服务器
            self.data_interaction_signing_server.connect_to_server()

    def test(self):
        tes = OptionInformationModel("S79426", "壹号土猪", "M1901", "认购止盈", 10, 46.4, 4640000, "1809045", 650, 1539273600.0,
                                     730, 1539273600.0, "对客在途", 1000)
        tes.insert_to_table(getattr(self, self.tab_name_dict.get(tes.state)))
        tes1 = OptionInformationModel("S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对公在途", 1000)
        tes1.insert_to_table(getattr(self, self.tab_name_dict.get(tes1.state)))
        tes2 = OptionInformationModel("S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对公今开", 1000)
        tes2.insert_to_table(getattr(self, self.tab_name_dict.get(tes2.state)))
        tes3 = OptionInformationModel("S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对客今开", 1000)
        tes3.insert_to_table(getattr(self, self.tab_name_dict.get(tes3.state)))
        tes4 = OptionInformationModel("S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对公今止", 1000)
        tes4.insert_to_table(getattr(self, self.tab_name_dict.get(tes4.state)))
        tes5 = OptionInformationModel("S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对客今止", 1000)
        tes5.insert_to_table(getattr(self, self.tab_name_dict.get(tes5.state)))
        tes6 = OptionInformationModel("S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对客今止", 1000)
        tes6.insert_to_table(getattr(self, self.tab_name_dict.get(tes6.state)))

    async def hello2(self):
        async with websockets.connect("wss://localhost:8765", ssl=ssl_context) as websocket:
            await websocket.send("name")
            greeting = await websocket.recv()

    # async def hello(self):
    #
    # reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
    # if reply == QMessageBox.Yes:
    #     name = "yes"
    # else:
    #     name = "No"
    # print(name)

    # async with websockets.connect("ws://192.168.0.112:8888/traecho") as websocket:
    # async with websockets.connect("wss://localhost:8765",ssl=ssl_context) as websocket:
    # websocket  = await  websockets.connect("wss://localhost:8765", ssl=ssl_context)
    # await self.websocket.send(json.dumps({"dictate": "询价", "contractCode": "1111"}))
    #
    # # await self.websocket.send(name)
    # # while True:
    # # print(type(json.dumps({"dictate": "询价", "contractCode": "1111"})))
    # # n = 0
    #
    # greeting = await self.websocket.recv()
    #
    # print(f"<{greeting}")
    # # websocket.close()
    # print(type(greeting))

    # await x.close()

    @pyqtSlot()
    def on_evening_up_enquiry_pushButton_clicked(self):
        '''点击平仓询价按钮,进入平仓询价界面,显示相应的数据.
        1.如果界面为空，提示未选中
        2.如果已经选择了相应的期权，进入平仓询价界面，并且将该界面的标签赋值，
            a.transaction_number_label_in_enquiry_page  交易书编号
            b.customer_name_label_in_enquiry_page       客户名称
            c.contract_code_label_in_enquiry_page       合约代码
            d.option_type_label_in_enquiry_page         期权类型
            e.lots_label_in_enquiry_page                手数
            f.number_per_hand_label_in_enquiry_page     每手份数

            g.forward_price_label                       期货价
            h.unit_price_label_in_enquiry_page          平仓单价
            i.total_price_label_in_enquiry_page         总价
            其中a,b,c,d,e,f为控制界面已经存在的数据。
            g,h,i为向签约服务器询价结果
        '''
        if not self.contract_code_label.text():
            loginDialog = LoginDialogControl()
            loginDialog.show()
            loginDialog.raise_()
            # loginDialog.activateWindow()
            return
        # 构造一个包,向签约服务器询价,签约服务判断是否可以询价,如果不可以提示拒绝询价,否则,将询价结果显示在界面中
        # asyncio.run_coroutine_threadsafe(self.enquiry_price_one(),self.loop)
        self.data_interaction.send_data(json.dumps({"purpose": "询价", "contractCode": "1111"}))

    async def enquiry_price_one(self):
        '''询价一次'''
        async with websockets.connect("wss://localhost:8765", ssl=ssl_context) as websocket:
            await websocket.send(json.dumps({"purpose": "询价6", "contractCode": "1111"}))
            enquiry_price_result = await websocket.recv()  # 等待收回复的消息

            enquiry_price_result = json.loads(enquiry_price_result)
            if enquiry_price_result.get("dictate") == "询价":
                self.stackedWidget.setCurrentWidget(self.evening_up_enquiry_page)
                self.unit_price_label_in_enquiry_page.setText(enquiry_price_result.get("contractCode"))
                self.transaction_number_label_in_enquiry_page.setText(self.transaction_number_label.text())
                self.customer_name_label_in_enquiry_page.setText(self.transaction_number_label.text())
                self.contract_code_label_in_enquiry_page.setText(self.contract_code_label.text())
                self.option_type_label_in_enquiry_page.setText(self.option_type_label.text())
                self.lots_label_in_enquiry_page.setText(self.lots_label.text())
                self.number_per_hand_label_in_enquiry_page.setText(self.number_per_hand_label.text())
            else:
                self.testSigal.emit()

    def on_test_signal(self):

        self.loginDialog.show()
        self.loginDialog.raise_()
        self.loginDialog.activateWindow()
        # QMessageBox.information(self, "未选中期权", "未选中期权", QMessageBox.Yes | QMessageBox.No)

    @pyqtSlot()
    def on_cancel_enquiry_pushButton_clicked(self):
        '''点击取消按钮，回到控制页面，如果正在询价，也应该断开盯市询价。目前只是简单的回到控制页面'''
        self.stackedWidget.setCurrentWidget(self.control_module_page)

    def _change_control_module_page(self, option_info_obj):
        '''利用表格中某行数据来修改control_module_page(控制模块)的内容'''
        self.transaction_number_label.setText(str(option_info_obj.transaction_number))
        self.customer_name_label.setText(str(option_info_obj.customer_name))
        self.contract_code_label.setText(str(option_info_obj.contract_code))
        self.option_type_label.setText(str(option_info_obj.option_type))
        self.state_label.setText(str(option_info_obj.state))
        self.total_price_label.setText(str(option_info_obj.total_price))
        self.lots_label.setText(str(option_info_obj.lots))
        self.number_per_hand_label.setText(str(option_info_obj.number_per_hand))
        self.unit_price_label.setText(str(option_info_obj.unit_price))
        self.main_strike_price_label.setText(str(option_info_obj.main_strike_price))
        self.main_exercise_date_label.setText(str(option_info_obj.main_exercise_date))
        self.second_strike_price_label.setText(str(option_info_obj.second_strike_price))
        self.second_exercise_date_label.setText(str(option_info_obj.second_exercise_date))

    @pyqtSlot(int, int)
    def on_on_way_for_guest_tableWidget_cellClicked(self, row, column):
        '''点击表格某一行,修改'''
        option_info_obj = self.on_way_for_guest_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            logger.info(option_info_obj)

    @pyqtSlot(int, int)
    def on_on_way_for_company_tableWidget_cellClicked(self, row, column):
        option_info_obj = self.on_way_for_company_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            logger.info(option_info_obj)

    @pyqtSlot(int, int)
    def on_today_close_for_guest_tableWidget_cellClicked(self, row, column):
        option_info_obj = self.today_close_for_guest_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            logger.info(option_info_obj)

    @pyqtSlot(int, int)
    def on_today_close_for_company_tableWidget_cellClicked(self, row, column):
        option_info_obj = self.today_close_for_guest_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            logger.info(option_info_obj)

    @pyqtSlot(int, int)
    def on_today_open_for_guest_tableWidget_cellClicked(self, row, column):
        option_info_obj = self.today_open_for_guest_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            logger.info(option_info_obj)

    @pyqtSlot(int, int)
    def on_today_open_for_company_tableWidget_cellClicked(self, row, column):
        option_info_obj = self.today_open_for_company_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            logger.info(option_info_obj)


class App(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        loop = QEventLoop(self)
        self.loop = loop

        asyncio.set_event_loop(self.loop)
        self.gui = MainFormControl(self.loop)
        # self.gui.show()
        loop.run_forever()


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # mainwindow = MainFormControl()
    # mainwindow.show()
    # sys.exit(app.exec_())
    # app = QApplication(sys.argv)
    # loop = QEventLoop(app)
    # asyncio.set_event_loop(loop)
    # mainwindow = MainFormControl()
    # mainwindow.show()
    # loop.run_forever()
    App()
