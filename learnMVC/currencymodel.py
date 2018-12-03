# -*- coding: utf-8 -*-
# @Time    : 18-12-1 下午3:26
# @Author  : 张帆
# @Site    : 
# @File    : currencymodel.py
# @Software: PyCharm
import time

from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt, QModelIndex


class CurrencyModel(QAbstractTableModel):
    def __init__(self,data:list,header):
        super(CurrencyModel, self).__init__()
        self.data_ = data
        self.header = header


    def append_data(self,x):
        self.data_.append(x)
        self.layoutChanged.emit()

    def remove_row(self,row):
        self.data_.pop(row)
        self.layoutChanged.emit()

    def reset_data(self,x):
        self.data_ = x
        self.layoutChanged.emit()
    def reset_header(self,x):
        self.header = x
        self.layoutChanged.emit()
    def rowCount(self, parent=None, *args, **kwargs):
        if self.data_:
            return len(self.data_)
        else:
            return 0

    def columnCount(self, parent=None, *args, **kwargs):
        if not self.data_:
            return 0
        if len(self.data_) > 0:
            return len(self.data_[0])
        return 0

    def time_stamp_to_str(self,time_stamp,format_str='%Y/%m/%d'):
        '''时间戳转化结构化的时间字符串  ---> 2018/12/12'''
        time_now = time.strftime(format_str,time.localtime(time_stamp))
        return time_now


    def get_data(self):
        return self
    # 返回一个项的任意角色的值，这个项被指定为QModelIndex
    def data(self, QModelIndex, role=None):
        if not QModelIndex.isValid():
            print("行或者列有问题")
            return QVariant()
        # if role == Qt.TextAlignmentRole:
        #     return int(Qt.AlignRight | Qt.AlignVCenter)
        # elif role == Qt.DisplayRole:
        #     row = QModelIndex.row()
        #     column = QModelIndex.column()
        #     return self.currencyMap.get('data')[row][column]
        # # print("查数据")
        # row = QModelIndex.row()
        # # print('role:',role)
        # if role is None:
        #     return self.currencyMap.get('data')[row]
        elif role != Qt.DisplayRole:
            print("123")
            return QVariant()
        table_data = self.data_[QModelIndex.row()][QModelIndex.column()]
        if isinstance(table_data,list):
            if isinstance(table_data[0],int):
                if table_data[0] > 1262275200:
                    table_data = [self.time_stamp_to_str(x) for x in table_data]
                    table_data = ",".join(table_data)
                    return QVariant(table_data)
                else:
                    table_data = [str(x) for x in table_data]
                    x = ",".join(table_data)
                    return QVariant(x)
            else:
                table_data = [str(x) for x in table_data]
                x = ",".join(table_data)
                return QVariant(x)
        return QVariant(self.data_[QModelIndex.row()][QModelIndex.column()])


    def headerData(self, p_int, Qt_Orientation, role=None):
        # if role != Qt.DisplayRole:
        #     return QVariant()
        # else:
        #     if Qt_Orientation == Qt.Horizontal:
        #         if len(self.currencyMap.get('header')) > p_int:
        #             return self.currencyMap.get('header')[p_int]
        print(123222)
        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[p_int])
        return QVariant()

