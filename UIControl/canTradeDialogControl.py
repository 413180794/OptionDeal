# -*- coding: utf-8 -*-
# @Time    : 18-12-17 上午9:00
# @Author  : 张帆
# @Site    : 
# @File    : canTradeDialogControl.py
# @Software: PyCharm
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from UIModel.tableModel import TableModel
from UIView.canTradeDialog import Ui_canTradeDialog
from PyQt5.QtCore import pyqtSlot, QModelIndex

class CanTradeDialogControl(QDialog, Ui_canTradeDialog):
    def __init__(self, parent, can_trade_option):
        super(CanTradeDialogControl, self).__init__(parent)
        self.setupUi(self)
        self.header = ["品种代码", "主单限量", "副单限量", "最小销量"]
        self.show_can_trade_model = TableModel(
            ["品种代码", "主单限量", "副单限量", "最小销量"], [])
        self.tableView.setModel(self.show_can_trade_model)
        self.can_trade_option = can_trade_option
        self.add_option_to_tableView()
        self.tableView.setColumnHidden(3,True)


    @pyqtSlot(QModelIndex)
    def on_tableView_clicked(self, QModelIndex):
        row = QModelIndex.row()
        row_data = self.show_can_trade_model.get_row_data(row)
        self.label.setText(f"最小销量:{row_data[3]}手")

    def add_option_to_tableView(self):
        all_row = []
        for opt_code, opt_info in self.can_trade_option.items():
            all_row.append(
                [opt_info['opt_code'], opt_info['max_main_num'], opt_info['max_sub_num'], opt_info['min_deal']])
        self.show_can_trade_model.update_table(self.header, all_row)
