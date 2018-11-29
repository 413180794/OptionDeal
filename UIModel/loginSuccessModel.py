# -*- coding: utf-8 -*-
# @Time    : 18-11-12 下午9:09
# @Author  : 张帆
# @Site    : 
# @File    : loginSuccessModel.py
# @Software: PyCharm
from PyQt5 import QtWidgets, QtGui, QtCore

from UIModel.model import Model


class LoginSuccessModel(Model):
    '''收到登录成功数据包'''
    if_add_widget = False

    def __init__(self, mainFormControl, userid, company_name, type_option_combox, main_lineEdit_dict,
                 second_lineEdit_dict,
                 dateEdit_dict, tableWidget, control_module_page_label_dict):
        self.mainFormControl = mainFormControl
        self._user_name, self._client_type = userid.split("_")
        self._company_name = company_name
        self.type_option_combox = type_option_combox
        self._main_lineEdit_dict = main_lineEdit_dict
        self._second_lineEdit_dict = second_lineEdit_dict
        self._dateEdit_dict = dateEdit_dict
        self.tableWidget = tableWidget
        self.control_module_page_label_dict = control_module_page_label_dict
        if not LoginSuccessModel.if_add_widget:
            self.change_dateEdit(self.mainFormControl.complement_infomation_page,
                                 self.mainFormControl.label_name_widget_verticalLayout,
                                 self.mainFormControl.dateEdit_widget_verticalLayout)
            self.change_formLayout(self.mainFormControl.main_contract_formLayout, self.main_lineEdit_dict,
                                   self.mainFormControl.complement_infomation_page)
            self.change_formLayout(self.mainFormControl.second_contract_formLayout, self.second_lineEdit_dict,
                                   self.mainFormControl.complement_infomation_page)
            self.change_type_option_combox(self.mainFormControl.option_type_comboBox)
            self.set_table(self.tableWidget)
            self.create_label_to_control_module_page(self.control_module_page_label_dict)
            LoginSuccessModel.if_add_widget = True

        self.mainFormControl.user_name = self._user_name
        self.mainFormControl.client_type = self._client_type
        self.mainFormControl.company_name = self._company_name
        self.mainFormControl.main_lineEdit_dict = self.main_lineEdit_dict
        self.mainFormControl.second_lineEdit_dict = self.second_lineEdit_dict
        self.mainFormControl.dateEdit_dict = self.dateEdit_dict
        for second_lineEdit in self.second_lineEdit_dict.values():
            self.mainFormControl.second_contract_widget.append(getattr(self.mainFormControl, second_lineEdit))
            self.mainFormControl.second_contract_widget.append(getattr(self.mainFormControl, second_lineEdit + "name"))

    @property
    def main_lineEdit_dict(self):
        return self._main_lineEdit_dict

    @property
    def second_lineEdit_dict(self):
        return self._second_lineEdit_dict

    @property
    def dateEdit_dict(self):
        return self._dateEdit_dict

    @classmethod
    def from_json(cls, mainFormControl, json):
        return cls(mainFormControl, json.get('userid'), json.get("company_name"), json.get('type_option_combox'),
                   json.get("main_lineEdit_widget"),
                   json.get("second_lineEdit_widget"), json.get("time_widget"), json.get("tableWidget"),
                   json.get("control_module_page_label"))

    def change_type_option_combox(self, combox):
        for item in self.type_option_combox:
            combox.addItem(item)

    def create_label(self, page):
        label = QtWidgets.QLabel(page)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label

    def create_label_to_control_module_page(self, tableDict):
        x, y = 0, 0
        for name, variable in tableDict.items():
            verticalLayout = QtWidgets.QVBoxLayout()
            verticalLayout.setSpacing(0)
            verticalLayout.setObjectName("verticalLayout" + variable)
            label = QtWidgets.QLabel(self.mainFormControl.control_module_page)
            font = QtGui.QFont()
            font.setBold(False)
            font.setWeight(50)
            label.setFont(font)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setObjectName("label")
            label.setText(name)
            verticalLayout.addWidget(label)
            setattr(self.mainFormControl, variable + "_in_control_module_page",
                    QtWidgets.QLabel(self.mainFormControl.control_module_page))
            label2 = getattr(self.mainFormControl, variable+"_in_control_module_page")
            label2.setFont(font)
            label2.setAlignment(QtCore.Qt.AlignCenter)
            label2.setObjectName(variable + "_in_control_module_page")
            verticalLayout.addWidget(label2)
            self.mainFormControl.control_model_page_gridLayout.addLayout(verticalLayout, x, y, 1, 1)
            y += 1
            if y == 3:
                x += 1
                y = 0

    def create_dateEdit(self, page, name):
        dateEdit = QtWidgets.QDateEdit(page)
        dateEdit.setObjectName(name)
        return dateEdit

    def change_dateEdit(self, page, label_verticalLayout, dateEdit_verticalLayout):
        for name, variable in self.dateEdit_dict.items():
            label = self.create_label(page)
            label.setText(name)
            setattr(self.mainFormControl, variable, self.create_dateEdit(page, variable))
            label_verticalLayout.addWidget(label)
            dateEdit_verticalLayout.addWidget(getattr(self.mainFormControl, variable))

    def set_tableWidget(self, tableWidgetName, tableDict):
        tableWidget = getattr(self.mainFormControl, tableWidgetName)
        tableWidget.horizontalHeader().setVisible(True)
        tableWidget.setColumnCount(len(tableDict.values()))
        tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        tableWidget.horizontalHeader().setDefaultSectionSize(90)
        tableWidget.horizontalHeader().setHighlightSections(True)
        tableWidget.horizontalHeader().setStretchLastSection(False)
        tableWidget.verticalHeader().setCascadingSectionResizes(True)
        tableWidget.verticalHeader().setStretchLastSection(False)
        tableWidget.setSortingEnabled(True)
        for i, tableName in enumerate(tableDict.keys()):
            print("1!!!!!!!!!!!!!!!!!!")
            item = QtWidgets.QTableWidgetItem()
            tableWidget.setHorizontalHeaderItem(i, item)
            item.setText(tableName)

    def set_table(self, tableWidget):
        for tableWidgetName, tableDict in tableWidget.items():
            self.set_tableWidget(tableWidgetName, tableDict)

    def change_formLayout(self, formLayout, widget_name, page):
        '''
        改变表单中的控件
        :param formLayout: 改变的表单
        :param widget_name: 控件（名称，lineEdit)
        :param page: 该控件所在页
        :return:
        '''

        count = 1
        # for i in range(1, formLayout.rowCount()):
        #     formLayout.removeRow(1) # 删除该表单除了第一行的控件
        for lineEdit_name, lineEdit_variable in widget_name.items():
            label = QtWidgets.QLabel(page)
            label.setObjectName(lineEdit_variable)
            label.setText(lineEdit_name)  # 设置该标签的名称

            formLayout.setWidget(count, QtWidgets.QFormLayout.LabelRole, label)
            setattr(self.mainFormControl, lineEdit_variable + "name", label)
            setattr(self.mainFormControl, lineEdit_variable, QtWidgets.QLineEdit(page))  # 设置lineEdit的变量，其属于mainForm
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                getattr(self.mainFormControl, lineEdit_variable).sizePolicy().hasHeightForWidth())
            getattr(self.mainFormControl, lineEdit_variable).setSizePolicy(sizePolicy)
            getattr(self.mainFormControl, lineEdit_variable).setObjectName(lineEdit_variable)
            formLayout.setWidget(count, QtWidgets.QFormLayout.FieldRole,
                                 getattr(self.mainFormControl, lineEdit_variable))  # 将其添加到表单中
            count += 1
