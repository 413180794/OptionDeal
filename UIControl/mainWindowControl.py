from PyQt5.QtWidgets import QMainWindow

from UIpy.mainWindow import Ui_MainWindow


class MainFormControl(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super(MainFormControl, self).__init__()
        self.setupUi(self)


