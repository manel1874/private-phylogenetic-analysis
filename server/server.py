##System 

import os

### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtNetwork import *

### Client classes

from server.multi_window_acc import Multi_acc
from server.secure_window_acc import Secure_window_acc
from server.quantum_window_acc import Quantum_window_acc

class Server(qtc.QObject):
    def __init__(self,widget,parent = None):
        super(Server, self).__init__(parent)
        self._server = QTcpServer(self)
        self.widget = widget
        self._clients = {}
        configs = open("config.txt","r")
        self.ip = configs.readline()
        configs.close()
        self.ip = self.ip.split(":")[1].rstrip()
        self.sessionOpened()

    def msgbtn(self):
        return 0

    def sessionOpened(self):
        PORT = 8000
        #change to th local ip of the machine
        address = QHostAddress(self.ip)
        if not self._server.listen(address, PORT):
            return
        self._server.newConnection.connect(self.on_newConnection)

    def on_newConnection(self):
    
        socket = self._server.nextPendingConnection()
        socket.readyRead.connect(self.on_readyRead)

    def on_readyRead(self):
        socket = self.sender()
        bytes_read = socket.readAll()
        invite = str(bytes_read, encoding='ascii')
        clienteIP = invite.split(" ")[2]
        clienteIP2 = ""
        if invite.split(" ")[3] == "and":
            clienteIP2 = invite.split(" ")[4]
        msgBox = qtw.QMessageBox()
        msgBox.setIcon(qtw.QMessageBox.Information)
        msgBox.setText(invite)
        msgBox.setWindowTitle("Invite")
        msgBox.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        msgBox.buttonClicked.connect(self.msgbtn)
        retval = msgBox.exec()
        if retval == 1024:
            if invite[0] == 'C': # Classical Multi-Party Computation
                msg_resp = 'Accepted '+self.ip
                msg_resp = bytes(msg_resp, 'utf-8')
                socket.write(msg_resp)
                #Start server from Classical Multi-Party Computation
                ml = Multi_acc(self.widget,clienteIP,socket)
                self.widget.addWidget(ml)
                self.widget.setCurrentIndex(self.widget.currentIndex()+1)
                self.widget.setFixedHeight(370)
                self.widget.setFixedWidth(574)
                self.close()
            elif invite[0] == 'S':
                msg_resp = 'Accepted '+self.ip
                msg_resp = bytes(msg_resp, 'utf-8')
                socket.write(msg_resp)
                sc = Secure_window_acc(self.widget,clienteIP,clienteIP2,socket)
                self.widget.addWidget(sc)
                self.widget.setCurrentIndex(self.widget.currentIndex()+1)
                self.widget.setFixedHeight(433)
                self.widget.setFixedWidth(645)
                self.close()
                
            elif invite[0] == 'Q':
                #Change to the quantum accept window at this moment its changing to the secure one
                msg_resp = 'Accepted '+self.ip
                msg_resp = bytes(msg_resp, 'utf-8')
                socket.write(msg_resp)
                sc = Quantum_window_acc(self.widget,clienteIP,clienteIP2,socket)
                self.widget.addWidget(sc)
                self.widget.setCurrentIndex(self.widget.currentIndex()+1)
                self.widget.setFixedHeight(521)
                self.widget.setFixedWidth(645)
                self.close()
                
        else:
            if invite[0] == 'C':
                msg_resp = 'Declined '+self.ip
                msg_resp = bytes(msg_resp, 'utf-8')
                socket.write(msg_resp)
                self.close()
            if invite[0] == 'S':
                msg_resp = 'Declined '+self.ip
                msg_resp = bytes(msg_resp, 'utf-8')
                socket.write(msg_resp)
                self.close()
            if invite[0] == 'Q':
                msg_resp = 'Declined '+self.ip
                msg_resp = bytes(msg_resp, 'utf-8')
                socket.write(msg_resp)
                self.close()
                

    def close(self):
        self._server.close()
