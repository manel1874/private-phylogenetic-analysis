### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtNetwork import *

class window(qtw.QWidget):

    def __init__(self, file, widget):
        super().__init__()
        self.file = file
        self.widget = widget
        self.title = 'Image'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Create widget
        self.label = qtw.QLabel(self)
        pixmap = qtg.QPixmap(self.file)
        pixmap = pixmap.scaled(750,750,qtc.Qt.KeepAspectRatio)
        self.widget.setFixedHeight(700)
        self.widget.setFixedWidth(400)
        self.label.setPixmap(pixmap)
        self.buton = qtw.QPushButton(self)
        self.buton.setText("Back")
        self.buton.setStyleSheet("QPushButton{\n"
"border: 2px solid Black;\n"
"\n"
" background-color: rgb(46, 52, 54);\n"
" color: white;\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: white;\n"
"color:black;\n"
"}")
        self.buton.clicked.connect(self.goBack)

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
