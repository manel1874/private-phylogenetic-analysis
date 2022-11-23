### System
import shutil
import os
import requests
import threading
import ipaddress

### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtNetwork import *

##interface

from interface.Quantum_Secure_acc import Quantum_window_acc_Interface
from common.q_compute import Quantum_Compute_Window

class Quantum_window_acc(qtw.QWidget):

    #clienIP is the ip of the inviter and otherpartyIp is the ip of the 3rd party if it exists
    def __init__(self,widget,clientIp,otherpartyIp,sck, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.files = []
        self.ui = Quantum_window_acc_Interface()
        self.ui.setupUi(self)
        self.widget = widget
        self.ui.pushButton_7.clicked.connect(self.add)
        self.ui.pushButton_8.clicked.connect(self.delete)
        self.ui.pushButton_9.clicked.connect(self.clear)
        self.ui.pushButton_10.clicked.connect(self.compute)
        self.ui.lineEdit_3.setHidden(True)
        self.ui.lineEdit_4.setHidden(True)
        self.ui.lineEdit_5.setHidden(True)
        self.ui.lineEdit_6.setHidden(True)
        self.ui.checkBox_3.setChecked(True)
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_2.setText("")
        configs = open("config.txt","r")
        self.ip = configs.readline().replace("\n","")
        configs.close()
        self.ip = self.ip.split(":")[1].rstrip()
        #Display other parties IPs
        ip1 = clientIp
        ip2 = self.ip
        ip3 = "255.255.255.255"
        if otherpartyIp != "":
            ip3 = otherpartyIp
            self.ui.lineEdit_3.setHidden(False)
            self.ui.lineEdit_5.setHidden(False)
            self.ui.lineEdit_4.setHidden(False)
            self.ui.lineEdit_6.setHidden(False)
            self.ui.lineEdit_3.setText(clientIp)
            self.ui.lineEdit_5.setText(otherpartyIp)
        else:
            self.ui.lineEdit_3.setHidden(False)
            self.ui.lineEdit_4.setHidden(False)
            self.ui.lineEdit_3.setText(clientIp)
            self.ui.lineEdit_6.setText("")

        #Calculate id
        iplist = [ip1,ip2,ip3]
        self.iplist = sorted(iplist,key = ipaddress.IPv4Address)
        self.id = self.iplist.index(ip2)
        self.idInviter = self.iplist.index(ip1)
        self.id3Party = self.iplist.index(ip3)

        #self.id
        print(self.id)


        

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

        self.rename_selected_files()
        self.partiesFile()

        if self.ui.radioButton_2.isChecked():
            self.type = "UPGMA"
        elif self.ui.radioButton_3.isChecked():
            self.type = "Neighbor-joining"
            
        numOfInputs = len(self.files)
        view = Quantum_Compute_Window(self.title,self.type, self.widget, self.numOfParties, self.id, numOfInputs)
        self.widget.addWidget(view)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        self.widget.setFixedHeight(300)
        self.widget.setFixedWidth(400)
