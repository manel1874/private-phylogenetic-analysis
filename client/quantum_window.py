### System
import requests
import socket
import os
import shutil
import ipaddress

### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore, QtNetwork
from interface.Quantum_acc import Quantum

from common.q_compute import Quantum_Compute_Window

class Quantum_window(qtw.QWidget):
  
    def __init__(self,widget, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.ui = Quantum()
        self.ui.setupUi(self)
        self.ui.setupUi(self)
        self.ui.pushButton_13.setHidden(True)
        self.ui.lineEdit_3.setHidden(True)
        self.ui.lineEdit_4.setHidden(True)
        self.ui.checkBox.setHidden(True)
        self.ui.checkBox_2.setHidden(True)
        self.ui.checkBox_3.setHidden(True)
        self.ui.checkBox_4.setHidden(True)
        self.ui.lineEdit_5.setHidden(True)
        self.ui.lineEdit_6.setHidden(True)
        self.ui.spinBox.setMaximum(2)
        self.ui.spinBox.setMinimum(1)
        self.ui.pushButton_12.clicked.connect(self.apply)
        self.ui.pushButton_13.clicked.connect(self.invite1)
        self.ui.pushButton_7.clicked.connect(self.add)
        self.ui.pushButton_8.clicked.connect(self.delete)
        self.ui.pushButton_9.clicked.connect(self.clear)
        self.ui.pushButton_14.clicked.connect(self.info)
        self.files = []
        self._socket = QtNetwork.QTcpSocket(self)
        self._socket.stateChanged.connect(self.on_stateChanged)
        self.ui.pushButton_10.clicked.connect(self.compute)
        self._socket.readyRead.connect(self.on_readyRead)
        configs = open("config.txt","r")
        self.ip = configs.readline().replace("\n","")
        configs.close()
        self.ip = self.ip.split(":")[1].rstrip()
        self.widget = widget
        self.accept1 = False
        self.accept2 = False
        self._socket2 = QtNetwork.QTcpSocket(self)
        self._socket2.stateChanged.connect(self.on_stateChanged2)
        self._socket2.readyRead.connect(self.on_readyRead2)

    def info(self):
        msgBox = qtw.QMessageBox()
        msgBox.setIcon(qtw.QMessageBox.Information)
        msgBox.setText("INFO")
        msgBox.setWindowTitle("Information on the cryptographic algorithms")
        msgBox.setStandardButtons(qtw.QMessageBox.Ok)
        msgBox.buttonClicked.connect(self.msgbtn)
        retval = msgBox.exec()

    
    #-----------------------SOCKETs_FOR_PARTY1------------------------
    def on_stateChanged(self, state):
        if state == QtNetwork.QAbstractSocket.ConnectedState:
            if self.ui.lineEdit_4.text() != "":
                msg = "Quantum_Secure Multiparty " + self.ip + ' and ' + self.ui.lineEdit_4.text() + " Number of Sequences: " + str(len(self.files))
            else:
                msg = "Quantum_Secure Multiparty " + self.ip + " Number of Sequences: " + str(len(self.files))


            self.sendMessage(bytes (msg,'utf-8'))
        elif state == QtNetwork.QAbstractSocket.UnconnectedState:
            print("disconnected")
            

    def on_readyRead(self):
        Response = self._socket.readAll()


        if Response.split(" ")[0] == "Accepted":
            if Response.split(" ")[1] == self.ui.lineEdit_3.text():
                self.accept1 = True
                self.ui.checkBox.setChecked(True)
                self.ui.checkBox_2.setChecked(True)
	            
            else:
                self.ui.checkBox_3.setChecked(True)
                self.ui.checkBox_4.setChecked(True)

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
    def on_stateChanged2(self, state):
        if state == QtNetwork.QAbstractSocket.ConnectedState:
            if self.ui.lineEdit_3.text() != "":
                msg = "Quantum_Secure Multiparty " + self.ip + ' and ' + self.ui.lineEdit_3.text()  + " Number of Sequences: " + str(len(self.files))
            else:
                msg = "Quantum_Secure Multiparty " + self.ip + " Number of Sequences: " + str(len(self.files))
            self.sendMessage2(bytes (msg,'utf-8'))
        elif state == QtNetwork.QAbstractSocket.UnconnectedState:
            print("disconnected")
            #QtCore.QCoreApplication.quit()

    def on_readyRead2(self):
        Response = self._socket2.readAll()

        
        if Response.split(" ")[0] == "Accepted":
            if Response.split(" ")[1] == self.ui.lineEdit_4.text():
                self.accept2 = True
                self.ui.checkBox_3.setChecked(True)
                self.ui.checkBox_4.setChecked(True)
            else:
                self.ui.checkBox.setChecked(True)
                self.ui.checkBox_2.setChecked(True)


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


    def invite1(self):
        #Party1
        if self.ui.spinBox.value() <= 2:
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
            
        #Party2
        if self.ui.spinBox.value() == 2:
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

        #calculate IDS of the parties
        if self.ui.lineEdit_4.text() == "":
            ip2 = "255.255.255.255"
        else:
            ip2 = self.ui.lineEdit_4.text()
        
        iplist = [self.ip,ip2,self.ui.lineEdit_3.text()]
        self.iplist = sorted(iplist,key = ipaddress.IPv4Address)
        self.id = self.iplist.index(self.ip)
        self.idParty2 = self.iplist.index(self.ui.lineEdit_3.text())
        self.idParty3 = self.iplist.index(ip2)

        #self.id
        #print(self.id)

    def apply(self):
        self.ui.pushButton_12.setEnabled(False)
        self.ui.spinBox.setEnabled(False)
        if self.ui.spinBox.value() == 1:
            self.ui.pushButton_13.setHidden(False)
            self.ui.lineEdit_3.setHidden(False)
            self.ui.checkBox.setHidden(False)
            self.ui.checkBox_2.setHidden(False)
            self.ui.lineEdit_5.setHidden(False)
            self.ui.lineEdit_4.setText("")
            self.ui.lineEdit_6.setText("")
        elif self.ui.spinBox.value() == 2:
            self.ui.pushButton_13.setHidden(False)
            self.ui.lineEdit_3.setHidden(False)
            self.ui.lineEdit_4.setHidden(False)
            self.ui.checkBox.setHidden(False)
            self.ui.checkBox_2.setHidden(False)
            self.ui.checkBox_3.setHidden(False)
            self.ui.checkBox_4.setHidden(False)
            self.ui.lineEdit_5.setHidden(False)
            self.ui.lineEdit_6.setHidden(False)

    
    def add(self):

        files = qtw.QFileDialog.getOpenFileNames(self, None,
            "binary_sequences", "*.txt",
            "All Files (*);;Text Files (*.txt)")
        filenames = files[0]
        filenamesDisplay = []
        for file in self.files:
            filenamesDisplay.append(file.split("/")[-1])
        for file in filenames:

            smc_engine_inputFiles = "smc_engine/inputFiles"
            shutil.copy2(file, smc_engine_inputFiles)

            self.files.append(file.replace("binary_sequences","smc_engine/inputFiles"))
            shutil.copy2(file,'smc_engine/inputFiles')
            filenamesDisplay.append(file.split("/")[-1])
        string = ""
        for file in filenamesDisplay:
            string = string + " " + file
        self.ui.lineEdit_2.setText(string)
    
    def rename_selected_files(self):

        """ TODO:
            - select sequences from binary_sequences folder
            - save number of selected sequences to variable called numOfInputs
            - delete all files inside smc_engine/inputFiles
            - send to folder smc_engine/inputFiles with the following structure:

                Party_i_seq_j

                where i is the party id number (give by variable partyNum)
                      j is the sequence number: 0 <= j < numOfInputs      (0 <= j <= numOfInputs - 1)
        """



        
        # Send to folder smc_engine/inputFiles with the following structure:
        #                Party_i_seq_j.txt

        #        where i is the party id number (give by variable partyNum)
        #              j is the sequence number: 0 <= j < numOfInputs      (0 <= j <= numOfInputs - 1)
        j=0
        name_decoding_dictionary = {}
        for file in self.files:
            smc_engine_inputFiles = "smc_engine/inputFiles"
            name = "Party_" + str(self.id) + "_seq_" + str(j) + ".txt"
            b_sequence = file.split("/")[-1]

            #shutil.copy2(file, smc_engine_inputFiles)
            shutil.move(smc_engine_inputFiles+"/"+b_sequence, smc_engine_inputFiles+"/"+name)

            #self.files.append(file.replace(b_sequence, name))
            name_decoding_dictionary[str(self.id) + str(j)] = b_sequence

            j=j+1

        self.name_decoding_dictionary = name_decoding_dictionary


    def delete(self):
        #Sugestão: não usar este botão
        files = qtw.QFileDialog.getOpenFileNames(self, None,
            "smc_engine/inputFiles", "*.txt",
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

    
    
    def partiesFile(self):
        """
            - Receive the other parties IP address and their corresponding id
            - Write file called "Parties" with the following structure:

                                    party_0_ip = 127.0.0.1
                                    party_1_ip = 127.0.0.1
                                    party_2_ip = 127.0.0.1
                                    party_0_port = 8000
                                    party_1_port = 8200
                                    party_2_port = 8400

            - Save this file into smc_engine/partiesFiles
        """
        filename = "smc_engine/partiesFiles/Parties"

        ip_0 = str(self.iplist[0])
        port_0 = "10000"
        ip_1 = str(self.iplist[1])
        port_1 = "10200"
        ip_2 = str(self.iplist[2])
        port_2 = "10400"

        if ip_2 == "255.255.255.255":
            self.numOfParties = 2
        else: 
            self.numOfParties = 3
        
        if self.numOfParties == 2:
            with open(filename, 'w') as file_object:
                file_object.write("party_0_ip = " + ip_0 + "\n")
                file_object.write("party_1_ip = " + ip_1 + "\n")
                file_object.write("party_0_port = " + port_0 + "\n")
                file_object.write("party_1_port = " + port_1 + "\n")
        else:
            with open(filename, 'w') as file_object:
                file_object.write("party_0_ip = " + ip_0 + "\n")
                file_object.write("party_1_ip = " + ip_1 + "\n")
                file_object.write("party_2_ip = " + ip_2 + "\n")
                file_object.write("party_0_port = " + port_0 + "\n")
                file_object.write("party_1_port = " + port_1 + "\n")
                file_object.write("party_2_port = " + port_2 + "\n")
    
    
    
    
    def compute(self):
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



        #Prepare partiesFile/Parties

        #self.iplist
        #self.id = iplist.index(self.ip)
        #self.idParty2 = iplist.index(self.ui.lineEdit_3.text())
        #self.idParty3 = iplist.index(ip2)

        """
        Amanha: 
        1. escrever self.iplist no _acc.py
        2. Fazer merge do guilherme
        3. Continuar mudar Parties file
        4. Fazer a função toda!
        """

        # Rename files in smc_engine/inputFiles
        self.rename_selected_files()
        # Generate Parties file
        self.partiesFile()
        

        self.title = self.ui.lineEdit.text()
        if self.ui.radioButton_2.isChecked():
            self.type = "UPGMA"
        elif self.ui.radioButton_3.isChecked():
            self.type = "Neighbor-joining"

        #Sequences_path = os.path.dirname(__file__) + '/../Selected_Sequences/'
        #arr = os.listdir(Sequences_path)
        #self.files = []
        #for file in arr:
        #    self.files.append(Sequences_path + file)

        numOfInputs = len(self.files)
        view = Quantum_Compute_Window(self.title,self.type, self.widget, self.numOfParties, self.id, numOfInputs)
        self.widget.addWidget(view)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        self.widget.setFixedHeight(300)
        self.widget.setFixedWidth(400)
