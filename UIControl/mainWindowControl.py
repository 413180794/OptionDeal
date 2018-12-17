import collections
import json
import os
import pathlib
import ssl
import sys
import logging
import time

import websockets
from PyQt5 import QtGui, QtCore, QtWidgets, sip
from PyQt5.QtGui import QKeySequence
from quamash import QEventLoop
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QModelIndex, QStringListModel, Qt, QSettings, QFile, QTextStream
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel, QDialog, qApp, QListView, QFormLayout, \
    QListWidgetItem, QToolButton, QVBoxLayout, QAction

from UIControl.canTradeDialogControl import CanTradeDialogControl
from UIControl.dataInteraction import DataInteraction
from UIControl.fontAndColorDialogControl import FontAndColorDialogControl
from UIControl.loginDialogControl import LoginDialogControl
from UIControl.resetSecretDialogControl import ResetSecretDialogControl
from UIControl.setTempSecretDialogControl import SetTempSecretDialogControl
from UIControl.shortCutSetDialogControl import ShortCutSetDialogControl
from UIControl.tool import findSubStr, insert

from UIModel.enquiryFeasibilityRequestModel import EnquiryFeasibilityRequestModel

from UIModel.optionEssentialInfoModel import OptionEssentialInfoModel

from UIModel.tableModel import TableModel
from UIView.mainWindow import Ui_MainWindow
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("../log/main_log.txt")
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
    option_table_info_signal = pyqtSignal(dict)
    login_success_signal = pyqtSignal(dict)  # 登录成功信号
    login_failed_signal = pyqtSignal(dict)  # 登录失败信号
    login_pushButton_setDisabled_signal = pyqtSignal(bool)
    set_loginDialog_text_signal = pyqtSignal(str)

    def __init__(self, loop):
        super(MainFormControl, self).__init__()
        self.setupUi(self)
        self.loop = loop
        self.client_type = "Hedge"
        self.data_interaction_signing_server = DataInteraction(self.loop, self)
        self.reset_secret_dialog_control = None
        self.set_temp_secret_dialog_control = None
        self.set_font_and_color_control = None
        self.short_cut_set_dialog_control = None
        self.can_trade_option_dialog_control = None
        self.login_dialog_control = LoginDialogControl(self.client_type, self.login_to_signing_server, self)
        self.data_interaction_signing_server = DataInteraction(self.loop, self)
        self.login_dialog_control.show()
        self.on_way_for_company_tableView_model = TableModel(
            ["交易书编号", "客户名称", "期货合约代码", "手数", "销售单价", "销售总价", "系统单号", "主行权价", "主行权日", "辅行权价", "辅行权日"], [])
        self.on_way_for_guest_tableView_model = TableModel(
            ["交易书编号", "客户名称", "期货合约代码", "手数", "销售单价", "销售总价", "系统单号", "主行权价", "主行权日", "辅行权价", "辅行权日"], [])
        self.today_close_for_company_tableView_model = TableModel(
            ["交易书编号", "客户名称", "期货合约代码", "手数", "销售单价", "销售总价", "系统单号", "主行权价", "主行权日", "辅行权价", "辅行权日"], [])
        self.today_close_for_guest_tableView_model = TableModel(
            ["交易书编号", "客户名称", "期货合约代码", "手数", "销售单价", "销售总价", "系统单号", "主行权价", "主行权日", "辅行权价", "辅行权日"], [])
        self.today_open_for_company_tableView_model = TableModel(
            ["交易书编号", "客户名称", "期货合约代码", "手数", "销售单价", "销售总价", "系统单号", "主行权价", "主行权日", "辅行权价", "辅行权日"], [])
        self.today_open_for_guest_tableView_model = TableModel(
            ["交易书编号", "客户名称", "期货合约代码", "手数", "销售单价", "销售总价", "系统单号", "主行权价", "主行权日", "辅行权价", "辅行权日"], [])

        self.on_way_for_company_tableView.setModel(self.on_way_for_company_tableView_model)
        self.on_way_for_guest_tableView.setModel(self.on_way_for_guest_tableView_model)
        self.today_close_for_company_tableView.setModel(self.today_close_for_company_tableView_model)
        self.today_close_for_guest_tableView.setModel(self.on_way_for_guest_tableView_model)
        self.today_open_for_company_tableView.setModel(self.today_open_for_company_tableView_model)
        self.today_open_for_guest_tableView.setModel(self.today_open_for_guest_tableView_model)

        # 以上的为None的变量在登录成功后才会被初始化

        self.handle = self.splitter.handle(1)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.button = QToolButton(self.handle)
        self.button.setArrowType(QtCore.Qt.RightArrow)
        self.button.clicked.connect(
            lambda: self.handleSplitterButton(False))
        self.layout.addWidget(self.button)
        self.handle.setLayout(self.layout)

        self.handle_2 = self.splitter_2.handle(1)
        self.splitter_2.setSizes([1, 0])
        self.layout_2 = QVBoxLayout()
        self.layout_2.setContentsMargins(0, 0, 0, 0)
        self.button_2 = QToolButton(self.handle_2)
        self.button_2.setArrowType(QtCore.Qt.RightArrow)
        self.button_2.clicked.connect(
            lambda: self.handleSplitterButton_2(False))
        self.layout_2.addWidget(self.button_2)
        self.handle_2.setLayout(self.layout_2)
        # test#
        # self.main_unit_price_label.setObjectName("warnLabel")
        # self.main_total_price_label.setObjectName("warnLabel")
        # test#
        # signal

        self.testSigal.connect(self.on_test_signal)
        self.users_info_update_signal.connect(self.on_users_info_update_signal)
        self.chat_message_to_groups_signal.connect(self.on_chat_message_to_groups_signal)
        self.opt_ess_info_signal.connect(self.on_opt_ess_info_signal)
        self.chat_success_signal.connect(self.on_chat_success_signal)

        self.update_password_failed_signal.connect(self.on_update_password_failed_signal)
        self.update_password_success_signal.connect(self.on_update_password_success_signal)
        self.option_table_info_signal.connect(self.on_option_table_info_signal)
        self.set_temp_password_failed_signal.connect(self.on_set_temp_password_failed_signal)
        self.set_temp_password_success_signal.connect(self.on_set_temp_password_success_signal)
        self.login_success_signal.connect(self.on_login_success_signal)
        self.login_failed_signal.connect(self.on_login_failed_signal)
        self.login_pushButton_setDisabled_signal.connect(self.on_login_pushButton_setDisabled_signal)
        self.set_loginDialog_text_signal.connect(self.on_set_loginDialog_text_signal)
        # self.lots_lineEdit_in_complement_infomation_page.textChange(self.on_lots_lineEdit_in_complement_infomation_page_textChange)
        # 注意这个六个赋值，原来QTableWidget是没有option_info_obj_list的，这是我强行添加的属性，用于保存每一条信息对象
        # 在on_on_way_for_guest_tableWidget_cellClicked 函数中可以体现出它的好处，方便的取到每一条表格中的数据对象
        self.tableModel_name_dict = {"对客在途": "on_way_for_guest_tableView_model", "对公在途": "on_way_for_company_tableView_model",
                              "对客今开": "today_open_for_guest_tableView_model",
                              "对公今开": "today_open_for_company_tableView_model",
                              "对客今止": "today_close_for_guest_tableView_model",
                              "对公今止": "today_close_for_company_tableView_model"}

        self.tableView_name_dict = {"对客在途": "on_way_for_guest_tableView", "对公在途": "on_way_for_company_tableView",
                              "对客今开": "today_open_for_guest_tableView",
                              "对公今开": "today_open_for_company_tableView",
                              "对客今止": "today_close_for_guest_tableView",
                              "对公今止": "today_close_for_company_tableView"}
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
        self.transaction_users = collections.defaultdict(list)  # 保存所有交易端的用户 键值类型为   公司名:[用户1,用户2,用户3]
        self.hedge_users = collections.defaultdict(list)
        self.shortcut_settings = QSettings("short_cut")
        # 所有的自定义action 都应该登录时从QSetting配置

        self.set_shortcut()

    def set_shortcut(self):
        '''配置快捷键'''
        print("配置跨级接纳")
        show_hide_detail_seq = QKeySequence(self.shortcut_settings.value("show_hide_detail"))

        if show_hide_detail_seq:
            self.show_hide_detail_action.setShortcut(show_hide_detail_seq)

        show_hide_company_seq = QKeySequence(self.shortcut_settings.value("show_hide_company"))
        if show_hide_company_seq:
            self.show_hide_company_action.setShortcut(show_hide_company_seq)

        page_down_seq = QKeySequence(self.shortcut_settings.value("page_down"))
        if page_down_seq:
            self.page_down_action.setShortcut(page_down_seq)

        page_up_seq = QKeySequence(self.shortcut_settings.value("page_up"))
        if page_up_seq:
            self.page_up_action.setShortcut(page_up_seq)

        location_up_seq = QKeySequence(self.shortcut_settings.value("location_up"))
        if location_up_seq:
            self.location_up_action.setShortcut(location_up_seq)

        location_right_seq = QKeySequence(self.shortcut_settings.value("location_right"))
        if location_right_seq:
            self.location_right_action.setShortcut(location_right_seq)

        location_left_seq = QKeySequence(self.shortcut_settings.value("location_left"))
        if location_left_seq:
            self.location_left_action.setShortcut(location_left_seq)

        location_down_seq = QKeySequence(self.shortcut_settings.value("location_down"))
        if location_down_seq:
            self.location_down_action.setShortcut(location_down_seq)

    @pyqtSlot()
    def on_move_right_action_2_triggered(self):
        '''触发向右平移'''
        print("向右平移")
        print(self.locale())
        # self.move(self.x()-self.move_right_lengh,self.y())  # 更改窗口位置

    @pyqtSlot()
    def on_switch_behind_action_triggered(self):
        '''触发向后切'''
        print("向后切")

    @pyqtSlot()
    def on_switch_front_action_triggered(self):
        "触发向前切"
        print("向前切")
    @pyqtSlot()
    def on_show_hide_detail_action_triggered(self):
        '''触发隐藏显示明细'''
        print("隐藏显示明细平")
    @pyqtSlot()
    def on_show_hide_company_action_triggered(self):
        '''触发隐藏对公'''
        print("隐藏对公")
    @pyqtSlot()
    def on_hide_detail_company_action_triggered(self):
        '''触发隐藏对公与明细'''
        print("隐藏对公与明细")
    @pyqtSlot()
    def on_page_down_action_triggered(self):
        '''触发向下翻页'''
        print("向下翻页")
    @pyqtSlot()
    def on_page_up_action_triggered(self):
        '''触发向上翻页'''
        print("向上翻页")
    @pyqtSlot()
    def on_location_up_action_triggered(self):
        '''触发定位最上'''
        print("定位最上")
    @pyqtSlot()
    def on_location_down_action_triggered(self):
        '''定位最下'''
        print("定位最下")
    @pyqtSlot()
    def on_location_left_action_triggered(self):
        '''定位最左'''
        print("定位最左")
    @pyqtSlot()
    def on_location_right_action_triggered(self):
        '''定位最右'''
        print("定位最右")
    @pyqtSlot()
    def on_add_price_action_triggered(self):
        '''增加溢价率'''
        print("溢价率")
    @pyqtSlot()
    def on_recove_price_action_triggered(self):
        '''恢复溢价率'''
        print("恢复溢价率")
    def handleSplitterButton(self, left=True):
        if left:
            self.splitter.setSizes([4, 1])
            self.button.setArrowType(QtCore.Qt.RightArrow)
            self.button.clicked.disconnect()
            self.button.clicked.connect(
                lambda: self.handleSplitterButton(False))
        else:
            self.splitter.setSizes([1, 0])
            self.button.setArrowType(QtCore.Qt.LeftArrow)
            self.button.clicked.disconnect()
            self.button.clicked.connect(
                lambda: self.handleSplitterButton(True))

    def handleSplitterButton_2(self, left=True):
        if left:
            self.splitter_2.setSizes([4, 1])
            self.button_2.setArrowType(QtCore.Qt.RightArrow)
            self.button_2.clicked.disconnect()
            self.button_2.clicked.connect(
                lambda: self.handleSplitterButton_2(False))
        else:
            self.splitter_2.setSizes([1, 0])
            self.button_2.setArrowType(QtCore.Qt.LeftArrow)
            self.button_2.clicked.disconnect()
            self.button_2.clicked.connect(
                lambda: self.handleSplitterButton_2(True))

    @pyqtSlot()
    def on_font_color_action_triggered(self):
        if not self.set_font_and_color_control:
            self.set_font_and_color_control = FontAndColorDialogControl(self.reset_ui, self)
        self.set_font_and_color_control.show()

    @pyqtSlot()
    def on_set_short_cut_action_triggered(self):
        if not self.short_cut_set_dialog_control:
            self.short_cut_set_dialog_control = ShortCutSetDialogControl(self)
            self.short_cut_set_dialog_control.reset_shortcut_signal.connect(self.set_shortcut)
        self.short_cut_set_dialog_control.set_seq()
        self.short_cut_set_dialog_control.show()

    @pyqtSlot(dict)
    def on_login_failed_signal(self, json):
        '''触发登录失败'''
        # 在登录界面中显示失败的原因
        self.login_dialog_control.lineedit_empty_Label.setText(json['failure_reason'])
        self.data_interaction_signing_server.disconnect_to_server()
        self.login_dialog_control.login_pushButton.setDisabled(False)

    @pyqtSlot(dict)
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
        self.user_name, self.client_type = json['userid'].split("_")
        self.company_name = json['company_name']
        self.login_dialog_control.close()
        self.option_type = json['option_type']
        self.pre_rate = json['pre_rate'] # 溢价率 ---
        self.can_trade_option = json['opt_info'] # 今日可销售期权
        self.change_type_option_combox(self.option_type)
        self.show()  # 打开主界面

    @pyqtSlot()
    def on_can_trade_option_action_triggered(self):
        '''查看今日可销售期权'''
        if not self.can_trade_option_dialog_control:
            self.can_trade_option_dialog_control = CanTradeDialogControl(self,self.can_trade_option)
        self.can_trade_option_dialog_control.show()

    def change_type_option_combox(self, option_type):
        for item in option_type.keys():
            self.option_type_comboBox.addItem(item)

    @pyqtSlot(bool)
    def on_login_pushButton_setDisabled_signal(self, state):
        self.login_dialog_control.login_pushButton.setDisabled(state)

    @pyqtSlot(str)
    def on_set_loginDialog_text_signal(self, text):
        self.login_dialog_control.lineedit_empty_Label.setText(text)

    def login_to_signing_server(self, url, port, login_request_json):
        '''登录到到签约服务器'''
        # logger.info("登录到签约服务器-->" + str(self.if_connect_to_signing_server()))
        # print(self.if_connect_to_signing_server())
        index = findSubStr("/", url, 3)
        print(index)
        if index != -1:
            url = insert(url, ":" + port, index)
        else:
            url = url + ":" + port
        print(url)
        self.data_interaction_signing_server.connect_to_sever(url, login_request_json)

    def delete_formLayout_widget(self, formLayout):
        # formLayout中除了第一行中所有控件
        for i in range(1, formLayout.rowCount()):
            formLayout.removeRow(1)

    def create_label(self, name):
        '''在page中创建一个label'''
        label = QtWidgets.QLabel(self.complement_infomation_page)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText(name)
        label.setObjectName(name)
        return label

    def create_dateEdit(self):
        '''创建一个dateEdit'''
        dateEdit = QtWidgets.QDateEdit(self.complement_infomation_page)

        return dateEdit

    def create_lineEdit(self):
        lineEdit = QtWidgets.QLineEdit(self.complement_infomation_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(lineEdit.sizePolicy().hasHeightForWidth())
        lineEdit.setSizePolicy(sizePolicy)
        return lineEdit

    def create_spinBox(self):
        spinBox = QtWidgets.QSpinBox(self.complement_infomation_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(spinBox.sizePolicy().hasHeightForWidth())
        spinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        spinBox.setSizePolicy(sizePolicy)
        spinBox.setRange(0, 100000)
        return spinBox

    @pyqtSlot(str)
    def on_option_type_comboBox_currentTextChanged(self, option_type):
        '''修改主界面
        1.  删除dateEdit_widget_verticalLayout中除了第一行所有控件
            删除label_name_widget_verticalLayout中除了第一行所有控件
            删除main_contract_formLayout中除了第一行中所有控件
            删除second_contract_formLayout中除了第一行中所有控件

        2.  重新向上述布局中添加新控件
        '''
        self.delete_formLayout_widget(self.dateEdit_formLayout)
        self.delete_formLayout_widget(self.main_contract_formLayout)
        self.delete_formLayout_widget(self.second_contract_formLayout)
        # 删除之后,开始添加新的
        # 1.添加日期
        for time_name in self.option_type.get(option_type).get("time_type"):
            label = self.create_label(time_name)
            date_edit = self.create_dateEdit()
            self.dateEdit_formLayout.addRow(label, date_edit)

        # 2.主力合约添加价格
        for price_name in self.option_type.get(option_type).get("price_type"):
            label = self.create_label(price_name)
            lineEdit = self.create_spinBox()
            self.main_contract_formLayout.addRow(label, lineEdit)
        # 2.次主力
        for price_name in self.option_type.get(option_type).get("price_type"):
            label = self.create_label(price_name)
            lineEdit = self.create_spinBox()
            self.second_contract_formLayout.addRow(label, lineEdit)

    @pyqtSlot(dict)
    def on_option_table_info_signal(self, json):
        '''收到主界面表格中所需要的信息'''
        header = json['header']
        table_data = json['table_data']
        for table_name, data in table_data.items():
            table_model_variable = self.tableModel_name_dict[table_name]
            table_model_variable = getattr(self, table_model_variable)
            table_model_variable.update_table(header, data)
            tableView_variable = self.tableView_name_dict[table_name]
            tableView_variable = getattr(self,tableView_variable)
            tableView_variable.setColumnHidden(len(header)-1,True)
    @pyqtSlot(dict)
    def on_set_temp_password_failed_signal(self, json):
        self.set_temp_secret_dialog_control.set_temp_password_failed_signal.emit(json)

    @pyqtSlot(dict)
    def on_set_temp_password_success_signal(self, json):
        self.set_temp_secret_dialog_control.set_temp_password_success_signal.emit(json)

    @pyqtSlot(dict)
    def on_update_password_success_signal(self, json):
        self.reset_secret_dialog_control.update_password_success_signal.emit(json)

    @pyqtSlot(dict)
    def on_update_password_failed_signal(self, json):
        self.reset_secret_dialog_control.update_password_failed_signal.emit(json)

    @pyqtSlot(dict)
    def on_chat_message_to_groups_signal(self, json):
        '''接收服务器发送而来的消息'''
        logger.info("接收数据")
        logger.info(str(json))

        self.html_list.append(f'''
                          <div style="margin:20px 10px;">
                          <div style="width:10%; text-align:center; margin:0 auto; background-color:white;
                                  border-radius:10%; color:gray;"> {time.strftime("%H:%M", time.localtime())}</div>
                              <div >
                                  <div style="margin-right:20px;"> {json['from_user']} 对 {self.company_name}</div>
                                  <div style="float: right;">{json['message']}</div>
                              </div>
                          </div>
                             ''')
        self.show_msg_textBrowser.setHtml("".join(self.html_list))

    @pyqtSlot(dict)
    def on_chat_success_signal(self, json):
        '''发送文本成功,服务器做出了相应'''

    @pyqtSlot(QListWidgetItem)
    def on_transaction_listWidget_itemClicked(self, item):

        self.show_users_listWidget.clear()
        self.hedge_listWidget.setCurrentIndex(QModelIndex())
        for user_name in self.transaction_users[item.text()]:
            self.show_users_listWidget.addItem(user_name)

    @pyqtSlot(QListWidgetItem)
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
            message = self.input_msg_textEdit.document().toPlainText()
            to_who = ",".join([item.text() for item in hedge_list + transaction_list])
            self.html_list.append(f'''
                    <div style="margin:20px 10px;">
                        <div style="width:10%; text-align:center; margin:0 auto; background-color:white;
                            border-radius:10%; color:gray;"> {self.get_time()}</div>
                        <div>
                            <div style="margin-right:20px;text-align:right"> 我 对 {to_who}</div> 
                            <div style="text-align:right;">{message}</div>
                        </div>
                    </div>
                ''')
            self.show_msg_textBrowser.setHtml("".join(self.html_list))
            chat_req_msg_json = json.dumps({
                "purpose": "chat_message",
                "user_name": self.user_name,
                "group_list": group_list,
                "company_name": self.company_name,
                "userid": self.user_name + "_" + self.client_type,
                "message": message
            })
            self.send_to_signing_server(chat_req_msg_json)
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

        self.stackedWidget.setCurrentWidget(self.open_check_feasibility_page)

    @pyqtSlot()
    def on_action_triggered(self):
        qApp.exit(888)

    @pyqtSlot()
    def on_reset_password_action_triggered(self):
        '''点击更改密码,弹出更改密码对话框'''
        if not self.reset_secret_dialog_control:
            self.reset_secret_dialog_control = ResetSecretDialogControl(self.client_type, self.user_name,
                                                                        self.send_to_signing_server, self)

        self.reset_secret_dialog_control.show()

    @pyqtSlot()
    def on_set_temp_password_action_triggered(self):
        '''点击授权密码,弹出设置授权密码对话框'''
        if not self.set_temp_secret_dialog_control:
            self.set_temp_secret_dialog_control = SetTempSecretDialogControl(self.client_type, self.user_name,
                                                                             self.send_to_signing_server, self)
        self.set_temp_secret_dialog_control.show()

    @pyqtSlot()
    def on_next_pushButton_in_open_check_feasibility_page_clicked(self):
        '''点击期权开仓--检查开仓页面中的下一步按钮
            1.交易端构建请求期权信息数据包,将此数据包发送给签约服务器
            2.等待接收 期权基本信息数据包 等待接收数据不在这里,收到期权基本信息数据包,将会调用 on_opt_ess_info_signal函数
        '''



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
        online_users = json.get("online_users")
        self.hedge_listWidget.clear()
        self.transaction_listWidget.clear()
        self.hedge_users.clear()
        self.transaction_users.clear()
        for user_company_group in online_users:
            user_name, company_name, group_type = user_company_group.split("_")
            if group_type == "Hedge":
                self.hedge_users[company_name].append(user_name)
            elif group_type == "Transaction":
                self.transaction_users[company_name].append(user_name)
            else:
                logger.info(group_type + "is wrong")
                raise ValueError()

        for company_name in self.hedge_users.keys():
            self.hedge_listWidget.addItem(company_name)
        for company_name in self.transaction_users.keys():
            self.transaction_listWidget.addItem(company_name)

    def send_to_signing_server(self, json):
        '''向签约服务器发送数据'''
        self.data_interaction_signing_server.send_data(json)

    def if_connect_to_signing_server(self):
        '''判断是否连接到签约服务器'''
        self.lots_spinBox_in_complement_infomation_page.valueChanged()
        return False if self.data_interaction_signing_server.web_socket is None else True

    @pyqtSlot(int)
    def on_lots_spinBox_in_complement_infomation_page_valueChanged(self, value):
        '''这个输入应该只能输入数字'''
        self.show_lots_lineEdit_label.setText(f"={str(value)}份")

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
        del enquiry_feasibility_request_model

    def on_test_signal(self):

        self.loginDialog.show()
        self.loginDialog.raise_()
        self.loginDialog.activateWindow()
        # QMessageBox.information(self, "未选中期权", "未选中期权", QMessageBox.Yes | QMessageBox.No)

    @pyqtSlot()
    def on_cancel_enquiry_pushButton_clicked(self):
        '''点击取消按钮，回到控制页面，如果正在询价，也应该断开盯市询价。目前只是简单的回到控制页面'''
        self.stackedWidget.setCurrentWidget(self.control_module_page)

    def _change_control_module_page(self, row_data):
        '''利用表格中某行数据来修改control_module_page(控制模块)的内容'''

        self.transaction_number_label.setText(str(row_data[0]))
        self.option_type_label.setText(str(row_data[1]))
        self.customer_name_label.setText(str(row_data[2]))
        self.contract_code_label.setText(str(row_data[3]))
        self.lots_label.setText(str(row_data[4]))
        self.number_per_hand_label.setText(str(row_data[5]))
        self.unit_price_label.setText(str(row_data[6]))
        self.total_price_label.setText(str(row_data[7]))

        self.main_strike_price_label.setText(str(row_data[8]))
        self.main_exercise_date_label.setText(self.time_stamp_to_str(row_data[10]))
        second_strike_price = ",".join([str(x) for x in row_data[11]])
        self.second_strike_price_label.setText(second_strike_price)
        second_exercise_date = ",".join([self.time_stamp_to_str(x) for x in row_data[12]])
        self.second_exercise_date_label.setText(str(second_exercise_date))

    def time_stamp_to_str(self, time_stamp, format_str='%Y/%m/%d'):
        '''时间戳转化结构化的时间字符串  ---> 2018/12/12'''
        time_now = time.strftime(format_str, time.localtime(time_stamp))
        return time_now

    @pyqtSlot(QModelIndex)
    def on_on_way_for_guest_tableView_clicked(self, QModelIndex):
        '''点击表格某一行,修改界面中lable内容'''
        self.state_label.setText("对客在途")
        row = QModelIndex.row()
        row_data = self.on_way_for_guest_tableView_model.get_row_data(row)
        print(row_data)
        self._change_control_module_page(row_data)

    @pyqtSlot(QModelIndex)
    def on_on_way_for_company_tableView_clicked(self, QModelIndex):
        self.state_label.setText("对公在途")
        row = QModelIndex.row()
        row_data = self.on_way_for_guest_tableView_model.get_row_data(row)
        print(row_data)
        self._change_control_module_page(row_data)

    @pyqtSlot(QModelIndex)
    def on_today_close_for_guest_tableView_clicked(self, QModelIndex):
        self.state_label.setText("对客今止")
        row = QModelIndex.row()
        row_data = self.on_way_for_guest_tableView_model.get_row_data(row)
        print(row_data)
        self._change_control_module_page(row_data)

    @pyqtSlot(QModelIndex)
    def on_today_close_for_company_tableView_clicked(self, QModelIndex):
        self.state_label.setText("对公今止")
        row = QModelIndex.row()
        row_data = self.on_way_for_guest_tableView_model.get_row_data(row)
        print(row_data)
        self._change_control_module_page(row_data)

    @pyqtSlot(QModelIndex)
    def on_today_open_for_guest_tableView_clicked(self, QModelIndex):
        self.state_label.setText("对客今开")
        row = QModelIndex.row()
        row_data = self.on_way_for_guest_tableView_model.get_row_data(row)
        print(row_data)
        self._change_control_module_page(row_data)

    @pyqtSlot(QModelIndex)
    def on_today_open_for_company_tableView_clicked(self, QModelIndex):
        self.state_label.setText("对公今开")
        row = QModelIndex.row()
        row_data = self.on_way_for_guest_tableView_model.get_row_data(row)
        print(row_data)
        self._change_control_module_page(row_data)

    def reset_ui(self):
        stylesheet = getstylesheetfromQss("ui.qss")
        self.setStyleSheet(stylesheet)


class App(QApplication):
    def __init__(self):

        QApplication.__init__(self, sys.argv)
        loop = QEventLoop(self)
        self.loop = loop

        asyncio.set_event_loop(self.loop)
        self.gui = MainFormControl(self.loop)
        self.gui.show()
        stylesheet = getstylesheetfromQss('ui.qss')
        self.gui.setStyleSheet(stylesheet)
        exit_code = self.exec_()
        if exit_code == 888:
            self.restart_program()
        else:
            sys.exit()

        loop.run_forever()

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


def getstylesheetfromQss(qss_path):
    file = QFile(qss_path)
    file.open(QFile.ReadOnly)
    ts = QTextStream(file)
    stylesheet = ts.readAll()
    return stylesheet


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
