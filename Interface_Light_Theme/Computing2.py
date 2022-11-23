# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Computing.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Compute(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(40, 140, 321, 23))
        self.progressBar.setStyleSheet("QProgressBar{\n"
"    background-color: rgb(200,200,200);\n"
"    color: rgb(170,85,127);\n"
"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk{\n"
"    border-radius: 10px;\n"
"    \n"
"    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(131, 142, 137, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 521, 351))
        self.label.setStyleSheet("background-color: white;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(140, 40, 151, 61))
        self.label_2.setStyleSheet("color: rgb(81, 181, 13);\n"
"font-size: 20px;")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(150, 210, 101, 51))
        self.pushButton.setStyleSheet("QPushButton{\n"
"border: 4px solid rgb(81, 181, 13);\n"
"border-radius: 14px;\n"
"background-color: white;\n"
" color: rgb(81, 181, 13);\n"
" padding: 5px 5px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: rgb(71, 224, 25);\n"
"color:white;\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.label.raise_()
        self.progressBar.raise_()
        self.label_2.raise_()
        self.pushButton.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Computing"))
        self.pushButton.setText(_translate("Form", "Show"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Compute()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
