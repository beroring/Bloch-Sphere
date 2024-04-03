# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '可变窗口.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 675)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.vtkrender = QVTKRenderWindowInteractor()
        self.vtkrender.setMinimumSize(QtCore.QSize(600, 600))
        self.vtkrender.setObjectName("vtkrender")
        self.horizontalLayout_10.addWidget(self.vtkrender)
        self.horizontalLayout.addLayout(self.horizontalLayout_10)
        self.layoutright = QtWidgets.QVBoxLayout()
        self.layoutright.setObjectName("layoutright")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setMinimumSize(QtCore.QSize(200, 56))
        self.title.setMaximumSize(QtCore.QSize(400, 56))
        self.title.setLineWidth(27)
        self.title.setObjectName("title")
        self.layoutright.addWidget(self.title, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.wavefunction = QtWidgets.QLabel(self.groupBox)
        self.wavefunction.setMinimumSize(QtCore.QSize(650, 100))
        self.wavefunction.setMaximumSize(QtCore.QSize(1000, 100))
        self.wavefunction.setStyleSheet("QLabel{font: 75 12pt \"微软雅黑\";}")
        self.wavefunction.setObjectName("wavefunction")
        self.horizontalLayout_11.addWidget(self.wavefunction)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.probability = QtWidgets.QLabel(self.groupBox_6)
        self.probability.setMinimumSize(QtCore.QSize(650, 100))
        self.probability.setMaximumSize(QtCore.QSize(1000, 100))
        self.probability.setStyleSheet("QLabel{font: 75 12pt \"微软雅黑\";}")
        self.probability.setObjectName("probability")
        self.horizontalLayout_7.addWidget(self.probability)
        self.verticalLayout_3.addWidget(self.groupBox_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.state0 = QtWidgets.QPushButton(self.groupBox_2)
        self.state0.setMinimumSize(QtCore.QSize(0, 43))
        self.state0.setMaximumSize(QtCore.QSize(134, 43))
        self.state0.setObjectName("state0")
        self.horizontalLayout_3.addWidget(self.state0)
        self.state1 = QtWidgets.QPushButton(self.groupBox_2)
        self.state1.setMinimumSize(QtCore.QSize(0, 43))
        self.state1.setMaximumSize(QtCore.QSize(134, 43))
        self.state1.setObjectName("state1")
        self.horizontalLayout_3.addWidget(self.state1)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.statepos = QtWidgets.QPushButton(self.groupBox_3)
        self.statepos.setMinimumSize(QtCore.QSize(0, 43))
        self.statepos.setMaximumSize(QtCore.QSize(134, 43))
        self.statepos.setObjectName("statepos")
        self.horizontalLayout_4.addWidget(self.statepos)
        self.stateneg = QtWidgets.QPushButton(self.groupBox_3)
        self.stateneg.setMinimumSize(QtCore.QSize(0, 43))
        self.stateneg.setMaximumSize(QtCore.QSize(134, 43))
        self.stateneg.setObjectName("stateneg")
        self.horizontalLayout_4.addWidget(self.stateneg)
        self.horizontalLayout_2.addWidget(self.groupBox_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gatey = QtWidgets.QPushButton(self.groupBox_4)
        self.gatey.setMinimumSize(QtCore.QSize(0, 43))
        self.gatey.setMaximumSize(QtCore.QSize(180, 43))
        self.gatey.setObjectName("gatey")
        self.gridLayout.addWidget(self.gatey, 0, 1, 1, 1)
        self.gatex = QtWidgets.QPushButton(self.groupBox_4)
        self.gatex.setMinimumSize(QtCore.QSize(0, 43))
        self.gatex.setMaximumSize(QtCore.QSize(180, 43))
        self.gatex.setObjectName("gatex")
        self.gridLayout.addWidget(self.gatex, 0, 0, 1, 1)
        self.gatet = QtWidgets.QPushButton(self.groupBox_4)
        self.gatet.setMinimumSize(QtCore.QSize(0, 43))
        self.gatet.setMaximumSize(QtCore.QSize(180, 43))
        self.gatet.setObjectName("gatet")
        self.gridLayout.addWidget(self.gatet, 1, 2, 1, 1)
        self.gatez = QtWidgets.QPushButton(self.groupBox_4)
        self.gatez.setMinimumSize(QtCore.QSize(0, 43))
        self.gatez.setMaximumSize(QtCore.QSize(180, 43))
        self.gatez.setObjectName("gatez")
        self.gridLayout.addWidget(self.gatez, 0, 2, 1, 1)
        self.gates = QtWidgets.QPushButton(self.groupBox_4)
        self.gates.setMinimumSize(QtCore.QSize(0, 43))
        self.gates.setMaximumSize(QtCore.QSize(180, 43))
        self.gates.setObjectName("gates")
        self.gridLayout.addWidget(self.gates, 1, 1, 1, 1)
        self.gateh = QtWidgets.QPushButton(self.groupBox_4)
        self.gateh.setMinimumSize(QtCore.QSize(0, 43))
        self.gateh.setMaximumSize(QtCore.QSize(180, 43))
        self.gateh.setObjectName("gateh")
        self.gridLayout.addWidget(self.gateh, 1, 0, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.rotatex = QtWidgets.QPushButton(self.groupBox_5)
        self.rotatex.setMinimumSize(QtCore.QSize(0, 43))
        self.rotatex.setMaximumSize(QtCore.QSize(180, 43))
        self.rotatex.setObjectName("rotatex")
        self.horizontalLayout_6.addWidget(self.rotatex)
        self.rotatey = QtWidgets.QPushButton(self.groupBox_5)
        self.rotatey.setMinimumSize(QtCore.QSize(0, 43))
        self.rotatey.setMaximumSize(QtCore.QSize(180, 43))
        self.rotatey.setObjectName("rotatey")
        self.horizontalLayout_6.addWidget(self.rotatey)
        self.rotatez = QtWidgets.QPushButton(self.groupBox_5)
        self.rotatez.setMinimumSize(QtCore.QSize(0, 43))
        self.rotatez.setMaximumSize(QtCore.QSize(180, 43))
        self.rotatez.setObjectName("rotatez")
        self.horizontalLayout_6.addWidget(self.rotatez)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.addWidget(self.groupBox_5)
        self.horizontalLayout_8.addLayout(self.verticalLayout_3)
        self.layoutright.addLayout(self.horizontalLayout_8)
        self.horizontalLayout.addLayout(self.layoutright)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1161, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menu)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.linestate = QtWidgets.QAction(MainWindow)
        self.linestate.setObjectName("linestate")
        self.circuitstate = QtWidgets.QAction(MainWindow)
        self.circuitstate.setObjectName("circuitstate")
        self.menu_2.addAction(self.linestate)
        self.menu.addAction(self.circuitstate)
        self.menu.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Bloch Sphere模拟单量子比特计算</span></p></body></html>"))
        self.groupBox.setTitle(_translate("MainWindow", "Psi"))
        self.wavefunction.setText(_translate("MainWindow", "|Psi> = (1+0j)|0> +\n        0j|1>"))
        self.groupBox_6.setTitle(_translate("MainWindow", "概率"))
        self.probability.setText(_translate("MainWindow", "概率\n|0>:1.0\n|1>:0.0"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Basic States"))
        self.state0.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/state0.jpg\"/></p></body></html>"))
        self.state0.setText(_translate("MainWindow", "|0>"))
        self.state1.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/state1.jpg\"/></p></body></html>"))
        self.state1.setText(_translate("MainWindow", "|1>"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Spuerposition"))
        self.statepos.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/statepos.jpg\"/></p></body></html>"))
        self.statepos.setText(_translate("MainWindow", "|+>"))
        self.stateneg.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/stateneg.jpg\"/></p></body></html>"))
        self.stateneg.setText(_translate("MainWindow", "|->"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Gates"))
        self.gatey.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/gatey.jpg\"/></p></body></html>"))
        self.gatey.setText(_translate("MainWindow", "Y"))
        self.gatex.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/gatex.jpg\"/></p></body></html>"))
        self.gatex.setText(_translate("MainWindow", "X"))
        self.gatet.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/gatet.jpg\"/></p></body></html>"))
        self.gatet.setText(_translate("MainWindow", "T"))
        self.gatez.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/gatez.jpg\"/></p></body></html>"))
        self.gatez.setText(_translate("MainWindow", "Z"))
        self.gates.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/gates.jpg\"/></p></body></html>"))
        self.gates.setText(_translate("MainWindow", "S"))
        self.gateh.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/gateh.jpg\"/></p></body></html>"))
        self.gateh.setText(_translate("MainWindow", "H"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Gates"))
        self.rotatex.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/rotatex.jpg\"/></p></body></html>"))
        self.rotatex.setText(_translate("MainWindow", "RotateX"))
        self.rotatey.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/rotatey.jpg\"/></p></body></html>"))
        self.rotatey.setText(_translate("MainWindow", "RotateY"))
        self.rotatez.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/tips/rotatez.jpg\"/></p></body></html>"))
        self.rotatez.setText(_translate("MainWindow", "RotateZ"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.menu_2.setTitle(_translate("MainWindow", "参考线"))
        self.linestate.setText(_translate("MainWindow", "显示/隐藏"))
        self.circuitstate.setText(_translate("MainWindow", "量子线路模拟"))
import icon_rc
