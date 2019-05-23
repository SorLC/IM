# -*- coding:utf8 -*-

import time

UDP_NORMAL = 0
UDP_LOGIN = 1
UDP_LOGOUT = 2
UDP_ERROR = -1
UDP_TIMEOUT = -2
UDP_SERVER_EXIT = -3
UDP_CHECK_ALIVE = 3

BUFF_SIZE = 1024


def generate_json(src, dest, msg, flag, _id=0):
    return {'id': _id, 'from': src, 'to': dest, 'time': time.ctime(), 'msg': msg, 'flag': flag}
