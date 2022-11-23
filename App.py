### System

import sys
import shutil
import os
import time
import socket
from subprocess import Popen, PIPE, STDOUT, call
import threading

### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtNetwork import *

### Interfaces
from interface.MainWindowV2 import Main
from interface.OptionsV2 import Opt
from interface.Local import Local_Window
from interface.Computing2 import Compute
from interface.Multi_party import Multi
from interface.Multi_partyAcc import MultiAcc

### Server classes
from server.server import Server
from server.main_window import MainWindow
from server.multi_window_acc import MultiAcc
from server.secure_window_acc import Secure_window_acc
from server.quantum_window_acc import Quantum_window_acc
#from server.main import app

### Client classes
from client.local import Local
from client.multi_window import Multi_window
from client.secure_window import Secure_window
from client.quantum_window import Quantum_window

### Common class
from common.compute import Compute_Window


app = qtw.QApplication(sys.argv)
app.setWindowIcon(qtg.QIcon('assets/images/ICON.png'))
app.setApplicationName("Phylogenetic Tree Computation")
widget = qtw.QStackedWidget()
main = MainWindow(widget)
widget.addWidget(main)
widget.setFixedHeight(372)
widget.setFixedWidth(1013)

widget.show()


try:

    sys.exit(app.exec_())
    
except:
    print("EXIT")

