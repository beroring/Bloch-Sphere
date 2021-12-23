import sys
import time
import vtk
import vtkmodules.all
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import pic_rc
from numpy import sin, cos, pi, sqrt, exp, arcsin, arccos, arctan, abs, conj, mod, array, dot, kron, ndarray
from PyQt5.QtGui import QIcon, QPixmap, QPaintEvent, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import Qt
from Ui_Warning import *
from Ui_MainWindow import *
from Ui_Dialog import *
from Ui_Qchoice import *
from Ui_Circuits import *
from Ui_Initialization import *
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkInteractionWidgets import (
    vtkSliderRepresentation2D,
    vtkSliderWidget,
    vtkOrientationMarkerWidget
)
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingFreeType import vtkVectorText
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkSphereSource,
    vtkLineSource,
    vtkRegularPolygonSource
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindowInteractor,
    vtkCamera,
    vtkFollower,
    vtkRenderer
)

# 定义常量矩阵
I = array([[1 + 0j, 0], [0, 1]])  # Inverse
H = 1 / sqrt(2) * array([[1 + 0j, 1], [1, -1]])  # Hadamard
X = array([[0, 1 + 0j], [1, 0]])  # PauliX
Y = array([[0, -1j], [1j, 0]])  # PauliY
Z = array([[1 + 0j, 0], [0, -1]])  # PauliZ
S = array([[1 + 0j, 0], [0, 1j]])  # Phase
T = array([[1, 0], [0, exp(1j * (pi / 4))]])  # PI/8
Cnot1 = array([[1 + 0j, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
Cnot2 = array([[1 + 0j, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]])
Cnot = [Cnot2, Cnot1]
Cz1 = array([[1 + 0j, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
Cz2 = array([[1 + 0j, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
Cz = [Cz2, Cz1]
Cs1 = array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1j]])
Cs2 = array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1j]])
Cs = [Cs2, Cs1]
Swap1 = array([[1 + 0j, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
Swap2 = array([[1 + 0j, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
Swap = [Swap1, Swap2]

# 定义初始值
zero = array([[1 + 0j], [0]])
one = array([[0], [1 + 0j]])
pos = 1 / sqrt(2) * array([[1 + 0j], [1 + 0j]])
neg = 1 / sqrt(2) * array([[1 + 0j], [-1 + 0j]])

# 定义circuits图片
Xpic = [":pics/XI.png", ":pics/IX.png"]
Ypic = [":pics/YI.png", ":pics/IY.png"]
Zpic = [":pics/ZI.png", ":pics/IZ.png"]
Hpic = [":pics/HI.png", ":pics/IH.png"]
Tpic = [":pics/TI.png", ":pics/IT.png"]
Spic = [":pics/SI.png", ":pics/IS.png"]
Swappic = [":pics/SWAP.png", ":pics/SWAP.png"]
CSpic = [":pics/SC.png", ":pics/CS.png"]
CZpic = [":pics/ZC.png", ":pics/CZ.png"]
CNOTpic = [":pics/NOTC.png", ":pics/CNOT.png"]

# 参数状态
Angle = 0
Axis = 'x'
Lstate = False  # 参考线
cirgate = [I]  # gate选择
cirgatename = []

global qibit  # circuits中qubit选择


# vtk交互模式设置
class KeyPressInteractorStyle(vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.parent = vtkRenderWindowInteractor()
        if parent is not None:
            self.parent = parent
        self.AddObserver("KeyPressEvent", self.keyPress)

    def keyPress(self, obj, event):
        key = self.parent.GetKeySym()
        if key == '0':
            myWin.zero()
        if key == '1':
            myWin.one()
        if key == 'o':
            myWin.positive()
        if key == 'n':
            myWin.negative()
        if key == 'x':
            myWin.Gatex()
        if key == 'y':
            myWin.Gatey()
        if key == 'z':
            myWin.Gatez()
        if key == 's':
            myWin.Gates()
        if key == 't':
            myWin.Gatet()
        if key == 'h':
            myWin.Gateh()


# vtk创建直线函数
def createline(p1=None, p2=None):
    if p2 is None:
        p2 = [2, 0, 0]
    if p1 is None:
        p1 = [-2, 0, 0]
    lineSource = vtkLineSource()
    lineSource.SetPoint1(p1)
    lineSource.SetPoint2(p2)

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(lineSource.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    return actor


# vtk创建坐标系函数
def MakeAxesActor():
    axes = vtkAxesActor()
    axes.SetShaftTypeToCylinder()
    axes.SetXAxisLabelText('X')
    axes.SetYAxisLabelText('Y')
    axes.SetZAxisLabelText('Z')
    axes.SetTotalLength(1.0, 1.0, 1.0)
    axes.SetCylinderRadius(0.5 * axes.GetCylinderRadius())
    axes.SetConeRadius(1.025 * axes.GetConeRadius())
    axes.SetSphereRadius(1.5 * axes.GetSphereRadius())
    return axes


# vtk创建球体函数
def createsphere(r=1):
    sphereSource = vtkSphereSource()
    sphereSource.SetCenter(0.0, 0.0, 0.0)
    sphereSource.SetRadius(r)
    sphereSource.SetThetaResolution(360)
    sphereSource.SetPhiResolution(360)

    # bmpReader = vtk.vtkBMPReader()
    # bmpReader.SetFileName("Earth.bmp")
    # texture = vtk.vtkTexture()
    # texture.SetInputConnection(bmpReader.GetOutputPort())
    # texture.InterpolateOn()
    # texturemaptosphere = vtk.vtkTextureMapToSphere()
    # texturemaptosphere.SetInputConnection(sphereSource.GetOutputPort())

    # Create a mapper and actor
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(sphereSource.GetOutputPort())
    # mapper.SetInputConnection(texturemaptosphere.GetOutputPort())

    actor = vtkActor()
    actor.GetProperty().SetOpacity(0.3)
    actor.SetMapper(mapper)
    # actor.SetTexture(texture)

    return actor


# 定义错误窗口
class Wrong(QDialog, Ui_Wrongtext):
    def __init__(self):
        super(Wrong, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(':pics/Warning.png'))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)


# 定义Rx,Ry,Rz门的输入窗口
class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(':pics/icon.png'))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.Ok)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.wrong = Wrong()
        self.wrong.setModal(True)
        self.setWindowTitle("输入")

    def Ok(self):
        global Angle
        qubit = myWin.getstate()
        Rot = I
        try:
            Angle = float(self.lineEdit.text())
            self.lineEdit.clear()
        except:
            self.lineEdit.clear()
            self.wrong.show()
        Angle = mod(Angle, 360) / 180 * pi
        a = sin(Angle / 2)
        b = cos(Angle / 2)
        if Axis == 'x':
            Rot = array([[b + 0j, 0 + -a * 1j], [0 + -a * 1j, b + 0j]])
        elif Axis == 'y':
            Rot = array([[b, -a], [a, b]])
        elif Axis == 'z':
            Rot = array([[b + 1j * sin(-Angle / 2), 0], [0, b + 1j * a]])
        else:
            print('Error!')
        qubit = dot(Rot, qubit)
        myWin.updated(qubit, 1)


# 定义curcuits中qubit初始值输入窗口
class Initialization(QDialog, Ui_Initialization):
    def __init__(self):
        super(Initialization, self).__init__()
        self.setupUi(self)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.Ok)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.Cancel)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

    def Ok(self):
        try:
            a = complex(self.lineEdit.text())
        except:
            a = 1.0
        try:
            b = complex(self.lineEdit_2.text())
        except:
            b = 0
        alpha = a / sqrt(abs(a) ** 2 + abs(b) ** 2)
        beta = b / sqrt(abs(b) ** 2 + abs(a) ** 2)
        if qibit == 1:
            circuit.q10 = array([[alpha], [beta]])
        elif qibit == 2:
            circuit.q20 = array([[alpha], [beta]])
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        circuit.Update()

    def Cancel(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()


# 定义curcuits中门选择qibit窗口
class Qchoice(QDialog, Ui_Qchoice):
    def __init__(self):
        super(Qchoice, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.radioButton.clicked.connect(self.Q1)
        self.radioButton_2.clicked.connect(self.Q2)
        self.setWindowIcon(QIcon(':pics/maomao.jpg'))
        self.setWindowTitle("请选择目标比特")

    def Q1(self):
        if isinstance(cirgate[0], list):
            circuit.circuit.append(cirgate[0][0])
        elif isinstance(cirgate[0], ndarray):
            circuit.circuit.append(kron(cirgate[0], I))
        else:
            print('Error!')
        circuit.circuitname.append(cirgatename[0])
        circuit.Update()
        self.close()

    def Q2(self):
        if isinstance(cirgate[0], list):
            circuit.circuit.append(cirgate[0][1])
        elif isinstance(cirgate[0], ndarray):
            circuit.circuit.append(kron(I, cirgate[0]))
        else:
            print('Error!')
        circuit.circuitname.append(cirgatename[1])
        circuit.Update()
        self.close()


# 定义curccuits的主窗口
class Circuits(QMainWindow, Ui_Ui_Circuits):
    def __init__(self):
        super(Circuits, self).__init__()
        self.setupUi(self)
        self.qchoice = Qchoice()
        self.qchoice.setModal(True)
        self.wrong = Wrong()
        self.wrong.setModal(True)
        self.initialization = Initialization()
        self.initialization.setModal(True)
        self.setWindowIcon(QIcon(':pics/maomao.jpg'))
        self.setWindowTitle("量子线路模拟")
        # self.pic_0.setStyleSheet("border: 2px solid red")    # 红色边框

        # 为按钮添加功能
        self.gateh.clicked.connect(lambda: self.Addgate(H, Hpic))
        self.gatex.clicked.connect(lambda: self.Addgate(X, Xpic))
        self.gatey.clicked.connect(lambda: self.Addgate(Y, Ypic))
        self.gatez.clicked.connect(lambda: self.Addgate(Z, Zpic))
        self.gatet.clicked.connect(lambda: self.Addgate(T, Tpic))
        self.gates.clicked.connect(lambda: self.Addgate(S, Spic))
        self.gateswap.clicked.connect(lambda: self.swapqubit(Swap, Swappic))
        self.cnot.clicked.connect(lambda: self.Addgate(Cnot, CNOTpic))
        self.cs.clicked.connect(lambda: self.Addgate(Cs, CSpic))
        self.cz.clicked.connect(lambda: self.Addgate(Cz, CZpic))
        self.setQ1.clicked.connect(lambda: self.initQ(1))
        self.setQ2.clicked.connect(lambda: self.initQ(2))
        self.actionBloch_Sphere.triggered.connect(self.bloch)
        self.reset.clicked.connect(self.Reset)
        self.qchoicestate = [False]
        self.q10 = array([[1 + 0j], [0 + 0j]])
        self.q20 = array([[1 + 0j], [0 + 0j]])
        self.q = kron(self.q10, self.q20)
        self.pic = [self.pic_0, self.pic_1, self.pic_2, self.pic_3, self.pic_4, self.pic_5, self.pic_6, self.pic_7]
        self.circuit = []
        self.circuitname = []
        self.lastone.clicked.connect(self.Lastone)

        # 预设按钮
        self.preset_1.clicked.connect(self.Preset_1)
        self.preset_2.clicked.connect(self.Preset_2)
        self.preset_3.clicked.connect(self.Preset_3)
        self.preset_4.clicked.connect(self.Preset_4)

    def swapqubit(self, gate, gatename):
        global cirgatename
        cirgate[0] = gate
        cirgatename = gatename
        if isinstance(cirgate[0], list):
            self.circuit.append(cirgate[0][0])
        elif isinstance(cirgate[0], ndarray):
            self.circuit.append(kron(cirgate[0], I))
        else:
            print('Error!')
        self.circuitname.append(cirgatename[0])
        self.Update()

    def Lastone(self):
        for i in range(0, 8):
            self.pic[i].setPixmap(QPixmap(""))
        try:
            self.circuit.pop()
            self.circuitname.pop()
        except:
            self.wrong.show()
        self.Update()

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.begin(self)
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(110, 373, 1151, 373)
        painter.drawLine(110, 445, 1151, 445)

    # 在线路上添加门
    def Addgate(self, gate, gatename):
        global cirgatename
        cirgate[0] = gate
        cirgatename = gatename
        self.qchoice.show()

    # 更新线路和输出
    def Update(self):
        self.label_3.setText("|Q1>={0:.8}|0>+{1:.8}|1>".format(complex(self.q10[0]), complex(self.q10[1])))
        self.label_4.setText("|Q2>={0:.8}|0>+{1:.8}|1>".format(complex(self.q20[0]), complex(self.q20[1])))
        self.q = kron(self.q10, self.q20)
        j = 0
        for i in self.circuit:
            self.q = dot(i, self.q)
            if j < 8:
                self.pic[j].setPixmap(QPixmap(self.circuitname[j]))
                j = j + 1
            else:
                self.wrong.show()
                self.Reset()
        a = complex(self.q[0])
        b = complex(self.q[1])
        c = complex(self.q[2])
        d = complex(self.q[3])
        pa = abs(a) ** 2
        pb = abs(b) ** 2
        pc = abs(c) ** 2
        pd = abs(d) ** 2
        self.output.setText("|Q>={0:.8}|00>+{1:.8}|01>\n      +{2:.8}|10>+{3:.8}|11>".format(a, b, c, d))
        self.output_2.setText("|00>：{0:.5f}    |01>：{1:.5f}    |10>：{2:.5f}    |11>：{3:.5f}".format(pa, pb, pc, pd))

    # 菜单打开bloch-sphere窗口选项
    def bloch(self):
        myWin.show()
        circuit.close()

    # 打开qubit初始状态设置窗口
    def initQ(self, q):
        global qibit
        self.initialization.show()
        qibit = q

    # 清除线路上的所有门
    def Reset(self):
        self.circuit = []
        self.circuitname = []
        self.q10 = array([[1 + 0j], [0 + 0j]])
        self.q20 = array([[1 + 0j], [0 + 0j]])
        for i in range(0, 8):
            self.pic[i].setPixmap(QPixmap(""))
        self.Update()

    def Preset_1(self):
        self.Reset()
        a = 2 + 1j
        b = 5 + 2j
        alpha = a / sqrt(abs(a) ** 2 + abs(b) ** 2)
        beta = b / sqrt(abs(b) ** 2 + abs(a) ** 2)
        self.q10 = array([[alpha], [beta]])
        self.q20 = array([[beta], [alpha]])
        self.circuit = [Cnot1, Cnot2, Cnot1]
        self.circuitname = [':pics/CNOT.png', ':pics/NOTC.png', ':pics/CNOT.png']
        self.Update()

    def Preset_2(self):
        self.Reset()
        a = 2 + 1j
        b = 5 + 2j
        alpha = a / sqrt(abs(a) ** 2 + abs(b) ** 2)
        beta = b / sqrt(abs(b) ** 2 + abs(a) ** 2)
        self.q10 = array([[alpha], [beta]])
        self.q20 = array([[beta], [alpha]])
        self.circuit = [Swap1]
        self.circuitname = [':pics/SWAP.png']
        self.Update()

    def Preset_3(self):
        self.Reset()
        a = 1 + 1j
        b = 3 + 2j
        alpha = a / sqrt(abs(a) ** 2 + abs(b) ** 2)
        beta = b / sqrt(abs(b) ** 2 + abs(a) ** 2)
        self.q10 = array([[alpha], [beta]])
        self.q20 = array([[beta], [alpha]])
        self.circuit = [kron(H, I), Cnot1]
        self.circuitname = [':pics/HI.png', ':pics/CNOT.png']
        self.Update()

    def Preset_4(self):
        self.Reset()
        a = 4 + 5j
        b = 8 + 9j
        alpha = a / sqrt(abs(a) ** 2 + abs(b) ** 2)
        beta = b / sqrt(abs(b) ** 2 + abs(a) ** 2)
        self.q10 = array([[alpha], [beta]])
        self.q20 = array([[beta], [alpha]])
        self.Update()


# 定义bloch-sphere主窗口
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.om1 = vtkOrientationMarkerWidget()
        self.setupUi(self)
        self.setWindowIcon(QIcon(':pics/icon.png'))
        self.ren = vtkRenderer()
        self.vtkrender.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkrender.GetRenderWindow().GetInteractor()
        self.Inputwindow = Dialog()
        self.Inputwindow.setModal(True)
        self.setWindowTitle("Bloch Sphere")

        # 为按钮添加功能
        self.state0.clicked.connect(self.zero)
        self.state1.clicked.connect(self.one)
        self.statepos.clicked.connect(self.positive)
        self.stateneg.clicked.connect(self.negative)
        self.gatex.clicked.connect(self.Gatex)
        self.gatey.clicked.connect(self.Gatey)
        self.gatez.clicked.connect(self.Gatez)
        self.gates.clicked.connect(self.Gates)
        self.gatet.clicked.connect(self.Gatet)
        self.gateh.clicked.connect(self.Gateh)
        self.rotatex.clicked.connect(self.Rotatex)
        self.rotatey.clicked.connect(self.Rotatey)
        self.rotatez.clicked.connect(self.Rotatez)
        self.linestate.triggered.connect(self.Linestate)
        self.circuitstate.triggered.connect(self.Circuitstate)

        colors = vtkNamedColors()

        # 将vtk部件的交互模式设置为自定义模式
        self.iren.SetInteractorStyle(KeyPressInteractorStyle(parent=self.iren))

        # 创建球体
        actorsphere = createsphere()
        actorsphere.GetProperty().SetColor(colors.GetColor3d('khaki'))
        self.ren.AddActor(actorsphere)

        # 设置滑块的初始参数
        tubeWidth = 0.008
        sliderLength = 0.008
        titleHeight = 0.04
        labelHeight = 0.04

        # 滑块设置
        self.sliderRepN1 = vtkSliderRepresentation2D()

        self.sliderRepN1.SetMinimumValue(0.0)
        self.sliderRepN1.SetMaximumValue(1.99999)
        self.sliderRepN1.SetValue(0.0)
        self.sliderRepN1.SetTitleText('Phi(0~2pi)')

        self.sliderRepN1.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
        self.sliderRepN1.GetPoint1Coordinate().SetValue(.1, .1)
        self.sliderRepN1.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
        self.sliderRepN1.GetPoint2Coordinate().SetValue(.9, .1)

        self.sliderRepN1.SetTubeWidth(tubeWidth)
        self.sliderRepN1.SetSliderLength(sliderLength)
        self.sliderRepN1.SetTitleHeight(titleHeight)
        self.sliderRepN1.SetLabelHeight(labelHeight)

        self.sliderWidgetN1 = vtkSliderWidget()
        self.sliderWidgetN1.SetInteractor(self.vtkrender.GetRenderWindow().GetInteractor())
        self.sliderWidgetN1.SetRepresentation(self.sliderRepN1)
        self.sliderWidgetN1.EnabledOn()

        self.sliderWidgetN1.AddObserver("InteractionEvent", self.callbackphi)

        self.sliderRepN2 = vtkSliderRepresentation2D()

        self.sliderRepN2.SetMinimumValue(0.0)
        self.sliderRepN2.SetMaximumValue(1.0)
        self.sliderRepN2.SetValue(0.0)
        self.sliderRepN2.SetTitleText('Theta(0~pi)')

        self.sliderRepN2.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
        self.sliderRepN2.GetPoint1Coordinate().SetValue(.1, .9)
        self.sliderRepN2.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
        self.sliderRepN2.GetPoint2Coordinate().SetValue(.9, .9)

        self.sliderRepN2.SetTubeWidth(tubeWidth)
        self.sliderRepN2.SetSliderLength(sliderLength)
        self.sliderRepN2.SetTitleHeight(titleHeight)
        self.sliderRepN2.SetLabelHeight(labelHeight)

        self.sliderWidgetN2 = vtkSliderWidget()
        self.sliderWidgetN2.SetInteractor(self.iren)
        self.sliderWidgetN2.SetRepresentation(self.sliderRepN2)
        self.sliderWidgetN2.EnabledOn()

        self.sliderWidgetN2.AddObserver("InteractionEvent", self.callbacktheta)

        # 设置坐标系
        axes1 = MakeAxesActor()
        self.om1.SetOrientationMarker(axes1)
        self.om1.SetViewport(0.35, 0.35, 0.65, 0.65)
        self.om1.SetInteractor(self.vtkrender.GetRenderWindow().GetInteractor())
        self.om1.EnabledOn()
        self.om1.InteractiveOff()

        # vtk部件和相机设置
        self.ren.SetBackground(colors.GetColor3d("AliceBlue"))

        camera = vtkCamera()
        camera.SetPosition(4.6, 2.0, 3.8)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.SetClippingRange(3.2, 10.2)
        camera.SetViewUp(0.3, 0.13, 1.0)
        self.ren.SetActiveCamera(camera)

        # 坐标系参考线
        self.actorx = createline()
        self.actory = createline([0, -2, 0], [0, 2, 0])
        self.actorz = createline([0, 0, -2], [0, 0, 2])
        self.ren.AddActor(self.actorx)
        self.ren.AddActor(self.actory)
        self.ren.AddActor(self.actorz)

        # 标签
        textSource0 = vtkVectorText()
        textSource0.SetText('0')
        textSource0.Update()
        mapper3 = vtkPolyDataMapper()
        mapper3.SetInputConnection(textSource0.GetOutputPort())
        self.textActor0 = vtkFollower()
        self.textActor0.SetMapper(mapper3)
        self.textActor0.SetScale(0.2, 0.2, 0.2)
        self.textActor0.RotateWXYZ(90, 1, 0, 0)
        self.textActor0.RotateWXYZ(90, 0, 0, 1)
        self.textActor0.AddPosition(0, -0.11, 1.2)
        self.textActor0.GetProperty().SetColor(colors.GetColor3d('black'))
        self.ren.AddActor(self.textActor0)

        textSource1 = vtkVectorText()
        textSource1.SetText('1')
        textSource1.Update()
        mapper4 = vtkPolyDataMapper()
        mapper4.SetInputConnection(textSource1.GetOutputPort())
        self.textActor1 = vtkFollower()
        self.textActor1.SetMapper(mapper4)
        self.textActor1.SetScale(0.2, 0.2, 0.2)
        self.textActor1.AddPosition(0, 0.11, -1.3)
        self.textActor1.RotateWXYZ(270, 1, 0, 0)
        self.textActor1.RotateWXYZ(270, 0, 0, 1)
        self.textActor1.GetProperty().SetColor(colors.GetColor3d('black'))
        self.ren.AddActor(self.textActor1)

        # 创建圆环
        self.polygonSource = vtkRegularPolygonSource()
        self.polygonSource.GeneratePolygonOff()
        self.polygonSource.SetNumberOfSides(360)
        self.polygonSource.SetRadius(0.0)
        self.polygonSource.SetCenter(0.0, 0.0, 1.0)
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(self.polygonSource.GetOutputPort())
        actorcircle = vtkActor()
        actorcircle.SetMapper(mapper)
        actorcircle.GetProperty().SetLineWidth(5)
        actorcircle.GetProperty().SetColor(colors.GetColor3d('green'))
        self.ren.AddActor(actorcircle)

        self.polygonSource1 = vtkRegularPolygonSource()
        self.polygonSource1.GeneratePolygonOff()
        self.polygonSource1.SetNumberOfSides(360)
        self.polygonSource1.SetRadius(1.0)
        self.polygonSource1.SetCenter(0.0, 0.0, 0.0)
        mapper1 = vtkPolyDataMapper()
        mapper1.SetInputConnection(self.polygonSource1.GetOutputPort())
        actorcircle1 = vtkActor()
        actorcircle1.SetMapper(mapper1)
        actorcircle1.GetProperty().SetLineWidth(5)
        actorcircle1.GetProperty().SetColor(colors.GetColor3d('red'))
        self.ren.AddActor(actorcircle1)
        actorcircle1.RotateX(-90)

        self.polygonSource2 = vtkRegularPolygonSource()
        self.polygonSource2.GeneratePolygonOff()
        self.polygonSource2.SetNumberOfSides(360)
        self.polygonSource2.SetRadius(1.0)
        self.polygonSource2.SetCenter(0.0, 0.0, 0.0)
        mapper2 = vtkPolyDataMapper()
        mapper2.SetInputConnection(self.polygonSource2.GetOutputPort())
        actorcircle2 = vtkActor()
        actorcircle2.SetMapper(mapper2)
        actorcircle2.GetProperty().SetLineWidth(5)
        actorcircle2.GetProperty().SetColor(colors.GetColor3d('blue'))
        self.ren.AddActor(actorcircle2)
        actorcircle2.RotateY(90)

        # 创建箭头
        actor = vtkArrowSource()
        actor.SetTipResolution(360)
        actor.SetShaftResolution(360)
        actor.SetTipLength(0.1)
        actor.SetTipRadius(0.02)
        actor.SetShaftRadius(0.01)
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(actor.GetOutputPort())
        self.actorarrow = vtkActor()
        self.actorarrow.SetMapper(mapper)
        self.actorarrow.SetOrientation(0, -90, 0)
        self.actorarrow.GetProperty().SetColor(colors.GetColor3d('Cyan'))
        self.ren.AddActor(self.actorarrow)

        self.ren.SetBackground(colors.GetColor3d('SlateGray'))

    # 更新箭头状态和滑块状态
    def updated(self, qubit, model=0):
        alpha, beta = qubit
        if complex(qubit[0]).imag != 0:
            a1, a2, b1, b2 = alpha.real, beta.real, alpha.imag, beta.imag
            a = 1 / sqrt((a1 ** 2 + b1 ** 2) ** 2 + (a1 * a2 + b1 * b2) ** 2 + (a1 * b2 - a2 * b1) ** 2)
            a = float(a)
            qubit_0 = dot(conj(complex(qubit[0])), qubit)
            qubit_0 = dot(a, qubit_0)
        else:
            qubit_0 = qubit
        alpha_0, beta_0 = qubit_0

        theta = arccos(alpha_0.real) * 2
        phi = 0
        if theta != 0:
            sinphi = (beta_0 / sin(theta / 2)).imag
            cosphi = (beta_0 / sin(theta / 2)).real
            if sinphi >= 0 and cosphi >= 0:
                phi = arcsin(sinphi)
            elif cosphi < 0:
                phi = arctan(sinphi / cosphi) + pi
            elif sinphi < 0 and cosphi >= 0:
                phi = arcsin(sinphi) + 2 * pi
            else:
                print('ERROR!')
                print('sinphi:{0},cosphi:{1},phi:{2},theta:{3}'.format(sinphi, cosphi, phi, theta))
        z = cos(theta)
        r = sin(theta)
        r2 = sqrt(1 - (sin(theta) * cos(phi)) ** 2)
        x2 = sin(theta) * cos(phi)
        x1 = sin(theta) * sin(phi)
        r1 = sqrt(1 - (sin(theta) * sin(phi)) ** 2)
        self.polygonSource.SetRadius(r)
        self.polygonSource.SetCenter(0.0, 0.0, z)
        self.polygonSource1.SetRadius(r1)
        self.polygonSource1.SetCenter(0.0, 0.0, x1)
        self.polygonSource2.SetRadius(r2)
        self.polygonSource2.SetCenter(0.0, 0.0, x2)
        self.actorarrow.SetOrientation(0, theta * 180 / pi - 90, phi * 180 / pi)
        P1 = round(float(abs(alpha) ** 2), 5)
        P2 = round(1 - P1, 5)
        self.wavefunction.setText('|Psi> = {0}|0> +\n        {1}|1>'.format(complex(alpha), complex(beta)))
        self.probability.setText('概率\n|0>:{0}\n|1>:{1}'.format(P1, P2))

        if model == 1:
            self.sliderRepN1.SetValue(phi / pi)
            self.sliderRepN2.SetValue(theta / pi)
            myWin.iren.Initialize()

    # 交互滑块theta时的反应
    def callbacktheta(self, obj, event):
        theta = obj.GetRepresentation().GetValue() * pi
        phi = self.sliderWidgetN1.GetRepresentation().GetValue() * pi
        qubit = self.getstate(theta, phi)
        self.updated(qubit)

    # 交互滑块phi时的反应
    def callbackphi(self, obj, event):
        phi = obj.GetRepresentation().GetValue() * pi
        theta = self.sliderWidgetN2.GetRepresentation().GetValue() * pi
        qubit = self.getstate(theta, phi)
        self.updated(qubit)

    # 获取箭头此时所在状态
    def getstate(self, theta=None, phi=None):
        if theta is None:
            theta = self.sliderRepN2.GetValue() * pi
        if phi is None:
            phi = self.sliderRepN1.GetValue() * pi
        alpha = cos(theta / 2)
        beta = exp(1j * phi) * sin(theta / 2)
        qubit = array([[alpha], [beta]])

        return qubit

    # 设置Gates and States
    def zero(self):
        self.updated(zero, 1)

    def one(self):
        self.updated(one, 1)

    def positive(self):
        self.updated(pos, 1)

    def negative(self):
        self.updated(neg, 1)

    def Gatex(self):
        qubit = self.getstate()
        qubit = dot(X, qubit)
        self.updated(qubit, 1)

    def Gatey(self):
        qubit = self.getstate()
        qubit = dot(Y, qubit)
        self.updated(qubit, 1)

    def Gatez(self):
        qubit = self.getstate()
        qubit = dot(Z, qubit)
        self.updated(qubit, 1)

    def Gates(self):
        qubit = self.getstate()
        qubit = dot(S, qubit)
        self.updated(qubit, 1)

    def Gatet(self):
        qubit = self.getstate()
        qubit = dot(T, qubit)
        self.updated(qubit, 1)

    def Gateh(self):
        qubit = self.getstate()
        qubit = dot(H, qubit)
        self.updated(qubit, 1)

    def Rotatex(self):
        global Axis
        self.Inputwindow.show()
        Axis = 'x'

    def Rotatey(self):
        global Axis
        self.Inputwindow.show()
        Axis = 'y'

    def Rotatez(self):
        global Axis
        self.Inputwindow.show()
        Axis = 'z'

    def Linestate(self):
        global Lstate
        self.actorx.SetVisibility(Lstate)
        self.actory.SetVisibility(Lstate)
        self.actorz.SetVisibility(Lstate)
        self.iren.Initialize()
        Lstate = not Lstate

    def Circuitstate(self):
        circuit.show()
        myWin.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    circuit = Circuits()
    # circuit.show()
    myWin = MyWindow()
    myWin.show()
    myWin.iren.Initialize()
    sys.exit(app.exec_())
