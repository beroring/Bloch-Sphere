# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '错误.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Wrongtext(object):
    def setupUi(self, Wrongtext):
        Wrongtext.setObjectName("Wrongtext")
        Wrongtext.resize(291, 187)
        Wrongtext.setMinimumSize(QtCore.QSize(291, 187))
        Wrongtext.setMaximumSize(QtCore.QSize(291, 187))
        self.pushButton = QtWidgets.QPushButton(Wrongtext)
        self.pushButton.setGeometry(QtCore.QRect(92, 130, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Wrongtext)
        self.label.setGeometry(QtCore.QRect(50, 40, 191, 81))
        self.label.setObjectName("label")

        self.retranslateUi(Wrongtext)
        self.pushButton.clicked.connect(Wrongtext.reject)
        QtCore.QMetaObject.connectSlotsByName(Wrongtext)

    def retranslateUi(self, Wrongtext):
        _translate = QtCore.QCoreApplication.translate
        Wrongtext.setWindowTitle(_translate("Wrongtext", "错误"))
        self.pushButton.setText(_translate("Wrongtext", "确定"))
        self.label.setText(_translate("Wrongtext", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">输入有误！</span></p></body></html>"))
