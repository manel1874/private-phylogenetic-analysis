# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Main(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(672, 408)
        Form.setStyleSheet("background-color: rgb(46, 52, 54);")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(-110, 0, 791, 411))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("assets/images/Main_Image.jpg"))
        self.label_2.setObjectName("label_2")
        self.New = QtWidgets.QPushButton(Form)
        self.New.setGeometry(QtCore.QRect(100, 100, 131, 51))
        self.New.setStyleSheet("QPushButton{\n"
"border: 2px solid white;\n"
"\n"
" background-color: black;\n"
" color: white;\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: white;\n"
"color:black;\n"
"}")
        self.New.setObjectName("New")
        self.View = QtWidgets.QPushButton(Form)
        self.View.setGeometry(QtCore.QRect(100, 250, 131, 51))
        self.View.setStyleSheet("QPushButton{\n"
"border: 2px solid white;\n"
"\n"
" background-color: black;\n"
" color: white;\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: white;\n"
"color:black;\n"
"}")
        self.View.setObjectName("View")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Phylogenetic Tree Computation"))
        self.New.setText(_translate("Form", "New"))
        self.View.setText(_translate("Form", "View"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Main()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
