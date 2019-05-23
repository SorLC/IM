# -*- coding:utf8 -*-
import sys

from PyQt5 import QtWidgets
from util.MainWindow import MainWindow

if __name__ == '__main__':
    server_name = 'qingyew.xyz'
    # server_ip = socket.gethostbyname(server_name)
    server_ip = '127.0.0.1'

    app = QtWidgets.QApplication(sys.argv)
    
    main = MainWindow(server_ip)
    main.show()

    sys.exit(app.exec_())
