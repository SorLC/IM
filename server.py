# -*- coding:utf8 -*-
import copy
import sys
import socket
import threading
import json

from util.tools import *
from PyQt5.QtCore import QThread, pyqtSignal, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class Receiver(QThread):
    checkAlive = pyqtSignal(str, tuple)
    normalMessage = pyqtSignal(dict, tuple)

    def __init__(self, udp):
        QThread.__init__(self)
        self.udp = udp

    def run(self):
        while True:
            data_json, addr = self.udp.recvfrom(BUFF_SIZE)
            data = json.loads(data_json.decode())
            if data['flag'] == UDP_CHECK_ALIVE:
                self.checkAlive.emit(data['from'], addr)
            else:
                self.normalMessage.emit(data, addr)


class MessageSolver(QMainWindow):
    online = {}
    __online_tmp = {}

    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(300, 300, 400, 50)
        self.setWindowTitle('IM - server')

        server_name = socket.getfqdn(socket.gethostname())
        server_ip = socket.gethostbyname(server_name)
        # server_ip = '127.0.0.1'
        self.addr = (server_ip, 8888)
        # 建立udp的socket
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(self.addr)

        label1 = QLabel(self)
        label1.setGeometry(QRect(25, 0, 400, 50))
        label1.setText('Server is running on (%s, %d)' % (self.addr[0], self.addr[1]))

        # 轮询接受消息
        self.msg_receiver = Receiver(self.udp)
        self.msg_receiver.normalMessage.connect(self.normal_message_receiver)
        self.msg_receiver.checkAlive.connect(self.check_alive_receiver)

        self.online['admin'] = self.addr

        self.msg_receiver.start()

        self.check_alive_sender_thread = threading.Thread(target=self.check_alive_sender)

    # 检查存活
    def check_alive_sender(self):
        self.online_tmp.clear()
        self.__online_tmp['admin'] = self.addr
        data = generate_json('admin', '', '', UDP_CHECK_ALIVE)
        self.__broadcast(data)
        time.sleep(1)
        self.online = copy.deepcopy(self.__online_tmp)

    # 接受存活确认帧
    def check_alive_receiver(self, name, addr):
        # print(name, addr)
        self.__online_tmp[name] = addr

    def normal_message_receiver(self, data, addr):
        normal_msg_thread = threading.Thread(target=self.__normal_msg, args=(data, addr))
        normal_msg_thread.start()
        normal_msg_thread.join()
        if not self.check_alive_sender_thread.isAlive():
            self.check_alive_sender_thread = threading.Thread(target=self.check_alive_sender)
            self.check_alive_sender_thread.start()

    def __normal_msg(self, data, addr):
        print(data, addr)
        # 正常会话
        if data['flag'] == UDP_NORMAL:
            dest = data['to']
            dest_addr = self.online.get(dest, None)
            if dest == 'admin':
                dt = generate_json('admin', data['from'], f'hello, it is {time.ctime()} now.', UDP_NORMAL, data['id'])
                dest_addr = addr
            elif dest_addr is None:
                dt = generate_json('admin', data['from'], 'no such user', UDP_ERROR, data['id'])
                dest_addr = addr
            else:
                dt = data
            self.__send(dt, dest_addr)
            print(data['from'], "->", dest, dest_addr)
        # 注册请求
        elif data['flag'] == UDP_LOGIN:
            src = data['from']
            if self.online.get(src, None) is None:
                self.online[src] = addr
                dt = generate_json('admin', src, json.dumps(self.online), UDP_LOGIN, data['id'])
                self.__send(dt, addr)
                print(src, "login ok")
                data = generate_json('admin', '', json.dumps(self.online), UDP_LOGIN)
                self.__broadcast(data)
            else:
                # 注册重叠
                dt = generate_json('admin', src, "user already exists", UDP_ERROR, data['id'])
                self.__send(dt, addr)
                print(src, "login failed")
        # 登出请求
        elif data['flag'] == UDP_LOGOUT:
            src = data['from']
            try:
                del self.online[src]
                print(src, "logout")
                data = generate_json('admin', '', json.dumps(self.online), UDP_LOGOUT)
                self.__broadcast(data)
            except KeyError:
                data = generate_json('admin', '', json.dumps(self.online), UDP_LOGOUT)
                self.__broadcast(data)

    # 发消息
    def __send(self, data, addr):
        self.udp.sendto(json.dumps(data).encode(), addr)

    # 广播
    def __broadcast(self, data):
        for (user, addr) in self.online.items():
            if user == 'admin':
                continue
            data['to'] = user
            self.__send(data, addr)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    service = MessageSolver()
    service.show()

    sys.exit(app.exec_())
