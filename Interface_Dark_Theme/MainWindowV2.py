# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main2.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Main(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1009, 318)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(0, -144, 1271, 661))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("assets/images/logo2.png"))
        self.label_2.setObjectName("label_2")
        self.New = QtWidgets.QPushButton(Form)
        self.New.setGeometry(QtCore.QRect(320, 160, 141, 61))
        self.New.setStyleSheet("QPushButton{\n"
"border: 4px solid rgb(32, 74, 135);\n"
"border-radius: 14px;\n"
"background-color: rgb(22, 24, 22);\n"
" color: rgb(0,121,253);\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: rgb(32, 74, 135);\n"
"color:white;\n"
"}")
        self.New.setObjectName("New")
        self.View = QtWidgets.QPushButton(Form)
        self.View.setGeometry(QtCore.QRect(70, 160, 141, 61))
        self.View.setStyleSheet("QPushButton{\n"
"border: 4px solid rgb(32, 74, 135);\n"
"border-radius: 14px;\n"
"background-color: rgb(22, 24, 22);\n"
" color: rgb(0,121,253);\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: rgb(32, 74, 135);\n"
"color:white;\n"
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
