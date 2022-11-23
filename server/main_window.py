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
from interface.MainWindowV2 import Main
from interface.OptionsV2 import Opt

### Server classes
from server.server import Server

### Client classes
from client.local import Local
from client.option import Option

### Common class
from common.compute import window




class MainWindow(qtw.QWidget):

    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.ui = Main()
        self.ui.setupUi(self)
        self.ui.New.clicked.connect(self.goOptions)
        self.ui.View.clicked.connect(self.HandleQuestion)
        self.sessionOpened = Server(widget)
        self.widget = widget
        

    def goOptions(self):
        opt = Option(self.widget)
        self.widget.addWidget(opt)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        self.widget.setFixedHeight(472)
        self.widget.setFixedWidth(1013)

    def HandleQuestion(self):
        files = qtw.QFileDialog.getOpenFileNames(self, None,
            "Results", "*.txt",
            "All Files (*);;Text Files (*.txt)")
        filename = files[0][0].split("/")[-1]
        shutil.copy2('Results/' + filename,'phylip-3.697/exe/intree')
        os.chdir("phylip-3.697/exe")
        if os.name != 'nt':
            p = Popen(['./drawgram'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = 'font1\nP\nW\n480\n852\nY\n'.encode())[0]
        else:
            p = Popen(['drawgram.exe'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = 'font1\nP\nW\n480\n852\nY\n'.encode())[0]
        os.chdir("../..")
        view = window("phylip-3.697/exe/plotfile", self.widget)
        self.widget.addWidget(view)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        os.remove("phylip-3.697/exe/intree")
        os.remove("phylip-3.697/exe/plotfile")