# -*- coding:utf8 -*-

from ui.registerDialog import Ui_Dialog
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets


class RegisterWindow(QtWidgets.QDialog, Ui_Dialog):
    usernameSignal = pyqtSignal(str)

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_Dialog.__init__(self)
        self.setupUi(self)

        self.name.setFocus()

        self.ok.clicked.connect(self.accept)

    def get_name(self):
        return self.name.text().strip()
