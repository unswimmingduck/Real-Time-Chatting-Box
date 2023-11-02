import socket
from threading import Thread
import time



class Server:
    def __init__(self):
        # 初始化tcp服务器和udp服务器
        self.server_tcp=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_tcp.bind(("127.0.0.1", 8989))
        self.server_tcp.listen(5)

        # 初始化相关表单
        self.clients=[]
        self.clients_name_list = []
        self.clients_str = "list"
        self.clients_name={}
        self.clients_name_ip={}
        
        # 接受相关信息
        self.get_conn()

    # 监听客户端链接
    def get_conn(self):
        while True:
            # 判断客户端是否连接
            client,address=self.server_tcp.accept()

            # 客户端连接之后对相关信息进行接受整理
            self.clients.append(client)
            upload_client_name = client.recv(1024).decode()
            self.clients_name[upload_client_name] = client
            self.clients_name_ip[upload_client_name] = address
            self.clients_name_list.append(upload_client_name)
            
            # 向所有连接的客户端更新表单
            self.update_list(1, client, address)
            
            # 进入线程，接收处理信息 
            Thread(target=self.get_msg,args=(client, self.clients_name, self.clients_name_ip, upload_client_name,)).start()

    def get_msg(self,client:socket.socket,clients_name, clients_name_ip,upload_client_name):
        # 循环监听客户端消息
        while True:
            try:
                # 接受客户端发送来的信息
                self.recv_data=client.recv(1024).decode()
                # 对发送来的信息进行分解
                data = self.recv_data.split("/")
                
                
                # msg/目标客户端匿名/信息/发送客户端昵名/发送时间
                if data[0] == "msg":
                    self.send_msg()     ## 将客户端发来的信息转发给其指定的用户

                # video中信息有三种格式：
                #   video/request/目标服务器/当前服务器
                #   video/decide/是否接收视频/发起视频请求的服务器/决定是否接受的服务器
                elif data[0] == "video":
                    print("video")
                    if data[1] == "request":
                        print("request")
                        clients_name[data[2]].send(str(self.recv_data).encode())
                    elif data[1] == "decide":
                        print("decide")
                        if data[2] == "a":
                            print("agree")
                            print(clients_name_ip[data[-1]])
                            clients_name[data[-2]].send(str("video/agree/" + 
                                                            str(clients_name_ip[data[-1]][0]) + "/" +
                                                            str(clients_name_ip[data[-1]][1])).encode())
                        elif data[2] == "d":
                            print("d")
                            clients_name[data[-2]].send(str("video/decline").encode())     

                # file中发送信息格式不同：
                # file/request/受邀方服务器名称/请求发起方客户端名称
                # file/decide/受邀方决定结果/受邀方客户端名称/请求发起方客户端名称
                elif data[0] == "file":
                    print("file")
                    # 给受邀方发送请求
                    if data[1] == "request":
                        print("request")
                        clients_name[data[2]].send(str(self.recv_data).encode())
                    # 给请求发起端发送受邀方的决定
                    elif data[1] == "decide":
                        print("decide")
                        clients_name[data[-1]].send(str(self.recv_data).encode())
                    # 发送文件的内容
                    elif data[1] == "content":
                        print("content")
                        clients_name[data[-2]].send(str(self.recv_data).encode()) 
                    
            except Exception as e:
                self.close_client(client,upload_client_name)
                break
            # 如果用户输入Q，推出
            if self.recv_data.upper()=="Q":
                self.close_client(client,upload_client_name)
                break

    
    # 关闭资源
    def close_client(self,client,upload_client_name):
        # 关闭相关的客户端
        client.close()
        # 将离开的客户端从相关表单上删除
        self.clients.remove(client)
        self.clients_name_list.remove(upload_client_name)
        del self.clients_name[str(upload_client_name)]
        # 向所有客户端更新删除后的表单
        self.update_list(2, client, upload_client_name)
        # 打印相关客户端离开的信息
        print(upload_client_name+"已经离开")


    def send_msg(self):
        # 得到目标服务器的client
        idx = self.clients.index(self.clients_name[self.recv_data.split("/")[1]])
        # 向目标服务器发送数据
        self.clients[idx].send(str(self.recv_data).encode())

    def update_list(self, idx, client:socket.socket = None, addr = None):
        # 将服务器总注册表单给转化为我们指定的数据格式
        for i in self.clients_name_list:
            self.clients_str += "/" + i 

        # 当客户端刚链接上服务器并更新表单的时候
        if(idx == 1):
            # 将注册过的表单广播并且得到当前所连接的服务器的ip地址和端口号
            for c in self.clients:
                # 向刚链接的服务器端发送其ip地址和端口号
                if c == client:
                    c.send(str(self.clients_str + "/" + str(addr[0]) + "/" + str(addr[1])).encode())
                else:
                    c.send(str(self.clients_str).encode())
        # 当有客户端离开服务器时更新表单
        elif(idx == 2):
            # 将注册过的表单广播 
            for c in self.clients:
                c.send(str(self.clients_str).encode())            
        
        self.clients_str = "list"