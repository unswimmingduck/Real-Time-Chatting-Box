from PyQt5.QtWidgets import *
import sys


from Client.client import Client

app = QApplication(sys.argv)
ui = Client()
ui.show()
sys.exit(app.exec_())   