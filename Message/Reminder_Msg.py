from PyQt5 import QtCore, QtGui, QtWidgets, Qt



class Message():
    def __init__(self) -> None:
        self.dialog = QtWidgets.QDialog()
        self.dialog.resize(200,200)
        self.dialog.setWindowTitle("提示信息")
        self.panel = QtWidgets.QLabel()
        self.okBtn = QtWidgets.QPushButton("确定")
        self.cancleBtn = QtWidgets.QPushButton("拒绝")
        self.vbox = QtWidgets.QVBoxLayout()
        # Thread(target=self.send_message(), args=(idx)).start()
    
    def send_message(self, idx, ask_name = None):
        
        self.update_dialog(self.vbox)
        self.index = idx
        if idx == 1 :            
            self.panel.setText("用户已连接，请在左侧列表中查找")    
            self.okBtn.clicked.connect(lambda: self.feedback())

            self.vbox.addWidget(self.panel)
            self.vbox.addWidget(self.okBtn)
            self.dialog.setLayout(self.vbox)

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()

        elif idx == 2:
            self.panel.setText("请输入正确的用户昵称")    
            self.okBtn.clicked.connect(lambda: self.feedback())
            
            self.vbox.addWidget(self.panel)
            self.vbox.addWidget(self.okBtn)
            self.dialog.setLayout(self.vbox)

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()       

        elif idx == 3:
            self.panel.setText("文件开始发送")    
            self.okBtn.clicked.connect(lambda: self.feedback())
            

            self.vbox.addWidget(self.panel)
            self.vbox.addWidget(self.okBtn)
            self.dialog.setLayout(self.vbox)

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()                 
    
        elif idx == 4:
            self.panel.setText("文件路径错误")    
            self.okBtn.clicked.connect(lambda: self.feedback())    
            
            self.vbox.addWidget(self.panel)
            self.vbox.addWidget(self.okBtn)
            self.dialog.setLayout(self.vbox)

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()                  
        
        elif idx == 5:
            self.panel.setText("用户： " + ask_name + " 发送来文件，是否接收？")    
            self.okBtn.clicked.connect(lambda: self.file_ask_feedback(1))
            self.cancleBtn.clicked.connect(lambda: self.file_ask_feedback(2))       

            self.vbox.addWidget(self.panel)
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(self.okBtn)
            hbox.addWidget(self.cancleBtn)
            self.vbox.addLayout(hbox)
            self.dialog.setLayout(self.vbox)              

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()  

        elif idx == 6:
            self.panel.setText("文件接收成功，并且接收无异常")    
            self.okBtn.clicked.connect(lambda: self.feedback())

            self.vbox.addWidget(self.panel)
            self.vbox.addWidget(self.okBtn)
            self.dialog.setLayout(self.vbox)

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()      

        elif idx == 7:
            self.panel.setText("文件接收出现问题，请及时联系发送方")    
            self.okBtn.clicked.connect(lambda: self.feedback())
            
            self.vbox.addWidget(self.panel)
            self.vbox.addWidget(self.okBtn)
            self.dialog.setLayout(self.vbox)

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()      

        elif idx == 8:
            self.panel.setText("对方拒绝接收文件")    
            self.okBtn.clicked.connect(lambda: self.feedback())
            
            self.vbox.addWidget(self.panel)
            self.vbox.addWidget(self.okBtn)
            self.dialog.setLayout(self.vbox)

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()      
                                     
            
    def video_send_msg(self,idx, ask_name=None):
        self.update_dialog(self.vbox)
        self.index = idx
        if idx == 1:
            self.panel.setText("用户" + ask_name + "请求进行视频连接")
            self.okBtn.clicked.connect(lambda: self.video_ask_feedback(1))
            self.cancleBtn.clicked.connect(lambda: self.video_ask_feedback(2))


            self.vbox.addWidget(self.panel)
            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(self.okBtn)
            hbox.addWidget(self.cancleBtn)
            self.vbox.addLayout(hbox)
            self.dialog.setLayout(self.vbox)   

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()                                       

        elif idx == 2:
            self.panel.setText("对方拒绝接听")
            self.okBtn.clicked.connect(lambda: self.feedback())
            
            self.vbox.addWidget(self.panel)
            self.vbox.addWidget(self.okBtn)
            self.dialog.setLayout(self.vbox)

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()    
        
        elif idx == 3:
            self.panel.setText("视频通话结束")
            self.okBtn.clicked.connect(lambda: self.video_ask_feedback(3))
            
            self.vbox.addWidget(self.panel)
            self.vbox.addWidget(self.okBtn)
            self.dialog.setLayout(self.vbox)

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
            self.dialog.exec_()               
            
    def video_ask_feedback(self, idx):
        if idx == 1:
            self.dialog.close()
            self.video_decide = "a"
        elif idx == 2:
            self.dialog.close()
            self.video_decide = "d"
        elif idx == 3:
            self.dialog.close()

    def feedback(self):
        self.dialog.close()
        self.index = 0
    
    def file_ask_feedback(self, idx):
        if idx == 1:
            self.dialog.close()
            self.file_decide = "a"
        elif idx == 2:
            self.dialog.close()
            self.file_decide = "d"            

            
    def update_dialog(self, layout):

        item_list = list(range(layout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in item_list:
            item = layout.itemAt(i)
            layout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
            else:
                self.update_dialog(item)
