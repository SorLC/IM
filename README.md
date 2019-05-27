# IM

###### First Demo

简单命令行界面，没有解决线程之间切换的问题，没有解决正常退出的问题。

`client.py`为客户端

`server.py`为服务器端

`client.py`需设置`server_addr`元组为服务器ip地址及端口号，首次打开需要注册ID，发送信息需要先指定ID再输入消息。

###### Second Demo

服务器与客户端均实现图形化界面并解决了线程不同步的问题以及不能正常退出的问题

---

###### 现版 v1.0

+ 打开时需要注册，名称不能重复
+ 左侧是在线列表，双击选中用户
+ 右上方为信息接受窗口
+ 右下方为信息发送窗口，enter键发送消息
+ sendf按钮可以发送文件，目前没有提示信息，保存在运行目录下，文件名有save_前缀
+ send按钮发送普通文本消息
+ 正常退出会自动登出，但如果发生运行时错误则不能正常登出，会导致服务器不能正常更新在线列表，导致左侧在线列表出现更新不及时或者不更新的情况

