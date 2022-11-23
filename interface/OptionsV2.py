# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Options.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Opt(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(464, 381)
        Form.setStyleSheet("background-color: rgb(46, 52, 54);")
        self.radioButton_4 = QtWidgets.QRadioButton(Form)
        self.radioButton_4.setGeometry(QtCore.QRect(30, 40, 301, 51))
        self.radioButton_4.setStyleSheet("QRadioButton{\n"
"    font-size: 17px;\n"
"    background-color:  rgb(79, 163, 224);\n"
"    color: rgb(238, 238, 236);\n"
"}")
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(Form)
        self.radioButton_5.setGeometry(QtCore.QRect(30, 100, 301, 51))
        self.radioButton_5.setStyleSheet("QRadioButton{\n"
"    font-size: 17px;\n"
"    background-color:  rgb(79, 163, 224);\n"
"    color: rgb(238, 238, 236);\n"
"}")
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_6 = QtWidgets.QRadioButton(Form)
        self.radioButton_6.setGeometry(QtCore.QRect(30, 160, 351, 51))
        self.radioButton_6.setStyleSheet("QRadioButton{\n"
"    font-size: 17px;\n"
"    background-color:  rgb(79, 163, 224);\n"
"    color: rgb(238, 238, 236);\n"
"}")
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_7 = QtWidgets.QRadioButton(Form)
        self.radioButton_7.setGeometry(QtCore.QRect(30, 220, 371, 51))
        self.radioButton_7.setStyleSheet("QRadioButton{\n"
"    font-size: 17px;\n"
"    background-color: rgb(79, 163, 224);\n"
"    color: rgb(238, 238, 236);\n"
"}")
        self.radioButton_7.setObjectName("radioButton_7")
        self.Ok = QtWidgets.QPushButton(Form)
        self.Ok.setGeometry(QtCore.QRect(50, 310, 131, 51))
        self.Ok.setStyleSheet("QPushButton{\n"
"border: 2px solid white;\n"
"border-radius: 14px;\n"
"background-color: rgb(52, 101, 164);\n"
" color: white;\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: white;\n"
"color:black;\n"
"}")
        self.Ok.setObjectName("Ok")
        self.pushButton_12 = QtWidgets.QPushButton(Form)
        self.pushButton_12.setGeometry(QtCore.QRect(290, 310, 131, 51))
        self.pushButton_12.setStyleSheet("QPushButton{\n"
"border: 2px solid white;\n"
"border-radius: 14px;\n"
"background-color: rgb(52, 101, 164);\n"
" color: white;\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: white;\n"
"color:black;\n"
"}")
        self.pushButton_12.setObjectName("pushButton_12")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 721, 431))
        self.label.setStyleSheet("background-color: rgb(79, 163, 224)")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.raise_()
        self.radioButton_4.raise_()
        self.radioButton_5.raise_()
        self.radioButton_6.raise_()
        self.radioButton_7.raise_()
        self.Ok.raise_()
        self.pushButton_12.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.radioButton_4.setText(_translate("Form", "Local Computation"))
        self.radioButton_5.setText(_translate("Form", "Classical Multi-party Computation"))
        self.radioButton_6.setText(_translate("Form", "Classical Secure Multi-party Computation"))
        self.radioButton_7.setText(_translate("Form", "Quantum Secure Multi-party Computation"))
        self.Ok.setText(_translate("Form", "OK"))
        self.pushButton_12.setText(_translate("Form", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Opt()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
