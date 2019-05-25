# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QTextCursor


class MyTextEdit(QtWidgets.QTextEdit):
    def __init__(self, parent):
        QtWidgets.QTextEdit.__init__(self, parent)
        self.parent = parent

    def keyPressEvent(self, event):
        QtWidgets.QTextEdit.keyPressEvent(self, event)
        if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            if event.modifiers() == QtCore.Qt.ControlModifier:
                self.append('')
                self.moveCursor(QTextCursor.StartOfLine)
                event.accept()
            else:
                event.ignore()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 600)
        MainWindow.setMaximumSize(QtCore.QSize(810, 600))
        MainWindow.setMinimumSize(QtCore.QSize(810, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.msg_send = MyTextEdit(self.centralwidget)
        self.msg_send.setGeometry(QtCore.QRect(230, 380, 571, 121))
        self.msg_send.setObjectName("msg_send")
        self.msg_recv = QtWidgets.QTextEdit(self.centralwidget)
        self.msg_recv.setGeometry(QtCore.QRect(230, 40, 571, 321))
        self.msg_recv.setObjectName("msg_recv")
        self.msg_recv.setReadOnly(True)
        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setGeometry(QtCore.QRect(710, 510, 93, 28))
        self.send.setObjectName("send")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 10, 41, 16))
        self.label.setObjectName("label")
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setGeometry(QtCore.QRect(270, 10, 531, 16))
        self.label_name.setText("")
        self.label_name.setObjectName("label_name")
        self.user = QtWidgets.QTableWidget(self.centralwidget)
        self.user.setGeometry(QtCore.QRect(10, 40, 201, 461))
        self.user.setObjectName("user")
        self.user.setHorizontalHeaderLabels(['Name'])
        self.user.setColumnCount(1)
        self.user.setRowCount(0)
        self.user.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.user.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.user.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.user.verticalHeader().setVisible(False)
        self.user.horizontalHeader().setVisible(False)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 72, 15))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionRegister = QtWidgets.QAction(MainWindow)
        self.actionRegister.setObjectName("actionRegister")
        self.actionLogOut = QtWidgets.QAction(MainWindow)
        self.actionLogOut.setObjectName("actionLogOut")
        self.menu.addAction(self.actionRegister)
        self.menu.addSeparator()
        self.menu.addAction(self.actionLogOut)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.setstatus(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IM - client"))
        MainWindow.setStatusTip(_translate("MainWindow", "Hello"))
        self.send.setText(_translate("MainWindow", "Send"))
        self.label.setText(_translate("MainWindow", "From"))
        self.label_2.setText(_translate("MainWindow", "Online"))
        self.menu.setTitle(_translate("MainWindow", "Option"))
        self.actionRegister.setText(_translate("MainWindow", "Register"))
        self.actionLogOut.setText(_translate("MainWindow", "LogOut"))

    def setstatus(self, status):
        self.msg_recv.setEnabled(status)
        self.msg_send.setEnabled(status)
        self.send.setEnabled(status)
        self.user.setEnabled(status)
        self.actionLogOut.setEnabled(status)
        self.actionRegister.setEnabled(not status)
        if status:
            self.statusbar.hide()
        else:
            self.statusbar.show()
