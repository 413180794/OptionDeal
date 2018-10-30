import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSplitter

from UIpy.mainWindow import Ui_MainWindow


class MainFormControl(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super(MainFormControl, self).__init__()
        self.setupUi(self)
     




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainFormControl()
    mainwindow.show()

    sys.exit(app.exec_())
