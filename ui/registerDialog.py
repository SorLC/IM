# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\registerDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(230, 90)
        Dialog.setMaximumSize(QtCore.QSize(230, 90))
        Dialog.setMinimumSize(QtCore.QSize(230, 90))
        self.ok = QtWidgets.QPushButton(Dialog)
        self.ok.setGeometry(QtCore.QRect(150, 50, 61, 21))
        self.ok.setObjectName("ok")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 16))
        self.label.setObjectName("label")
        self.name = QtWidgets.QLineEdit(Dialog)
        self.name.setGeometry(QtCore.QRect(20, 50, 113, 21))
        self.name.setObjectName("name")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Register"))
        self.ok.setText(_translate("Dialog", "ok"))
        self.label.setText(_translate("Dialog", "Register as"))

