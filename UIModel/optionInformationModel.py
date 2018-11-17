# -*- coding: utf-8 -*-
# @Time    : 18-11-2 下午4:27
# @Author  : 张帆
# @Site    : 
# @File    : optionInformationModel.py
# @Software: PyCharm
'''每一行显示在期权交易端表格中的数据'''
import time

from PyQt5.QtWidgets import QTableWidgetItem

from UIModel.model import Model


class OptionInformationModel(Model):
    '''自动向tablewidget中插入。也许还能做更多的事情？->从json中构建对象'''

    def get_json(self):
        pass

    @classmethod
    def from_json(cls, mainFormControl, json):
        pass

    def __init__(self, mainFormControl, transaction_number: str, customer_name: str, contract_code: str,
                 option_type: str,
                 lots: int, unit_price: float, total_price: float, system_number: str, main_strike_price: float,
                 main_exercise_date: float, second_strike_price: float, second_exercise_date: float,
                 state: str, number_per_hand: int):
        '''
        :param transaction_number:  交易书编号
        :param customer_name: 客户名称
        :param contract_code: 合约代码
        :param option_type: 期权类型
        :param total_price: 总价
        :param lots: 手数
        :param number_per_hand: 每手份数
        :param unit_price: 单价
        :param system_number: 系统单号
        :param main_strike_price: 主行权价
        :param main_exercise_date: 主行权日
        :param second_strike_price: 次行权价
        :param second_exercise_date: 次行权日
        :param state: 状态
        :param tabelWidget: 所对应的表格
        '''
        self.mainFormControl = mainFormControl
        self.state = state
        self._second_exercise_date = second_exercise_date
        self.second_strike_price = second_strike_price
        self._main_exercise_date = main_exercise_date
        self.main_strike_price = main_strike_price
        self.unit_price = unit_price
        self.number_per_hand = number_per_hand
        self.lots = lots
        self.system_number = system_number
        self.total_price = total_price
        self.option_type = option_type
        self.contract_code = contract_code
        self.customer_name = customer_name
        self.transaction_number = transaction_number
        self.table_data = [self.transaction_number, self.customer_name, self.contract_code, self.option_type, self.lots,
                           self.unit_price, self.total_price, self.system_number,
                           self.main_strike_price, self.main_exercise_date,
                           self.second_strike_price, self.second_exercise_date]
        self._insert_to_table(getattr(self.mainFormControl, self.mainFormControl.tab_name_dict.get(self.state)))
        # 这里不一定是insert,也有可能是更新
    @property
    def main_exercise_date(self):
        return time.strftime("%Y/%m/%d", time.localtime(self._main_exercise_date))

    @property
    def second_exercise_date(self):
        return time.strftime("%Y/%m/%d", time.localtime(self._second_exercise_date))

    def _insert_to_table(self, tableWidget):
        '''将数据插入到表格中'''
        tableWidget.option_info_obj_list.append(self)
        tableWidget.insertRow(tableWidget.rowCount())
        for column in range(tableWidget.columnCount()):
            print(self.table_data[column])
            item = QTableWidgetItem(str(self.table_data[column]))
            item.setToolTip(str(self.table_data[column]))
            tableWidget.setItem(tableWidget.rowCount() - 1, column, item)

    def __repr__(self):
        return f'''
        交易书编号:{self.transaction_number},
        客户名称:{self.customer_name},
        合约代码:{self.contract_code},
        期权类型:{self.option_type},
        总价:{self.total_price},
        手数:{self.lots},
        每手份数:{self.number_per_hand},
        单价:{self.unit_price},
        主行权价:{self.main_strike_price},
        主行权日:{self.main_exercise_date},
        次行权价:{self.second_strike_price},
        此行权日:{ self.second_exercise_date},
        状态:{self.state},
        '''
