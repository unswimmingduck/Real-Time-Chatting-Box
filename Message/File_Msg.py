from Message.Reminder_Msg import Message
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import os



class file_Message():
    def __init__(self) -> None:
        # 初始化小窗
        self.dialog = QtWidgets.QDialog()
        self.dialog.resize(400,200)
        self.dialog.setWindowTitle("请配置文件发送相关信息")  
        # 初始化输入框
        self.editline = QtWidgets.QLineEdit()
        self.editline.setPlaceholderText("请输入所要发送文件的路径")  
        # 初始化按键
        self.okBtn = QtWidgets.QPushButton("确定")
        self.okBtn.clicked.connect(self.send_msg)
        # 设置小窗布局
        vbox=QtWidgets.QVBoxLayout()
        vbox.addWidget(self.editline)
        vbox.addWidget(self.okBtn)
        self.dialog.setLayout(vbox)

        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
        self.dialog.exec_()    


    def send_msg(self):
        file_result_feedback = Message() 
        path = str(self.editline.text())
        if os.path.exists(path):
            self.file_path = path
            file_result_feedback.send_message(3)
        else:
            self.file_path = None
            file_result_feedback.send_message(4)
        self.editline.clear()
        self.dialog.close()
