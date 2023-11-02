from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from threading import Thread, Event
import socket
import time
import cv2
import numpy as np
import os
import hashlib


from Message.Register_Msg import Rgs_Message
from Message.Reminder_Msg import Message
from Message.File_Msg import file_Message


class Client(QtCore.QObject):    
    
    update_text = QtCore.pyqtSignal(str)
    video_request = QtCore.pyqtSignal(str)
    video_start = QtCore.pyqtSignal(str)
    video_decline = QtCore.pyqtSignal(str)
    video_stop = QtCore.pyqtSignal(str)
    
    file_request = QtCore.pyqtSignal(str)
    file_start = QtCore.pyqtSignal(str)
    file_decline = QtCore.pyqtSignal(str)
    file_success = QtCore.pyqtSignal(str)
    file_erro = QtCore.pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.main_widget = QtWidgets.QWidget()

        # 初始化通讯方式
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 对udp通信进行初始化
        self.client_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        # self.client_udp_add = ("127.0.0.1",8989)

        # 初始化注册小框，并得到相关注册信息
        self.rgs_msg = Rgs_Message() 
        self.client_name = str(self.rgs_msg.get_client_name)

        # 连接服务器，并向服务器中注册昵称
        self.client.connect(("127.0.0.1",8989))
        self.client.send(self.client_name.encode())


        # 获取服务器上服务器注册表单,并且在该表单上剔除自己
        self.clients_list = (self.client.recv(4028).decode()).split("/")
        self.client_ip = []
        self.client_ip.append(str(self.clients_list[-2]))
        self.client_ip.append(int(self.clients_list[-1]))

        self.clients_list.remove(self.client_name)
        self.clients_list.remove("list")
        del self.clients_list[-1]       ## 删除信息里面的ip信息
        del self.clients_list[-1]       ## 删除信息里面的端口信息
        # print(self.clients_list)

        # 初始化相关列表即参数
        self.num_connected_cline = 0        ## 该服务器连接其他服务器的个数
        self.client_connceted_list = []     ## 已连接的其他服务器的昵称
        self.TB_list = []                   ## 与每个服务器通信中聊天框的组件
        self.Thread_recv_list = []          ## 接收消息线程的表单
        self.Thread_event_list = []         ## 线程事件表单
        self.recv_data_content = []         ## 消息接收内容
        self.recv_data_id = []              ## 接收到消息方的id
        self.video_ask_client = []          ## 发送视频请求的客户端名称
        self.client_udp_ip_port = []        ## 存储进行视频通话时所要连接的udp的地址和端口
        self.aim_clinet_udp_ip_port = []    ## 在询问受邀请方是否接受视频的时候存储邀请方客户端的ip

        self.file_ask_client = []           ## 发送文件请求方客户端名称
        self.file_size = []                 ## 所发送文件的大小
        self.file_md_recv = []              ## 接收文件后所得到的md加密码
        self.file_recv_name = []            ## 接收文件的文件名

        # 初始化信息框
        self.msg = Message()
        

        self.update_text.connect(self.updateText)
        self.video_request.connect(self.video_request_ask)
        self.video_start.connect(self.video_process)
        self.video_decline.connect(self.video_decline_process)
        self.video_stop.connect(lambda: self.msg.video_send_msg(3))
        
        self.file_request.connect(self.file_request_ask)
        self.file_start.connect(self.file_process)
        self.file_decline.connect(self.file_decline_process)
        self.file_success.connect(lambda: self.msg.send_message(6))
        self.file_erro.connect(lambda: self.msg.send_message(7))

        self.setupUi(self.main_widget)

        
