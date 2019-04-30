import socket
import time
import threading
import json

server_name = 'qingyew.xyz'
server_ip = socket.gethostbyname(server_name)
server_addr = (server_ip, 8888)

username: str
online = {}

UDP_NORMAL = 0
UDP_LOGIN = 1
UDP_LOGOUT = 2
UDP_ERROR = -1

BUFF_SIZE = 1024


def generate_json(src, dest, msg, flag):
    return {'from': src, 'to': dest, 'time': time.ctime(), 'msg': msg, 'flag': flag}


def _receive(udp):
    try:
        data_json, addr = udp.recvfrom(BUFF_SIZE)
        data = json.loads(data_json.decode())
        # print(data, flush=True)
        if data['flag'] == UDP_NORMAL:
            print(f"\r\n[{data['time']}] {data['from']}:", data['msg'], flush=True)
        elif data['flag'] == UDP_LOGIN or data['flag'] == UDP_LOGOUT:
            global online
            online = json.loads(data['msg'])
            print("\r\n", ",".join(online), "are online now.", flush=True)
        elif data['flag'] == UDP_ERROR:
            print("\r\nerror", data['msg'], flush=True)
        return data
    except ConnectionResetError:
        print("server", server_ip, "is offline")
        logout(udp)
        udp.close()
        exit(0)


def _send(udp, data):
    udp.sendto(json.dumps(data).encode(), server_addr)


def receive(udp):
    while True:
        _receive(udp)


def send(udp):
    while True:
        dest = input("to>")
        msg = input("say>")
        data = generate_json(username, dest, msg, 0)
        _send(udp, data)


def login(udp):
    global username
    while True:
        username = input("login as: ")
        data = generate_json(username, 'admin', '', 1)
        _send(udp, data)
        data = _receive(udp)
        if data['flag'] != -1:
            break
        print(username, 'has been already registered')
    print("\r\nWelcome!", flush=True)


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
    SendThread.start()
