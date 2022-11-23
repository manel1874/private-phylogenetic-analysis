# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OptionsB.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
import os

from PyQt5 import QtCore, QtGui, QtWidgets


class Opt(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1013, 472)
        Form.setStyleSheet("background-color: white;")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(-20, -20, 1051, 551))
        self.label.setStyleSheet("background-color: white;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(50, 320, 161, 31))
        self.label_2.setStyleSheet("color: rgb(81, 181, 13);\n"
"background-color: white;\n"
"font-size: 18px;\n"
"")
        self.label_2.setObjectName("label_2")
        self.Ok_3 = QtWidgets.QPushButton(Form)
        self.Ok_3.setGeometry(QtCore.QRect(280, 120, 201, 191))
        self.Ok_3.setStyleSheet("QPushButton{\n"
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
        self.Ok_3.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/images/Multi2Light.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Ok_3.setIcon(icon)
        self.Ok_3.setIconSize(QtCore.QSize(100, 100))
        self.Ok_3.setObjectName("Ok_3")
        self.Ok_4 = QtWidgets.QPushButton(Form)
        self.Ok_4.setGeometry(QtCore.QRect(530, 120, 201, 191))
        self.Ok_4.setStyleSheet("QPushButton{\n"
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
        self.Ok_4.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/images/SecureLight.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Ok_4.setIcon(icon1)
        self.Ok_4.setIconSize(QtCore.QSize(100, 100))
        self.Ok_4.setObjectName("Ok_4")
        self.Ok_5 = QtWidgets.QPushButton(Form)
        self.Ok_5.setGeometry(QtCore.QRect(30, 120, 201, 191))
        self.Ok_5.setStyleSheet("QPushButton{\n"
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
        self.Ok_5.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("assets/images/System-computer-iconLight.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Ok_5.setIcon(icon2)
        self.Ok_5.setIconSize(QtCore.QSize(100, 100))
        self.Ok_5.setObjectName("Ok_5")
        self.Ok_6 = QtWidgets.QPushButton(Form)
        self.Ok_6.setGeometry(QtCore.QRect(780, 120, 201, 191))
        self.Ok_6.setStyleSheet("QPushButton{\n"
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
        self.Ok_6.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("assets/images/SecureQuantumLight.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Ok_6.setIcon(icon3)
        self.Ok_6.setIconSize(QtCore.QSize(100, 100))
        self.Ok_6.setObjectName("Ok_6")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(300, 320, 191, 51))
        self.label_3.setStyleSheet("color: rgb(81, 181, 13);\n"
"background-color: white;\n"
"font-size: 18px;\n"
"")
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(520, 320, 231, 51))
        self.label_4.setStyleSheet("color: rgb(81, 181, 13);\n"
"background-color: white;\n"
"font-size: 18px;\n"
"")
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(770, 320, 241, 51))
        self.label_5.setStyleSheet("color: rgb(81, 181, 13);\n"
"background-color: white;\n"
"font-size: 18px;\n"
"")
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setObjectName("label_5")
        self.Ok_7 = QtWidgets.QPushButton(Form)
        self.Ok_7.setGeometry(QtCore.QRect(0, 0, 101, 61))
        self.Ok_7.setStyleSheet("QPushButton{\n"
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
        self.Ok_7.setIconSize(QtCore.QSize(100, 100))
        self.Ok_7.setObjectName("Ok_7")
        self.label.raise_()
        self.Ok_3.raise_()
        self.Ok_4.raise_()
        self.Ok_5.raise_()
        self.label_2.raise_()
        self.Ok_6.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.Ok_7.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Local Computation"))
        self.label_3.setText(_translate("Form", "Classical Multiparty \n"
"     Computation"))
        self.label_4.setText(_translate("Form", "Classical Secure Multiparty \n"
"            Computation"))
        self.label_5.setText(_translate("Form", "Quantum Secure Multiparty \n"
"            Computation"))
        self.Ok_7.setText(_translate("Form", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Opt()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
