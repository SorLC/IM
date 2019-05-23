import socket
import time
import threading
import json

# 在线
online = {}

server_name = socket.getfqdn(socket.gethostname())
server_ip = socket.gethostbyname(server_name)
server_ip = '127.0.0.1'
server_addr = (server_ip, 8888)

# 正常通讯
UDP_NORMAL = 0
# 用户登录
UDP_LOGIN = 1
# 用户登出
UDP_LOGOUT = 2
# 服务器错误
UDP_ERROR = -1
# 服务器退出
UDP_SERVER_EXIT = -2
# 缓冲区大小
BUFF_SIZE = 1024


# 数据打包
def generate_json(src, dest, msg, flag):
    return {'from': src, 'to': dest, 'time': time.ctime(), 'msg': msg, 'flag': flag}


# 向所有人广播
def broadcast(udp, data):
    for (user, addr) in online.items():
        if user == 'admin':
            continue
        data['to'] = user
        udp.sendto(json.dumps(data).encode(), addr)


# 处理来自客户端的消息
def solve(udp):
    while True:
        # 接受消息和地址
        data_json, addr = udp.recvfrom(BUFF_SIZE)
        # data解码
        data = json.loads(data_json.decode())
        print(data)
        if data['flag'] == UDP_NORMAL:
            # 获取目的人名称
            dest = data['to']
            # 查找目的ip
            dest_addr = online.get(dest, None)
            # 目的人为服务器
            if dest == 'admin':
                # 问好
                dt = generate_json('admin', data['from'], f'hello, it is {time.ctime()} now.', UDP_NORMAL)
                # 重定向目的ip为来源
                dest_addr = addr
            elif dest_addr is None:
                # 目的人不存在
                dt = generate_json(
                    'admin', data['from'], 'no such user', UDP_ERROR)
                # 重定向目的ip为来源
                dest_addr = addr
            else:
                # 转发数据包
                dt = data
            # 发送
            udp.sendto(json.dumps(dt).encode(), dest_addr)
            # 打印调试信息
            print(data['from'], "->", dest, dest_addr)
        # 用户登录
        elif data['flag'] == UDP_LOGIN:
            src = data['from']
            if online.get(src, None) is None:
                online[src] = addr
                # 广播在线用户
                dt = generate_json('admin', src, json.dumps(online), UDP_LOGIN)
                broadcast(udp, dt)
                print(src, "login ok")
            else:  # 用户已存在
                dt = generate_json(
                    'admin', src, "user already exists", UDP_ERROR)
                udp.sendto(json.dumps(dt).encode(), addr)
                print(src, "login failed")
        # 用户登出
        elif data['flag'] == UDP_LOGOUT:
            src = data['from']
            del online[src]
            # 广播在线用户
            dt = generate_json('admin', src, json.dumps(online), UDP_LOGOUT)
            broadcast(udp, dt)
            print(src, "logout")


if __name__ == '__main__':
    udpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpServerSocket.bind(server_addr)

    print("server is running", server_addr)
    online['admin'] = server_addr

    # solve多线程
    SolveThread = threading.Thread(target=solve, args=(udpServerSocket,))
    SolveThread.setDaemon(True)
    SolveThread.start()
    SolveThread.join()

    # 服务器退出
    exit_data = generate_json('admin', '', 'server exit', UDP_SERVER_EXIT)
    broadcast(udpServerSocket, exit_data)

    udpServerSocket.close()
