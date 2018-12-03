# -*- coding: utf-8 -*-
# @Time    : 18-12-2 下午3:34
# @Author  : 张帆
# @Site    : 
# @File    : tableModel.py
# @Software: PyCharm
import time

from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt


class TableModel(QAbstractTableModel):
    def __init__(self, header: list, table_data: list):
        super(TableModel, self).__init__()
        self.table_data = table_data
        self.header = header

    def add_row(self, row_data: list):
        '''向表格中增加一行数据'''
        self.table_data.append(row_data)
        self.layoutChanged.emit()

    def romove_row(self, row):
        '''删除表格中指定行数据'''
        self.table_data.pop(row)
        self.layoutChanged.emit()

    def get_row_data(self, row):
        '''获得表格中一行数据'''
        return self.table_data[row]

    def update_table(self, header, table_data):
        self.header = header
        self.layoutChanged.emit()
        self.table_data = table_data
        self.layoutChanged.emit()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.table_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.header)

    def time_stamp_to_str(self, time_stamp, format_str='%Y/%m/%d'):
        '''  时间戳转化结构化的时间字符串 ---> 2018/12/12  '''
        time_now = time.strftime(format_str, time.localtime(time_stamp))
        return time_now

    def data(self, QModelIndex, role=None):
        if not QModelIndex.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        table_data = self.table_data[QModelIndex.row()][QModelIndex.column()]
        if isinstance(table_data, list):
            if isinstance(table_data[0], int) or isinstance(table_data[0], double):
                if table_data[0] > 1262275200:
                    table_data = [self.time_stamp_to_str(x) for x in table_data]
                    table_data = ",".join(table_data)
                    return QVariant(table_data)
                else:
                    table_data = [str(x) for x in table_data]
                    table_data = ",".join(table_data)
                    return QVariant(table_data)
            else:
                table_data = [str(x) for x in table_data]
                x = ",".join(table_data)
                return QVariant(x)
        if isinstance(table_data, float) or isinstance(table_data, int):
            if table_data > 1262275200:
                table_data = self.time_stamp_to_str(table_data)
                return QVariant(table_data)
        return QVariant(self.table_data[QModelIndex.row()][QModelIndex.column()])

    def headerData(self, p_int, Qt_Orientation, role=None):
        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[p_int])
        return QVariant()
