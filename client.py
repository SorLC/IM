import socket
import time
import threading
import json

BUFF_SIZE = 1024
server_addr = ('101.76.221.40', 8888)
username: str
online = {}

UDP_NORMAL = 0
UDP_LOGIN = 1
UDP_LOGOUT = 2
UDP_ERROR = -1


def generate_json(src, dest, msg, flag):
    return {'from': src, 'to': dest, 'time': time.ctime(), 'msg': msg, 'flag': flag}


def _receive(udp):
    data_json, addr = udp.recvfrom(BUFF_SIZE)
    data = json.loads(data_json.decode())
    # print(data, flush=True)
    if data['flag'] == UDP_NORMAL:
        print(f"\r\n[{data['time']}] {data['from']}: ", data['msg'], flush=True)
    elif data['flag'] == UDP_LOGIN or data['flag'] == UDP_LOGOUT:
        global online
        online = json.loads(data['msg'])
        print("\r\n", ",".join(online), "are online now.", flush=True)
    elif data['flag'] == UDP_ERROR:
        print("\r\nerror", data['msg'], flush=True)
    return data


def receive(udp):
    while True:
        _receive(udp)


def send(udp):
    while True:
        dest = input("to>")
        msg = input("say>")
        data = generate_json(username, dest, msg, 0)
        udp.sendto(json.dumps(data).encode(), server_addr)


def login(udp):
    global username
    while True:
        username = input("login as: ")
        data = generate_json(username, 'admin', '', 1)
        udp.sendto(json.dumps(data).encode(), server_addr)
        data = _receive(udp)
        if data['flag'] != -1:
            break
    print("\r\nwelcome!", flush=True)


def logout(udp):
    data = generate_json(username, 'admin', '', 2)
    udp.sendto(json.dumps(data).encode(), server_addr)


if __name__ == '__main__':
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    login(udp)
    ReceiveThread = threading.Thread(target=receive, args=(udp,))
    SendThread = threading.Thread(target=send, args=(udp,))
    ReceiveThread.setDaemon(True)
    ReceiveThread.start()
    # SendThread.setDaemon(True)
    SendThread.start()
    # SendThread.join()
    #

    # ReceiveThread.join()

    while True:
        if threading.active_count() == 0:
            logout(udp)
            udp.close()
