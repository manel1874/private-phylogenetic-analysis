### System
import shutil
import os
import requests
import threading

### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtNetwork import *

### Interfaces
from interface.Multi_partyAcc import MultiAcc

### Common class
from common.compute import Compute_Window

class Multi_acc(qtw.QWidget):

    def __init__(self, widget,ip,sck, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.files = []
        self.ui = MultiAcc()
        self.ui.setupUi(self)
        self.ui.pushButton_7.clicked.connect(self.add)
        self.ui.pushButton_8.clicked.connect(self.delete)
        self.ui.pushButton_9.clicked.connect(self.clear)
        self.ui.pushButton_10.clicked.connect(self.send)
        self.ui.pushButton_11.clicked.connect(self.compute)
        self.ui.pushButton_11.setEnabled(False)
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_2.setText("")
        #self.ui.lineEdit_2.setReadOnly(True)
        self.widget = widget
        self.ServerIP = ip
        configs = open("config.txt","r")
        self.ip = configs.readline()
        configs.close()
        self.ip = self.ip.split(":")[1].rstrip()
        self.socket = sck

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

    def msgbtn(self):
        return 0

    def checker(self):
        loop = qtc.QEventLoop()
        while(1):
            qtc.QTimer.singleShot(2000, loop.quit)
            loop.exec_()
            Sequences_path = os.path.dirname(__file__) + '/../Selected_Sequences/'
            arr = os.listdir(Sequences_path)
            if len(arr) > len(self.files):
                self.ui.checkBox.setChecked(True)
                self.ui.pushButton_11.setEnabled(True)
                return 1

    def send(self):
        self.thr = threading.Thread(target=self.checker, args=())
        self.thr.start()
        self.title = self.ui.lineEdit.text()
        Sequences_path = os.path.dirname(__file__) + '/../Selected_Sequences/'
        arr = os.listdir(Sequences_path)
        for file in arr:
            file = {'upload_file': open("Selected_Sequences/" + file,"rb")}
            url = 'http://' + self.ServerIP + ':8090/fileServer'
            x = requests.post(url,files = file)
        msg_resp = 'Sequences '+ self.ip
        msg_resp = bytes(msg_resp, 'utf-8')
        self.socket.write(msg_resp)
    

    def compute(self):
        #CHECK HERE
        self.thr.join()
        self.title = self.ui.lineEdit.text()
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