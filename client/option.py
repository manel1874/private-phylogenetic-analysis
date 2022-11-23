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
from interface.OptionsB import Opt
from interface.Multi_party2 import Multi

### Client classes
from client.local import Local
from client.multi_window import Multi_window
from client.secure_window import Secure_window
from client.quantum_window import Quantum_window

### Common class
from common.compute import window


class Option(qtw.QWidget):

    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.ui = Opt()
        self.ui.setupUi(self)

        self.ui.Ok_5.clicked.connect(self.LocalComp)
        self.ui.Ok_3.clicked.connect(self.MultiComp)
        self.ui.Ok_4.clicked.connect(self.SecureComp)
        self.ui.Ok_6.clicked.connect(self.QuantumComp)
        self.ui.Ok_7.clicked.connect(self.goBack)
        self.widget = widget

    def LocalComp(self):
        lc = Local(self.widget)
        self.widget.addWidget(lc)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        self.widget.setFixedHeight(370)
        self.widget.setFixedWidth(574)
    
    def MultiComp(self):
        lc = Multi_window(self.widget)
        self.widget.addWidget(lc)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        self.widget.setFixedHeight(533)
        self.widget.setFixedWidth(631)
    
    def SecureComp(self):
        sc= Secure_window(self.widget)
        self.widget.addWidget(sc)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        self.widget.setFixedHeight(591)
        self.widget.setFixedWidth(631)
        
    def QuantumComp(self):
        qsc= Quantum_window(self.widget)
        self.widget.addWidget(qsc)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        self.widget.setFixedHeight(591)
        self.widget.setFixedWidth(631)

    def goBack(self):
        max = self.widget.count()
        for i in range(max):
            self.widget.removeWidget(self.widget.widget(max-i))
        ### Server classes
        from server.main_window import MainWindow 
        main = MainWindow(self.widget)
        self.widget.addWidget(main)
        self.widget.setCurrentIndex(1)
        self.widget.setFixedHeight(372)
        self.widget.setFixedWidth(1013)
