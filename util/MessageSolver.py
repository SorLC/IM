# -*- coding:utf8 -*-
import json
from util.tools import *
from PyQt5.QtCore import pyqtSignal, QThread


class MessageSolver(QThread):
    receiveMessage = pyqtSignal(dict)

    def __init__(self, udp, server_addr):
        super().__init__()
        self.udp = udp
        self.server_addr = server_addr

    def run(self):
        while True:
            try:
                data_json, addr = self.udp.recvfrom(BUFF_SIZE)
                data = json.loads(data_json.decode())
                self.receiveMessage.emit(data)
            except ConnectionResetError:
                self.receiveMessage.emit(generate_json("admin", '', "Server is offline", UDP_SERVER_EXIT))

    def send(self, data):
        # print("send", data)
        self.udp.sendto(json.dumps(data).encode(), self.server_addr)
