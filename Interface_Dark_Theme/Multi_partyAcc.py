# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Local.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class MultiAcc(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(574, 370)
        #Form.setStyleSheet("background-color: rgb(46, 52, 54);")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 30, 431, 16))
        self.label.setStyleSheet("color: rgb(238, 238, 236);")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 531, 41))
        self.lineEdit.setStyleSheet("QLineEdit{\n"
" border: 2px solid rgb(37, 39, 48);\n"
" border-radius:20px;\n"
" color : #FFF;\n"
" padding-left: 20px;\n"
"padding-right: 20px;\n"
" background-color: rgb(34,36,44);\n"
"}")
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 291, 16))
        self.label_2.setStyleSheet("color: rgb(238, 238, 236);")
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 130, 251, 41))
        self.lineEdit_2.setStyleSheet("QLineEdit{\n"
" border: 2px solid rgb(37, 39, 48);\n"
" border-radius:20px;\n"
" color : #FFF;\n"
" padding-left: 20px;\n"
"padding-right: 20px;\n"
" background-color: rgb(34,36,44);\n"
"}")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(280, 130, 51, 41))
        self.pushButton_7.setStyleSheet("QPushButton{\n"
"border: 4px solid rgb(32, 74, 135);\n"
"border-radius: 14px;\n"
"background-color: rgb(22, 24, 22);\n"
" color: rgb(0,121,253);\n"
" padding: 7px 7px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: rgb(32, 74, 135);\n"
"color:white;\n"
"}")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(340, 130, 51, 41))
        self.pushButton_8.setStyleSheet("QPushButton{\n"
"border: 4px solid rgb(32, 74, 135);\n"
"border-radius: 14px;\n"
"background-color: rgb(22, 24, 22);\n"
" color: rgb(0,121,253);\n"
" padding: 7px 7px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: rgb(32, 74, 135);\n"
"color:white;\n"
"}")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setGeometry(QtCore.QRect(400, 130, 81, 41))
        self.pushButton_9.setStyleSheet("QPushButton{\n"
"border: 4px solid rgb(32, 74, 135);\n"
"border-radius: 14px;\n"
"background-color: rgb(22, 24, 22);\n"
" color: rgb(0,121,253);\n"
" padding: 7px 7px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: rgb(32, 74, 135);\n"
"color:white;\n"
"}")
        self.pushButton_9.setObjectName("pushButton_9")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(30, 180, 301, 51))
        self.radioButton_2.setStyleSheet("QRadioButton{\n"
" background-color: rgb(22, 24, 22);\n"
"    font-size: 15px;\n"
"    color: white;\n"
"}")
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(Form)
        self.radioButton_3.setGeometry(QtCore.QRect(30, 240, 301, 51))
        self.radioButton_3.setStyleSheet("QRadioButton{\n"
" background-color: rgb(22, 24, 22);\n"
"    font-size: 15px;\n"
"    color: white;\n"
"}")
        self.radioButton_3.setObjectName("radioButton_3")
        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setGeometry(QtCore.QRect(490, 130, 71, 41))
        self.pushButton_10.setStyleSheet("QPushButton{\n"
"border: 4px solid rgb(32, 74, 135);\n"
"border-radius: 14px;\n"
"background-color: rgb(22, 24, 22);\n"
" color: rgb(0,121,253);\n"
" padding: 7px 7px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: rgb(32, 74, 135);\n"
"color:white;\n"
"}")
        self.pushButton_10.setObjectName("pushButton_10")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(-70, -30, 741, 411))
        self.label_3.setStyleSheet("background-color: rgb(22, 24, 22);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.pushButton_11 = QtWidgets.QPushButton(Form)
        self.pushButton_11.setGeometry(QtCore.QRect(230, 290, 121, 51))
        self.pushButton_11.setStyleSheet("QPushButton{\n"
"border: 4px solid rgb(32, 74, 135);\n"
"border-radius: 14px;\n"
"background-color: rgb(22, 24, 22);\n"
" color: rgb(0,121,253);\n"
" padding: 7px 7px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: rgb(32, 74, 135);\n"
"color:white;\n"
"}")
        self.pushButton_11.setObjectName("pushButton_11")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(370, 230, 170, 23))
        self.checkBox.setStyleSheet(" background-color: rgb(22, 24, 22);\n"
"    font-size: 15px;\n"
"    color: white;\n"
)
        self.checkBox.setObjectName("checkBox")
        self.label_3.raise_()
        self.label.raise_()
        self.lineEdit.raise_()
        self.label_2.raise_()
        self.lineEdit_2.raise_()
        self.pushButton_7.raise_()
        self.pushButton_8.raise_()
        self.pushButton_9.raise_()
        self.radioButton_2.raise_()
        self.radioButton_3.raise_()
        self.pushButton_10.raise_()
        self.pushButton_11.raise_()
        self.checkBox.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Local"))
        self.label.setText(_translate("Form", "Select the name of the file to store the result"))
        self.label_2.setText(_translate("Form", "Select the sequences"))
        self.pushButton_7.setText(_translate("Form", "+"))
        self.pushButton_8.setText(_translate("Form", "-"))
        self.pushButton_9.setText(_translate("Form", "Clear"))
        self.radioButton_2.setText(_translate("Form", "UPGMA"))
        self.radioButton_3.setText(_translate("Form", "Neighbor-joining"))
        self.pushButton_10.setText(_translate("Form", "Send"))
        self.pushButton_11.setText(_translate("Form", "Compute"))
        self.checkBox.setText(_translate("Form", "All parties are ready"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = MultiAcc()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