# 初始化聊天程序总体UI
    def setupUi(self, Form):
        
        Form.setObjectName("Chat_APP")
        Form.resize(846, 783)
        Form.setWindowTitle("当前用户为：" + str(self.client_name))
        
        # 右侧聊天款用groupbox进行初始化
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(260, 10, 561, 751))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")


        # group中的wiget
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(10, 50, 541, 691))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")


        # 左侧窗口初始化
        self.widget1 = QtWidgets.QWidget(Form)
        self.widget1.setGeometry(QtCore.QRect(20, 20, 221, 741))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # 提前申明已连接用户，提前申明ListWidget
        self.listWidget_4 = QtWidgets.QListWidget(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_4.sizePolicy().hasHeightForWidth())
        self.listWidget_4.setSizePolicy(sizePolicy)
        self.listWidget_4.setObjectName("listWidget_4")               

        # 左侧editline搜索框初始化
        self.lineEdit_left = QtWidgets.QLineEdit(self.widget1)
        self.completer = QtWidgets.QCompleter(list(self.clients_list))   
        self.lineEdit_left.setCompleter(self.completer)
        self.lineEdit_left.setPlaceholderText("输入所要联系用户的昵名")        
        self.lineEdit_left.setText("")
        self.lineEdit_left.setObjectName("lineEdit_left")
        self.verticalLayout.addWidget(self.lineEdit_left)
        self.lineEdit_left.textEdited.connect(lambda: self.update_completer())
        self.lineEdit_left.returnPressed.connect(lambda: self.get_cline_id())   ## 按下回车键后开始搜索

        #设置ListWiget位置 
        self.verticalLayout.addWidget(self.listWidget_4)


        #申明stacked
        self.stacked = QtWidgets.QStackedWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(16)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stacked.sizePolicy().hasHeightForWidth())    
        
        # 开启接收消息的进程
        self.Thread_recv()
        QtCore.QMetaObject.connectSlotsByName(Form)

        

####################################聊天框函数#########################################
    # 获取目标服务器聊天框
    def get_cline_id(self):
        # 获取输入的用户名昵称
        self.aim_client = self.lineEdit_left.text()
        self.lineEdit_left.clear()

        # 判断输入的昵称是否合法
        if self.aim_client not in self.client_connceted_list and self.aim_client in self.clients_list:
            self.get_connect()
        elif self.aim_client not in self.clients_list:
            self.msg.send_message(2)            
        elif self.aim_client in self.client_connceted_list:
            self.msg.send_message(1)

    # 连接目标客户端并初始化聊天框
    def get_connect(self):
        # 在ListWidget中插入项目
        self.listWidget_4.insertItem(self.num_connected_cline, self.aim_client)
        self.num_connected_cline += 1
        self.client_connceted_list.append(self.aim_client)

        # 初始化聊天框中按键
        self.pushButton_13 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_13.setGeometry(QtCore.QRect(10, 18, 93, 28))
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_13.setText("返回主页")

        # 初始化与groupbox相关的数据
        pushButton_13 = QtWidgets.QPushButton(self.groupBox)
        pushButton_13.setGeometry(QtCore.QRect(10, 18, 93, 28))
        pushButton_13.setObjectName("pushButton_13")
        

        # group中的wiget
        widget = QtWidgets.QWidget()
        widget.setGeometry(QtCore.QRect(10, 50, 541, 691))
        widget.setObjectName("widget")
        verticalLayout_2 = QtWidgets.QVBoxLayout()
        verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        verticalLayout_2.setObjectName("v")
        TextBrowser = QtWidgets.QTextBrowser()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(TextBrowser.sizePolicy().hasHeightForWidth())
        TextBrowser.setSizePolicy(sizePolicy)
        TextBrowser.setObjectName("TextBrowser")
        verticalLayout_2.addWidget(TextBrowser)
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setObjectName("horizontalLayout")

        
        # 初始化按键
        pushButton_2 = QtWidgets.QPushButton()
        pushButton_2.setObjectName("pushButton_2")
        pushButton_2.setText("视频通话")
        pushButton_2.clicked.connect(self.video_key)        ## 将Video按键关联到self.video_key中
        horizontalLayout.addWidget(pushButton_2)

        pushButton = QtWidgets.QPushButton()
        pushButton.setObjectName("pushButton")
        pushButton.setText("发送文件")
        horizontalLayout.addWidget(pushButton)
        pushButton.clicked.connect(self.file_key)           ## 将file按键关联到self.file_key中

        verticalLayout_2.addLayout(horizontalLayout)


        editline = QtWidgets.QLineEdit()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(editline.sizePolicy().hasHeightForWidth())
        editline.setSizePolicy(sizePolicy)
        editline.setObjectName("editline")
        verticalLayout_2.addWidget(editline)
        editline.returnPressed.connect(lambda: self.send_message(editline))
        widget.setLayout(verticalLayout_2)
        
        self.TB_list.append(TextBrowser)
        self.stacked.addWidget(widget)
        self.verticalLayout_2.addWidget(self.stacked)
        self.listWidget_4.currentRowChanged.connect(self.display)
        
        # 开启接收消息的进程
        self.Thread_recv() 
######################################################################################        

        

