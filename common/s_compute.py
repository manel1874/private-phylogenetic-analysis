### System

import shutil
import os
from subprocess import Popen, PIPE, STDOUT

### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtNetwork import *

### Interfaces
from interface.Computing2 import Compute

### Common
from common.window import window



class Secure_Compute_Window(qtw.QWidget):

    def __init__(self,title,typeNU, widget, numOfParties, partyNum, numOfInputs, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.ui = Compute()
        self.ui.setupUi(self)
        self.widget = widget
        self.partyNum = partyNum
        self.numOfInputs = numOfInputs
        self.numOfParties = numOfParties

        # Run smc engine
        os.chdir("smc_engine")
        runGenomeSMC = "./runGenomeSMC" + " " + str(self.numOfParties) + " " + str(self.partyNum) + " " + str(self.numOfInputs)
        genomeSMC_process = Popen(runGenomeSMC, shell=True)
        genomeSMC_process.wait()

        # Compute Phylogenetic trees with PHYLIP
        os.chdir("../phylip-3.697/exe")
        if os.name != 'nt':
            if typeNU == "UPGMA":
                p = Popen(['./neighbor'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
                stdout_data = p.communicate(input = 'N\nY'.encode())[0]
            else:
                p = Popen(['./neighbor'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
                stdout_data = p.communicate(input = 'Y'.encode())[0]
            os.rename(r'outtree',r'intree')
            p = Popen(['./drawgram'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = 'font1\nP\nW\n480\n852\nY\n'.encode())[0]
            #os.rename(r'plotfile',r'plotfile.bmp')
            os.remove("infile")
            os.remove("outfile")
            shutil.move("intree", "../../Results/" + title)
            os.chdir("../..")
            for file in os.scandir("Selected_Sequences"):
                if file.name.endswith(".txt"):
                    os.remove(file.path)
            for file in os.scandir("smc_engine/inputFiles"):
                if file.name.endswith(".txt"):
                    os.remove(file.path)
        else:
            p = Popen(['dnadist.exe'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = 'I\nY\n'.encode())[0]
            os.remove("infile")
            os.rename(r'outfile',r'infile')
            if typeNU == "UPGMA":
                p = Popen(['neighbor.exe'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
                stdout_data = p.communicate(input = 'N\nY'.encode())[0]
            else:
                p = Popen(['neighbor.exe'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
                stdout_data = p.communicate(input = 'Y'.encode())[0]
            os.rename(r'outtree',r'intree')
            p = Popen(['drawgram.exe'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = 'font1\nP\nW\n480\n852\nY\n'.encode())[0]
            #os.rename(r'plotfile',r'plotfile.bmp')
            os.remove("infile")
            os.remove("outfile")
            shutil.move("intree", "../../Results/" + title)
            os.chdir("../..")
            for file in os.scandir("Selected_Sequences"):
                if file.name.endswith(".txt"):
                    os.remove(file.path)
        for i in range(101):
            self.ui.progressBar.setValue(i)
        self.ui.pushButton.clicked.connect(self.done)

    def done(self):
        view = window("phylip-3.697/exe/plotfile", self.widget)
        self.widget.addWidget(view)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        os.remove("phylip-3.697/exe/plotfile")


