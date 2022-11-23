### System
import shutil
import os
import requests

### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtNetwork import *

### Interfaces
from interface.Local import Local_Window

### Common class
from common.compute import Compute_Window

class Local(qtw.QWidget):

    def __init__(self, widget,ip,socket, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.files = []
        self.ui = Local_Window()
        self.ui.setupUi(self)

        self.ui.pushButton_7.clicked.connect(self.add)
        self.ui.pushButton_8.clicked.connect(self.delete)
        self.ui.pushButton_9.clicked.connect(self.clear)
        self.ui.pushButton_10.clicked.connect(self.compute)
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_2.setText("")
        #self.ui.lineEdit_2.setReadOnly(True)
        self.widget = widget
        self.ServerIP = ip
        self.ip = "127.0.0.1"

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

    def compute(self):
        self.title = self.ui.lineEdit.text()
        Sequences_concat_path = os.path.dirname(__file__) + '/../Selected_Sequences/' + self.ip + '.txt'
        with open(Sequences_concat_path,'w') as outfile:
            outfile.write("\t" + str(len(self.files)) + "\t" + "30144\n")
            for fname in self.files:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)
                os.remove(fname)
        outfile.close()
        file = {'upload_file': open('Selected_Sequences/' + self.ip + '.txt',"rb")}
        url = 'http://' + "127.0.0.1" + ':8090/fileServer'
        x = requests.post(url,files = file,ip = self.ip)
        msg_resp = 'Sequences '+'192.168.1.76'
        msg_resp = bytes(msg_resp, 'utf-8')
        socket.write(msg_resp)
