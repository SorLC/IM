# -*- coding:utf8 -*-
import sys
import socket

from PyQt5 import QtWidgets
from util.MainWindow import MainWindow

if __name__ == '__main__':
    server_name = 'qingyew.xyz'
    server_ip = socket.gethostbyname(server_name)

    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow(server_ip)
    main.show()

    sys.exit(app.exec_())
