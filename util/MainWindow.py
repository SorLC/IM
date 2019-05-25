# -*- coding:utf8 -*-
import socket
import json

from PyQt5.QtGui import QTextCursor

from util.RegisterWindow import RegisterWindow
from util.MessageSolver import MessageSolver
from ui.mainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from util.tools import *


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    name: str
    current_name: str
    cnt = 0
    register_id = -1

    def __init__(self, server_ip):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # 建立菜单栏的信号槽
        self.actionRegister.triggered.connect(self.register)
        self.actionLogOut.triggered.connect(self.logout)

        self.user.doubleClicked.connect(self.__select_user)

        self.send.clicked.connect(self.__send_msg)

        # 建立udp的socket
        self.server_addr = (server_ip, 8888)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 消息轮询
        self.msg = MessageSolver(self.udp, self.server_addr)
        self.msg.receiveMessage.connect(self.__get)

        # 管理历史消息
        self.history_msg = {}

    def register(self):
        reg = RegisterWindow()
        if reg.exec_():
            self.name = reg.get_name()

            # 发送注册请求
            self.cnt += 1
            self.register_id = self.cnt
            data = generate_json(self.name, 'admin', '', 1, self.cnt)
            self.msg.send(data)
            self.msg.start()

    # 登出请求
    def logout(self):
        data = generate_json(self.name, 'admin', '', 2)
        self.msg.send(data)
        self.close()

    # 更新列表
    def show_user(self, user_list):
        cnt = 0
        self.user.setRowCount(len(user_list) - 1)
        for user in user_list:
            if user == self.name:
                continue
            if user not in self.history_msg.keys():
                self.history_msg[user] = []
            self.user.setItem(cnt, 0, QtWidgets.QTableWidgetItem(user))
            cnt += 1

    # 选中用户
    def __select_user(self, index: QtCore.QModelIndex):
        name = index.data()
        self.current_name = name
        self.label_name.setText(name)
        self.show_msg()

    # 显示信息
    def show_msg(self):
        if not hasattr(self, "current_name") or self.history_msg.get(self.current_name, None) is None:
            return
        content = ""
        for tup in self.history_msg[self.current_name]:
            content += tup[0] + ':\n' + tup[1] + " say >>> " + tup[2] + '\n'
        self.msg_recv.setPlainText(content)
        self.msg_recv.moveCursor(QTextCursor.End)

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            self.__send_msg()

    # 发送消息
    def __send_msg(self):
        if hasattr(self, 'current_name'):
            msg = self.msg_send.toPlainText().strip()
            self.msg_send.setPlainText('')
            if msg == "":
                return
            self.cnt += 1
            data = generate_json(self.name, self.current_name, msg, UDP_NORMAL, self.cnt)
            self.history_msg[data['to']].append((data['time'], data['from'], data['msg']))
            self.show_msg()
            self.msg.send(data)

    # 处理接受到的信息
    def __solve_received_msg(self, data):
        if data['id'] == self.register_id:
            # 判断是否注册成功
            if data['flag'] < 0:
                QtWidgets.QMessageBox.information(self, "Error", data['msg'])
            else:
                self.statusbar.showMessage("Welcome, " + self.name)
                self.setstatus(True)
                online = json.loads(data['msg'])
                self.show_user(online.keys())
        elif data['id'] == 0:
            # 广播消息
            if data['flag'] < 0:
                QtWidgets.QMessageBox.information(self, "Error", data['msg'])
                self.setstatus(False)
            elif data['flag'] in [UDP_LOGIN, UDP_LOGOUT]:
                online = json.loads(data['msg'])
                self.show_user(online.keys())
            elif data['flag'] == UDP_CHECK_ALIVE:
                data['from'] = self.name
                data['to'] = 'admin'
                self.msg.send(data)
        else:
            if data['flag'] < 0:
                QtWidgets.QMessageBox.information(self, "Error", data['msg'])
                if data['flag'] == UDP_SERVER_EXIT:
                    self.setstatus(False)
            else:
                # 添加历史记录
                self.history_msg[data['from']].append((data['time'], data['from'], data['msg']))
                # 刷新当前界面
                self.show_msg()
                self.statusbar.showMessage("A message from " + data['from'])

    def __get(self, data):
        self.__solve_received_msg(data)
