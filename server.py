import socket
import time
import threading
import json

online = {}

BUFF_SIZE = 1024
server_addr = ('127.0.0.1', 8888)

UDP_NORMAL = 0
UDP_LOGIN = 1
UDP_LOGOUT = 2
UDP_ERROR = -1
UDP_SERVER_EXIT = -2


def generate_json(src, dest, msg, flag):
    return {'from': src, 'to': dest, 'time': time.ctime(), 'msg': msg, 'flag': flag}


def broadcast(udp, data):
    for (user, addr) in online.items():
        if user == 'admin':
            continue
        data['to'] = user
        udp.sendto(json.dumps(data).encode(), addr)


def solve(udp):
    while True:
        data_json, addr = udp.recvfrom(BUFF_SIZE)
        data = json.loads(data_json.decode())
        print(data)
        if data['flag'] == UDP_NORMAL:
            dest = data['to']
            dest_addr = online.get(dest, None)
            if dest == 'admin':
                dt = generate_json('admin', data['from'], f'hello, it is {time.ctime()} now.', UDP_NORMAL)
                dest_addr = addr
            elif dest_addr is None:
                dt = generate_json('admin', data['from'], 'no such user', UDP_ERROR)
                dest_addr = addr
            else:
                dt = data
            udp.sendto(json.dumps(dt).encode(), dest_addr)
            print(data['from'], "->", dest, dest_addr)
        elif data['flag'] == UDP_LOGIN:
            src = data['from']
            if online.get(src, None) is None:
                online[src] = addr
                dt = generate_json('admin', src, json.dumps(online), UDP_LOGIN)
                broadcast(udp, dt)
                print(src, "login ok")
            else:
                dt = generate_json('admin', src, "user already exists", UDP_ERROR)
                udp.sendto(json.dumps(dt).encode(), addr)
                print(src, "login failed")
        elif data['flag'] == UDP_LOGOUT:
            src = data['from']
            del online[src]
            dt = generate_json('admin', src, json.dumps(online), UDP_LOGOUT)
            broadcast(udp, dt)
            print(src, "logout")


if __name__ == '__main__':
    udpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpServerSocket.bind(server_addr)
    online['admin'] = server_addr
    SolveThread = threading.Thread(target=solve, args=(udpServerSocket,))
    SolveThread.setDaemon(True)
    SolveThread.start()
    SolveThread.join()

    exit_data = generate_json('admin', '', 'server exit', UDP_SERVER_EXIT)
    broadcast(udpServerSocket, exit_data)

    udpServerSocket.close()
    # # ReceiveThread = threading.Thread(target=receive, args=(udpCliSocket, ))
    #
    # while True:
    #     data, add = udpCliSocket.recvfrom(BUFF_SIZE)
    #     if not data:
    #         break
    #     print(f"from {add}", data.decode())
    #     res = input("say>")
    #     udpCliSocket.sendto(f"[{time.ctime()}] {res}".encode(), add)
    #
    # udpCliSocket.close()