####################################更新类函数#########################################
    # 更新comlpeter表单
    def update_completer(self):
        self.completer = QtWidgets.QCompleter(list(self.clients_list)) 
        self.lineEdit_left.setCompleter(self.completer)

    # 更新stackedwiget 
    def display(self, index):
        # 更新stackedwiget
        self.stacked.setCurrentIndex(index)
        # 更新groupbox里的标签，显示现在是与谁的聊天框
        self.aim_client = self.listWidget_4.item(index).text()
        self.groupBox.setTitle(self.aim_client)

    # 更新聊天框聊天内容
    def updateText(self):
        self.TB_list[self.recv_data_id[-1]].append(str("User: " + self.recv_data_content[-1].split("/")[0]))
        self.TB_list[self.recv_data_id[-1]].append(str( "     " +self.recv_data_content[-1].split("/")[1]))
        self.recv_data_id.clear()
        self.recv_data_content.clear()
        
################################################################################# 
    

        
########################################视频通话函数#######################################         
    # video按键关联函数
    def video_key(self):
        # 初始化摄像头,并设置分辨率
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # 向server发送video请求
        self.client.send(str("video/request/" + self.aim_client + "/"  + self.client_name + "/" + 
                             str(self.client_ip[0]) + "/" + str(self.client_ip[1])).encode())        

    # video请求函数
    def video_request_ask(self):
        # 生成弹窗，并获得是否接受视频请求
        self.msg.video_send_msg(1, self.video_ask_client[-1])
        self.video_decide = str(self.msg.video_decide)
        # 向server发送决定结果， 格式为： video/decide/决定结果/视频请求方/当前客户名（即被邀请方）
        print("video_decide: ",self.video_decide)
        print("video_ask_client: ", self.video_ask_client)
        print("client_name: ", self.client_name)
        self.client.send(str("video/decide/" + str(self.video_decide) + "/" + str(self.video_ask_client[-1]) + "/" + str(self.client_name)).encode())
        print("send completely")
        
        # 清空邀请方表单
        self.video_ask_client.clear()
        # 如果决定结果为接受，则开启接受数据，并呈现实时视频
        if(self.video_decide == "a"):
            # 初始化摄像头
            # self.cap = cv2.VideoCapture(0)
            # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            # Thread(target=self.video_send_process, args=(self.cap, self.client_udp, self.aim_clinet_udp_ip_port, )).start()
            Thread(target=self.recv_video, args=(self.client_udp, self.client_ip, )).start()
        
        # 清空邀请方地址表单
        self.aim_clinet_udp_ip_port.clear()

    # 拒绝视频通话函数
    def video_decline_process(self):
        self.cap.release()
        self.msg.video_send_msg(2, self.video_ask_client[-1])

    # 视频通话线程函数 
    def video_process(self):
        print("video_send_msg")
        # Thread(target=self.recv_video, args=(self.client_udp, self.client_ip, )).start()
        Thread(target=self.video_send_process, args=(self.cap, self.client_udp, self.client_udp_ip_port,)).start()        

    # 接收视频通话数据函数
    def recv_video(self, udp:socket.socket, client_ip:list):
        print("recv_video")
        udp.bind(tuple(client_ip))
        while True:
            data = None
            try:
                data, _ = udp.recvfrom(921600)
                receive_data = np.frombuffer(data, dtype='uint8')
                r_img = cv2.imdecode(receive_data, 1)

                cv2.putText(r_img, "server", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow('server', r_img)
            except BlockingIOError as e:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    # 视频通话发送数据函数
    def video_send_process(self, cap, udp:socket.socket, udp_ip_port: list):
        while True:
            _, img = cap.read()             
            img = cv2.flip(img, 1)
            # 压缩图片
            _, send_data = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 50])

            udp.sendto(send_data, tuple(udp_ip_port))

            print(f'正在发送数据，大小:{img.size} Byte')

            cv2.putText(img, "client", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('client', img)
           
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("stop video")
                cap.release()
                self.client_udp_ip_port.clear()
                break

        udp.close()
        cv2.destroyAllWindows()

#################################################################################################        


        
##################################################发送数据函数#####################################
                 
    # 发送数据，数据发送格式为：msg(数据格式)/接收客户端昵名/数据/发送该数据的客户端昵名/发送时间
    def send_message(self, editline):
        # 获取输入的信息
        msg_raw = editline.text()
        # 对输入的信息进行分装
        msg = str("msg" + "/" + self.aim_client + '/' + msg_raw + '/' + self.client_name + "/" + time.strftime("%x"))
        # 对封装完的信息进行发送，发送给服务器处理
        self.client.send(msg.encode())
        # 在小聊天框中显示自己发送的内容
        idx = self.client_connceted_list.index(self.aim_client)
        self.TB_list[idx].append(str("User: " + self.client_name + "     " + "Time: " + time.strftime("%x")))
        self.TB_list[idx].append(str( "     " + msg_raw))
        # 清空输入框内的消息
        editline.clear()
    
    # 接收数据函数
    def recv_data(self,
                  client:socket.socket, 
                  client_udp:socket.socket, 
                  client_name:str, 
                  clients_list: list, 
                  client_connceted_list:list, 
                  data_content:list, 
                  idx_list:list, 
                  video_ask_client:list,
                  client_udp_ip_port:list,
                  aim_clinet_udp_ip_port:list,
                  file_ask_client:list,
                  file_size:list,
                  md_recv:list,
                  file_name:list,
                  event: Event):
        data_size = 1048
        while True:
            try:
                # 接收消息
                data = client.recv(data_size).decode()
                # 将封装过的消息进行拆解
                data = str(data).split("/")
                
                # 接收数据，并把数据显示在TextBrowser上
                if(data[0] == "msg"):
                    # 将拆解过的分装消息中的具体发送内容更新到聊天框上
                    idx_list.append(client_connceted_list.index(data[3]))
                    data_content.append(str(data[-4] + "     Time: " + data[-3] + "-" + data[-2] + "-" + data[-1] + "/" + data[2]))
                    self.update_text.emit("text_update")
                
                # 接收client注册表单，并更新表单
                elif(data[0] == "list"): 
                    data.remove("list")
                    # 更新表单
                    for i in data:
                        print(i)
                        if i not in clients_list:
                            clients_list.append(i)
                    clients_list.remove(client_name)
                
                # 当接受的消息为video类型的时候
                elif(data[0] == "video"):
                    print("video")
                    # 当消息为video请求的时候
                    if(data[1] == "request"):
                        print("request")
                        video_ask_client.append(data[-3])       ## 接受请求视频的客户端名称
                        aim_clinet_udp_ip_port.append(str(data[-2])) ## 接受请求视频方的客户端ip
                        aim_clinet_udp_ip_port.append(int(data[-1])) ## 接受请求视频方的客户端ip中的端口号
                        self.video_request.emit("video ask")    ## 开启询问是否开启视频
                    # 当消息为首邀请方同意视频的时候
                    elif(data[1] == "agree"):
                        print("agree")
                        ## 存储受邀请方的的ip和端口
                        client_udp_ip_port.append((data[-2])) 
                        client_udp_ip_port.append(int(data[-1])) 
                        print(client_udp_ip_port)   
                        self.video_start.emit("start")              ## 触发视频开启函数
                    elif(data[1] == "decline"):
                        print("decline")
                        self.video_decline.emit("decline")          ## 触发视频关闭函数
                
                # 发送文件的数据格式 "file/request/目标客户端名称/文件传输发起端客户端名称
                elif(data[0] == "file"):
                    # 接收到文件发送请求的数据
                    if(data[1] == "request"):
                        print("request")        
                        file_ask_client.append(data[-1])            ## 存储文件传输发起端名称
                        self.file_request.emit("file request")      ## 进行文件
                    # 接收到文件接收端发来的对于文件传输请求的决定
                    elif(data[1] == "decide"):
                        if(data[2] == "a"):                         ## 收到接收端发来的同意接收决定
                            self.file_start.emit("file transition start")       ## 开始发送文件
                        elif(data[2] == "d"):                       ## 收到接收端发来的拒绝接绝决定
                            self.file_decline.emit("file transition is declined")   ## 生成拒绝接收弹窗
                    # 接收到文件传输发起端发送来的文件内容
                    elif(data[1] == "content"):
                        if(data[2] == "name"):
                            file_name.append(os.path.split(data[-1])[-1])
                        elif(data[2] == "size"):                      ## 接收文件传输中文件的大小
                            file_size.append(int(data[-2]))
                        elif(data[2] == "info"):                    ## 接收文件传输中文件的具体内容
                            print("info")
                            # 打开文件夹
                            f = open(str("new_" + file_name[-1]), "wb")
                            m = hashlib.md5()
                            byte_info = str(data[-1]).encode()
                            m.update(byte_info)
                            f.write(byte_info)
                            f.close()
                            md_recv.append(m.hexdigest())
                        elif(data[2] == "md"):
                            print("md")
                            md_code = (data[-1]).encode()
                            print(md_recv[-1])
                            # md验证码正确，生成文件接收成功弹窗
                            if(md_code == md_recv[-1]):
                                print("md_success")
                                md_recv.clear()
                                self.file_success.emit("file transition successful")
                            # md验证码步正确，生成文件接收成功弹窗
                            else:
                                print("md_fail")
                                md_recv.clear()
                                self.file_erro.emit("file transition has some erro")

            except:
                # exit()
                pass

            if event.isSet():
                print("break")
                break

    # 接收数据线程函数
    def Thread_recv(self):
        # 更新线程程序
        
        if len(self.Thread_recv_list) != 0 :
            print("set")
            self.Thread_event_list[-1].set()
            self.event = Event()    # 关闭上一个线程循环
            self.Thread_recv_work = Thread(target=self.recv_data,
                                           args=(self.client, self.client_udp, self.client_name, self.clients_list, self.client_connceted_list, 
                                                 self.recv_data_content, self.recv_data_id, self.video_ask_client, 
                                                 self.client_udp_ip_port, self.aim_clinet_udp_ip_port, self.file_ask_client,
                                                 self.file_size, self.file_md_recv, self.file_recv_name,
                                                 self.event,)).start()
            self.Thread_recv_list.append(self.Thread_recv_work)     ##  线程的类收集在表单中
            self.Thread_event_list.append(self.event)               ##  将event收集在表单中

        # 第一次启动线程
        else:
            self.event = Event()
            self.Thread_recv_work = Thread(target=self.recv_data,
                                           args=(self.client, self.client_udp, self.client_name, self.clients_list, self.client_connceted_list, 
                                                 self.recv_data_content, self.recv_data_id, self.video_ask_client, 
                                                 self.client_udp_ip_port , self.aim_clinet_udp_ip_port, self.file_ask_client, 
                                                 self.file_size, self.file_md_recv, self.file_recv_name,
                                                 self.event,)).start()
            self.Thread_recv_list.append(self.Thread_recv_work)     ##  线程的类收集在表单中
            self.Thread_event_list.append(self.event)               ##  将event收集在表单中

################################################################################################# 



###########################################文件发送函数####################################       

    def file_key(self):
        # 进入到有关file的弹窗当中
        self.file_msg = file_Message()
        # 如果输入的文件路径正确，向server中发送相关信息，数据发送格式为：file/request/受邀方服务器名称/请求发起方客户端名称
        if(self.file_msg.file_path != None):
            self.client.send(str("file/request/" + self.aim_client + "/" + self.client_name).encode())

    def file_request_ask(self):
        # 进入文件请求交互界面，决定是否接收文件
        self.msg.send_message(5, self.file_ask_client[-1])
        # 向服务端发送接收端决定 
        self.client.send(str("file/decide/"+ self.msg.file_decide + "/" + self.client_name + "/" + self.file_ask_client[-1]).encode())
        self.file_ask_client.clear()
            
    def file_process(self):
        # 接收端同意接收文件，开启发送文件线程
        path = self.file_msg.file_path
        self.client.send(str("file/content/name/" + self.aim_client + "/" + path).encode())
        Thread(target=self.send_file, args=(self.client, path, self.aim_client, )).start()
    
    def send_file(self, client:socket.socket, file_path, aim_client):    
        # 得到文件大小
        file_size = os.stat(file_path).st_size
        # 向受邀方发送文件的大小
        client.send(str("file/content/size/" + aim_client + "/" + str(file_size) ).encode())
        # 生成md校验码
        m = hashlib.md5()
        # 打开目标文件
        f = open(file_path, "rb")
        # 逐行读取并发送，每行更新md校验码
        for line in f:
            try:
                client.send(("file/content/info/" + aim_client+ "/").encode() + line)  # 发送数据
                m.update(line)
                time.sleep(0.01)
                print("lien")
            except:
                pass
                
        # 发送完，关闭文件指针
        f.close()

        try:
            # 生成最终md校验码，并通过tcp协议发送给接收文件的客户端
            md5 = m.hexdigest()
            client.send(str("file/content/md/" + aim_client + "/" + md5).encode())  # 发送md5值
        except:
            pass
            
    def file_decline_process(self):
        self.msg.send_message(8)
        

################################################################################################# 

            
    def show(self):
        self.main_widget.show()