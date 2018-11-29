import collections
import json
import pathlib
import ssl
import sys
import logging
import time

import websockets
from PyQt5 import QtGui, QtCore, QtWidgets
from quamash import QEventLoop
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QModelIndex
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel, QDialog, qApp

from UIControl.resetSecretDialogControl import ResetSecretDialogControl
from UIControl.setTempSecretDialogControl import SetTempSecretDialogControl
from UIModel.chatMessageModel import ChatMessageModel
from UIModel.chatReqMsgModel import ChatReqMsgModel
from UIModel.enquiryFeasibilityRequestModel import EnquiryFeasibilityRequestModel

from UIModel.optionEssentialInfoModel import OptionEssentialInfoModel
from UIModel.optionInformationModel import OptionInformationModel
from UIModel.requestEssentialInfoModel import RequestEssentialInfoModel
from UIModel.updateUsersInfoModel import UpdateUsersInfoModel
from UIView.mainWindow import Ui_MainWindow
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("main_log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# ssl_context.load_verify_locations(
#     pathlib.Path(__file__).with_name('localhost.pem'))

widget_name_lineEdit = {"行权价": "strike_price_lineEdit", "向下止盈": "target_profit_lineEdit"}
time_widget_name = {"最近到期日": "date_due"}


class MainFormControl(QMainWindow, Ui_MainWindow):
    testSigal = pyqtSignal()
    users_info_update_signal = pyqtSignal(dict)
    opt_ess_info_signal = pyqtSignal(dict)  # 收到期权基本信息数据包 的信号
    chat_success_signal = pyqtSignal(dict)
    chat_message_to_groups_signal = pyqtSignal(dict)
    update_password_failed_signal = pyqtSignal(dict)
    update_password_success_signal = pyqtSignal(dict)
    set_temp_password_failed_signal = pyqtSignal(dict)
    set_temp_password_success_signal = pyqtSignal(dict)

    def __init__(self, loop):
        super(MainFormControl, self).__init__()
        self.setupUi(self)
        self.loop = loop
        self.data_interaction_signing_server = None
        self.reset_secret_dialog_control = None
        self.set_temp_secret_dialog_control = None

        # signal
        self.testSigal.connect(self.on_test_signal)
        self.users_info_update_signal.connect(self.on_users_info_update_signal)
        self.chat_message_to_groups_signal.connect(self.on_chat_message_to_groups_signal)
        self.opt_ess_info_signal.connect(self.on_opt_ess_info_signal)
        self.chat_success_signal.connect(self.on_chat_success_signal)
        self.hedge_listWidget.itemClicked.connect(self.on_hedge_listWidget_itemClicked)
        self.transaction_listWidget.itemClicked.connect(self.on_transaction_listWidget_itemClicked)
        self.update_password_failed_signal.connect(self.on_update_password_failed_signal)
        self.update_password_success_signal.connect(self.on_update_password_success_signal)
        # self.set_temp_password_failed_signal.connect(self.on_set_temp_password_failed_signal)
        # self.set_temp_password_success_signal.conect(self.on_set_temp_password_success_signal)

        # self.lots_lineEdit_in_complement_infomation_page.textChange(self.on_lots_lineEdit_in_complement_infomation_page_textChange)
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
        self.second_contract_widget = [
            self.second_contract_code_name_label,
            self.second_contract_code_label,
            self.second_futures_price_name_label,
            self.second_unit_price_name_label,
            self.second_total_price_name_label,
            self.second_option_price_label,
            self.second_unit_price_label,
            self.second_total_price_label,
            self.second_max_lots_name_label,
            self.second_max_lots_label,
        ]  # 次主力合约的所有控件
        #

        self.transaction_users = collections.defaultdict(list)  # 保存所有交易端的用户 键值类型为   公司名:[用户1,用户2,用户3]
        self.hedge_users = collections.defaultdict(list)

        self.test()

        self.html_list = []
        # self.loop.create_task(self.connect_test())

        # self.on_way_for_guest_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # async def connect_test(self):
        #     self.websocket = await websockets.connect("wss://192.168.0.112:8888/traecho")

    def on_update_password_success_signal(self, json):
        self.reset_secret_dialog_control.update_password_success_signal.emit(json)

    def on_update_password_failed_signal(self, json):
        self.reset_secret_dialog_control.update_password_failed_signal.emit(json)

    def on_chat_message_to_groups_signal(self, json):
        '''接收服务器发送而来的消息'''
        logger.info("接收数据")
        logger.info(str(json))

        chat_msg_model = ChatMessageModel.from_json(self, json)
        chat_msg_model.show_message()

    def on_chat_success_signal(self, json):
        '''发送文本成功,服务器做出了相应'''

    def on_transaction_listWidget_itemClicked(self, item):
        self.show_users_listWidget.clear()
        self.hedge_listWidget.setCurrentIndex(QModelIndex())
        for user_name in self.transaction_users[item.text()]:
            self.show_users_listWidget.addItem(user_name)

    def on_hedge_listWidget_itemClicked(self, item):
        self.show_users_listWidget.clear()
        self.transaction_listWidget.setCurrentIndex(QModelIndex())
        for user_name in self.hedge_users[item.text()]:
            self.show_users_listWidget.addItem(user_name)

    @pyqtSlot()
    def on_send_msg_pushButton_clicked(self):

        hedge_list = self.hedge_listWidget.selectedItems()
        transaction_list = self.transaction_listWidget.selectedItems()
        if hedge_list or transaction_list:
            group_list = [item.text() + "_" + "Hedge" for item in hedge_list] + [item.text() + "_" + "Transaction" for
                                                                                 item
                                                                                 in transaction_list]
            chat_req_msg_model = ChatReqMsgModel(self.input_msg_textEdit, self.company_name, self.user_name, group_list,
                                                 self.client_type)
            logger.info("ChatReqMsgModel" + str(chat_req_msg_model))
            to_who = ",".join([item.text() for item in hedge_list + transaction_list])
            # self.show_msg_textBrowser.insertHtml(
            #     f'''<div style="margin:20px 10px;">
            #             <div style="width:10%; text-align:left; background-color:white;
            #             border-radius:10%; color:gray;"> {self.get_time()}</div>
            #             <div>
            #                 <div> 我 对 {to_who}</div> &nbsp;&nbsp;&nbsp;
            #                 <div >{chat_req_msg_model.message}</div>
            #             </div>
            #         </div>
            #         <br>
            #         <div></div>
            #         '''
            # )
            self.html_list.append(f'''
                    <div style="margin:20px 10px;">
                        <div style="width:10%; text-align:center; margin:0 auto; background-color:white;
                            border-radius:10%; color:gray;"> {self.get_time()}</div>
                        <div>
                            <div style="margin-right:20px;"> 我 对 {to_who}</div> &nbsp;&nbsp;&nbsp;
                            <div style="float: right;">{chat_req_msg_model.message}</div>
                        </div>
                    </div>
                ''')
            self.show_msg_textBrowser.setHtml("".join(self.html_list))
            self.send_to_signing_server(chat_req_msg_model.get_json())

        self.input_msg_textEdit.clear()

    def get_time(self):
        return time.strftime("%H:%M", time.localtime())

    @pyqtSlot()
    def on_cancel_pushButton_in_open_check_feasibility_page_clicked(self):
        '''点击取消 回到控制页面'''

        self.stackedWidget.setCurrentWidget(self.control_module_page)

    @pyqtSlot()
    def on_sell_new_option_action_triggered(self):
        '''点击销售新期权,页面跳转'''
        print("销售")
        self.stackedWidget.setCurrentWidget(self.open_check_feasibility_page)

    @pyqtSlot()
    def on_action_triggered(self):
        qApp.exit(888)

    @pyqtSlot()
    def on_reset_password_action_triggered(self):
        '''点击更改密码,弹出更改密码对话框'''
        if not self.reset_secret_dialog_control:
            self.reset_secret_dialog_control = ResetSecretDialogControl(self)
        self.reset_secret_dialog_control.show()

    @pyqtSlot()
    def on_set_temp_password_action_triggered(self):
        '''点击授权密码,弹出设置授权密码对话框'''
        if not self.set_temp_secret_dialog_control:
            self.set_temp_secret_dialog_control = SetTempSecretDialogControl(self)
        self.set_temp_secret_dialog_control.show()

    @pyqtSlot()
    def on_next_pushButton_in_open_check_feasibility_page_clicked(self):
        '''点击期权开仓--检查开仓页面中的下一步按钮
            1.交易端构建请求期权信息数据包,将此数据包发送给签约服务器
            2.等待接收 期权基本信息数据包 等待接收数据不在这里,收到期权基本信息数据包,将会调用 on_opt_ess_info_signal函数
        '''
        requestEssentialInfoModel = RequestEssentialInfoModel(self)
        requestEssentialInfoModel.send_json_to_signing_server()  # 发送给签约服务器

    def on_opt_ess_info_signal(self, json):
        '''
        如果收到了 期权基本信息数据包,将会调用此函数,执行以下步骤
            0.删除期货品种代码中的内容
            1.由收到的json构建期权基本信息数据包
            2.进入信息补全页面,并且利用基本信息数据包填写信息补全页面的一部分的信息
                0.期货合约代码
                1.最远到期日
                2.主力合约最大手数
                3.次主力合约的最大手数（如果有），如果没有，则不显示
                4.主力合约代码
                5.次主力合约代码（如果有）
        '''
        self.fvcode_lineEdit.clear()  # 删除期货品种代码中的内容
        option_essential_info_model = OptionEssentialInfoModel.from_json(self, json)
        self.stackedWidget.setCurrentWidget(self.complement_infomation_page)
        option_essential_info_model.set_show_fvcode_label_text()
        option_essential_info_model.set_furthest_date_due_label_text()
        option_essential_info_model.set_main_max_lots_label_text()
        option_essential_info_model.set_secode_max_lots_label_text()

    def on_users_info_update_signal(self, json):
        '''收到了用户信息,构建updateUsersInfoModel,删除两个列表中除了第一行所有用户名,根据用户名列表更新该列
        1.删除所有公司
        2.添加新公司
        3.更新公司下的用户

        '''
        print(json)
        update_users_info_model = UpdateUsersInfoModel.from_json(self, json)
        update_users_info_model.remove_all_item()
        self.hedge_users.clear()
        self.transaction_users.clear()
        online_users = update_users_info_model.online_users
        for user_company_group in online_users:
            user_name, company_name, group_type = user_company_group.split("_")
            if group_type == "Hedge":
                self.hedge_users[company_name].append(user_name)
            elif group_type == "Transaction":
                self.transaction_users[company_name].append(user_name)

            else:
                logger.info(group_type + "is wrong")
                raise ValueError()
        update_users_info_model.add_all_item(self.hedge_users, self.transaction_users)

    def send_to_signing_server(self, json):
        '''向签约服务器发送数据'''
        self.data_interaction_signing_server.send_data(json)

    def if_connect_to_signing_server(self):
        '''判断是否连接到签约服务器'''
        return False if self.data_interaction_signing_server.web_socket is None else True

    @pyqtSlot(str)
    def on_lots_lineEdit_in_complement_infomation_page_textChanged(self, text):
        '''这个输入应该只能输入数字'''
        self.show_lots_lineEdit_label.setText(f"={text}份")

    def test(self):

        tes = OptionInformationModel(self, "S79426", "壹号土猪", "M1901", "认购止盈", 10, 46.4, 4640000, "1809045", 650,
                                     1539273600.0,
                                     730, 1539273600.0, "对客在途", 1000)
        # tes.insert_to_table(getattr(self, self.tab_name_dict.get(tes.state)))
        tes1 = OptionInformationModel(self, "S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对公在途", 1000)
        # tes1.insert_to_table(getattr(self, self.tab_name_dict.get(tes1.state)))
        tes2 = OptionInformationModel(self, "S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对公今开", 1000)
        # tes2.insert_to_table(getattr(self, self.tab_name_dict.get(tes2.state)))
        tes3 = OptionInformationModel(self, "S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对客今开", 1000)
        # tes3.insert_to_table(getattr(self, self.tab_name_dict.get(tes3.state)))
        tes4 = OptionInformationModel(self, "S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对公今止", 1000)
        # tes4.insert_to_table(getattr(self, self.tab_name_dict.get(tes4.state)))
        tes5 = OptionInformationModel(self, "S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对客今止", 1000)
        # tes5.insert_to_table(getattr(self, self.tab_name_dict.get(tes5.state)))
        tes6 = OptionInformationModel(self, "S79426", "壹号土猪", "M1901", "认购止盈", 130, 46.4, 4640000, "1809045", 650,
                                      1539273600.0,
                                      7320, 1539273600.0, "对客今止", 1000)
        # tes6.insert_to_table(getattr(self, self.tab_name_dict.get(tes6.state)))

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
        # 构造一个包,向签约服务器询价,签约服务判断是否可以询价,如果不可以提示拒绝询价,否则,将询价结果显示在界面中
        # asyncio.run_coroutine_threadsafe(self.enquiry_price_one(),self.loop)
        # self.data_interaction_signing_server.send_data(json.dumps({"purpose": "询价", "contractCode": "1111"}))

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

    @pyqtSlot()
    def on_test_pushButton_clicked(self):

        enquiry_feasibility_request_model = EnquiryFeasibilityRequestModel(self, "询价", "开仓")
        print("期权请求数据包内容-->", json.loads(enquiry_feasibility_request_model.get_json()))

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
            # logger.info(option_info_obj)

    @pyqtSlot(int, int)
    def on_on_way_for_company_tableWidget_cellClicked(self, row, column):
        option_info_obj = self.on_way_for_company_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            # logger.info(option_info_obj)

    @pyqtSlot(int, int)
    def on_today_close_for_guest_tableWidget_cellClicked(self, row, column):
        option_info_obj = self.today_close_for_guest_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            # logger.info(option_info_obj)

    @pyqtSlot(int, int)
    def on_today_close_for_company_tableWidget_cellClicked(self, row, column):
        option_info_obj = self.today_close_for_guest_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            # logger.info(option_info_obj)

    @pyqtSlot(int, int)
    def on_today_open_for_guest_tableWidget_cellClicked(self, row, column):
        option_info_obj = self.today_open_for_guest_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            # logger.info(option_info_obj)

    @pyqtSlot(int, int)
    def on_today_open_for_company_tableWidget_cellClicked(self, row, column):
        option_info_obj = self.today_open_for_company_tableWidget.option_info_obj_list[row]
        if option_info_obj is self.old_option_info_obj:
            return
        else:
            self._change_control_module_page(option_info_obj)
            self.old_option_info_obj = option_info_obj
            # logger.info(option_info_obj)


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
