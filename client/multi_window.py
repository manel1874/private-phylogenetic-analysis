### System
import requests
import socket
import os
import shutil
### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore, QtNetwork

### Client classes
from interface.Multi_party2 import Multi


### Common class
from common.compute import Compute_Window

class Multi_window(qtw.QWidget):

    def __init__(self, widget,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.ui = Multi()
        self.ui.setupUi(self)
        self.ui.pushButton_13.setHidden(True)
        self.ui.pushButton_16.setHidden(True)
        self.ui.lineEdit_3.setHidden(True)
        self.ui.lineEdit_4.setHidden(True)
        self.ui.checkBox.setHidden(True)
        self.ui.checkBox_2.setHidden(True)
        self.ui.checkBox_3.setHidden(True)
        self.ui.checkBox_4.setHidden(True)
        self.ui.spinBox.setMaximum(2)
        self.ui.spinBox.setMinimum(1)
        #connect the buttons to the functions
        self.ui.pushButton_12.clicked.connect(self.apply)
        self.ui.pushButton_13.clicked.connect(self.invite1)
        self.ui.pushButton_16.clicked.connect(self.invite2)
        self.ui.pushButton_7.clicked.connect(self.add)
        self.ui.pushButton_8.clicked.connect(self.delete)
        self.ui.pushButton_9.clicked.connect(self.clear)
        self.files = []
        #Define the socket to connect to party 1
        self._socket = QtNetwork.QTcpSocket(self)
        self._socket.stateChanged.connect(self.on_stateChanged)
        self.ui.pushButton_10.clicked.connect(self.compute)
        self._socket.readyRead.connect(self.on_readyRead)
        #Read the ip from the config file
        configs = open("config.txt","r")
        self.ip = configs.readline()
        configs.close()
        self.ip = self.ip.split(":")[1].rstrip()
        self.widget = widget
        #Booleans to verify if the client as to send the sequences or not
        self.accept1 = False
        self.accept2 = False
        #Define the socket to connect to party 2
        self._socket2 = QtNetwork.QTcpSocket(self)
        self._socket2.stateChanged.connect(self.on_stateChanged2)
        self._socket2.readyRead.connect(self.on_readyRead2)
    
    #-----------------------SOCKETs_FOR_PARTY1------------------------
    #Runs when the socket tries to connect
    def on_stateChanged(self, state):
        if state == QtNetwork.QAbstractSocket.ConnectedState:
            msg = "Classical Multiparty " + self.ip + " Number of Sequences: " + str(len(self.files))
            self.sendMessage(bytes (msg,'utf-8'))
        elif state == QtNetwork.QAbstractSocket.UnconnectedState:
            print("disconnected")
            
    #Read mensages from party 1
    def on_readyRead(self):
        Response = self._socket.readAll()


        if Response.split(" ")[0] == "Accepted":
            if Response.split(" ")[1] == self.ui.lineEdit_3.text():
                self.accept1 = True
                self.ui.checkBox.setChecked(True)
            else:
                self.ui.checkBox_3.setChecked(True)

        if Response.split(" ")[0] == "Declined":
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Information)
            msgBox.setText("Party " + self.ui.lineEdit_3.text() + " has declined the invite")
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            msgBox.buttonClicked.connect(self.msgbtn)
            retval = msgBox.exec()
            
        if Response.split(" ")[0] == "Sequences":
            if Response.split(" ")[1] == self.ui.lineEdit_3.text():
                self.ui.checkBox_2.setChecked(True)
            else:
                self.ui.checkBox_4.setChecked(True)
    
    def sendMessage(self,message):
        if self._socket.state() == QtNetwork.QAbstractSocket.ConnectedState:
            bytes_read = message
            self._socket.write(bytes_read)

    #-----------------------SOCKETs_FOR_PARTY2------------------------
    #Runs when the socket tries to connect
    def on_stateChanged2(self, state):
        if state == QtNetwork.QAbstractSocket.ConnectedState:
            #self._timer.start()
            msg = "Classical Multiparty " + self.ip + " Number of Sequences: " + str(len(self.files))
            self.sendMessage2(bytes (msg,'utf-8'))
        elif state == QtNetwork.QAbstractSocket.UnconnectedState:
            print("disconnected")
            #QtCore.QCoreApplication.quit()

    #Read mensages from party 2
    def on_readyRead2(self):
        Response = self._socket2.readAll()

        
        if Response.split(" ")[0] == "Accepted":
            if Response.split(" ")[1] == self.ui.lineEdit_4.text():
                self.accept2 = True
                self.ui.checkBox_3.setChecked(True)
            else:
                self.ui.checkBox.setChecked(True)


        if Response.split(" ")[0] == "Declined":
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Information)
            msgBox.setText("Party " + self.ui.lineEdit_4.text() + " has declined the invite")
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            msgBox.buttonClicked.connect(self.msgbtn)
            retval = msgBox.exec()


        if Response.split(" ")[0] == "Sequences":
            if Response.split(" ")[1] == self.ui.lineEdit_4.text():
            
                self.ui.checkBox_4.setChecked(True)
            else:
                self.ui.checkBox_2.setChecked(True)
        

    def sendMessage2(self,message):
        if self._socket2.state() == QtNetwork.QAbstractSocket.ConnectedState:
            bytes_read = message
            self._socket2.write(bytes_read)

    def msgbtn(self):
        return 0

    #Send the files via the flask server
    def sendFile(self,urlDef):
        Sequences_path = os.path.dirname(__file__) + '/../Selected_Sequences/'
        arr = os.listdir(Sequences_path)
        for file in arr:
            file = {'upload_file': open(Sequences_path + file,"rb")}
            url = 'http://' + urlDef + ':8090/fileServer'
            x = requests.post(url,files = file)

    def invite1(self):
        try:
            address = self.ui.lineEdit_3.text()
            socket.inet_aton(self.ui.lineEdit_3.text())
        except socket.error:
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Information)
            msgBox.setText("Invalid IP address")
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            msgBox.buttonClicked.connect(self.msgbtn)
            retval = msgBox.exec()
            return 0
        self._socket.connectToHost(QtNetwork.QHostAddress(address), 8000)
    

    def invite2(self):  
        try:
            address = self.ui.lineEdit_4.text()
            socket.inet_aton(self.ui.lineEdit_4.text())
        except socket.error:
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Information)
            msgBox.setText("Invalid IP address")
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            msgBox.buttonClicked.connect(self.msgbtn)
            retval = msgBox.exec()
            return 0
      
        self._socket2.connectToHost(QtNetwork.QHostAddress(address), 8000)

    def apply(self):
        self.ui.pushButton_12.setEnabled(False)
        self.ui.spinBox.setEnabled(False)
        if self.ui.spinBox.value() == 1:
            self.ui.pushButton_13.setHidden(False)
            self.ui.lineEdit_3.setHidden(False)
            self.ui.checkBox.setHidden(False)
            self.ui.checkBox_2.setHidden(False)
        elif self.ui.spinBox.value() == 2:
            self.ui.pushButton_13.setHidden(False)
            self.ui.pushButton_16.setHidden(False)
            self.ui.lineEdit_3.setHidden(False)
            self.ui.lineEdit_4.setHidden(False)
            self.ui.checkBox.setHidden(False)
            self.ui.checkBox_2.setHidden(False)
            self.ui.checkBox_3.setHidden(False)
            self.ui.checkBox_4.setHidden(False)

    def add(self):

        files = qtw.QFileDialog.getOpenFileNames(self, None,
            "Sequences", "*.txt",
            "All Files (*);;Text Files (*.txt)")
        filenames = files[0]
        filenamesDisplay = []
        for file in self.files:
            filenamesDisplay.append(file.split("/")[-1])
        for file in filenames:
            self.files.append(file.replace("Sequences","Selected_Sequences"))
            shutil.copy2(file,'Selected_Sequences')
            filenamesDisplay.append(file.split("/")[-1])
        string = ""
        for file in filenamesDisplay:
            string = string + " " + file
        self.ui.lineEdit_2.setText(string)

    def delete(self):
        files = qtw.QFileDialog.getOpenFileNames(self, None,
            "Selected_Sequences", "*.txt",
            "All Files (*);;Text Files (*.txt)")

        filenames = files[0]
        for f in filenames:
            counter = 0
            for f2 in self.files:
                if f == f2:
                    self.files.remove(f2)
                    os.remove(f2)
        string = ""
        for file in self.files:
            string = string + " " + file.split("/")[-1]

        self.ui.lineEdit_2.setText(string)

    def clear(self):
        for f in self.files:
            os.remove(f)
        self.files = []
        self.ui.lineEdit_2.setText("")

    def compute(self):
        self.title = self.ui.lineEdit.text()
        #Send the files only if the party accepted
        if self.ui.lineEdit_3.text() != "" and self.accept1:
            self.sendFile(self.ui.lineEdit_3.text())
        if self.ui.lineEdit_4.text() != "" and self.accept2:
            self.sendFile(self.ui.lineEdit_4.text())
            
        if len(self.files)== 1:
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Information)
            msgBox.setText("Select more than one sequence")
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            msgBox.buttonClicked.connect(self.msgbtn)
            retval = msgBox.exec()
            return 0
        if self.title == "":
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Information)
            msgBox.setText("Select a name for the file that will store the result")
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            msgBox.buttonClicked.connect(self.msgbtn)
            retval = msgBox.exec()
            return 0
        if self.files == []:
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Information)
            msgBox.setText("No sequences selected")
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            msgBox.buttonClicked.connect(self.msgbtn)
            retval = msgBox.exec()
            return 0
        if (not self.ui.radioButton_2.isChecked() and not self.ui.radioButton_3.isChecked()):
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Information)
            msgBox.setText("Select a algorithm to calculate the result")
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            msgBox.buttonClicked.connect(self.msgbtn)
            retval = msgBox.exec()
            return 0
        if self.ui.radioButton_2.isChecked():
            self.type = "UPGMA"
        elif self.ui.radioButton_3.isChecked():
            self.type = "Neighbor-joining"

        Sequences_path = os.path.dirname(__file__) + '/../Selected_Sequences/'
        arr = os.listdir(Sequences_path)
        self.files = []
        for file in arr:
            self.files.append(Sequences_path + file)
        view = Compute_Window(self.files,self.title,self.type, self.widget)
        self.widget.addWidget(view)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        self.widget.setFixedHeight(300)
        self.widget.setFixedWidth(400)


        
