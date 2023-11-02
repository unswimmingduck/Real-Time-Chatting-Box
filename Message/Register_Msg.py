from PyQt5 import QtCore, QtGui, QtWidgets, Qt


class Rgs_Message():
    def __init__(self) -> None:
        # 初始化小窗
        self.dialog = QtWidgets.QDialog()
        self.dialog.resize(400,200)
        self.dialog.setWindowTitle("请输入注册信息")  
        # 初始化输入框
        self.editline = QtWidgets.QLineEdit()
        self.editline.setPlaceholderText("请输入您的昵称")  
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
        self.get_client_name = self.editline.text()
        self.dialog.close()