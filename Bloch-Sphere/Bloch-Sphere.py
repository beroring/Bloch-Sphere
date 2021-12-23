import sys
import vtk
import vtkmodules.all
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from numpy import sin, cos, pi, sqrt, matrix, exp, arcsin, arccos, arctan, abs, conj, mod
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from Ui_Warning import *
from Ui_MainWindow import *
from Ui_Dialog import *
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

# Qubit transformation matrices
I = matrix([[1 + 0j, 0], [0, 1]])  # Inverse
H = 1 / sqrt(2) * matrix([[1 + 0j, 1], [1, -1]])  # Hadamard
X = matrix([[0, 1 + 0j], [1, 0]])  # PauliX
Y = matrix([[0, -1j], [1j, 0]])  # PauliY
Z = matrix([[1 + 0j, 0], [0, -1]])  # PauliZ
S = matrix([[1 + 0j, 0], [0, 1j]])  # Phase
T = matrix([[1, 0], [0, exp(1j * (pi / 4))]])  # PI/8
# sN = 1 / sqrt(2) * matrix([[1 + 0j, -1], [1, 1]])  # Sqrt Not
zero = matrix([[1 + 0j, 0]]).T
one = matrix([[0, 1 + 0j]]).T
pos = 1 / sqrt(2) * matrix([1 + 0j, 1 + 0j]).T
neg = 1 / sqrt(2) * matrix([1 + 0j, -1 + 0j]).T

Angle = 0
Axis = 'x'
Lstate = False


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


class Wrong(QDialog, Ui_Wrongtext):
    def __init__(self):
        super(Wrong, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('Warning.png'))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)


class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.Ok)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

    def Ok(self):
        global Angle
        qubit = myWin.getstate()
        Rot = I
        try:
            Angle = float(self.lineEdit.text())
            self.lineEdit.clear()
        except:
            self.lineEdit.clear()
            wrong.show()
        Angle = mod(Angle, 360) / 180 * pi
        a = sin(Angle / 2)
        b = cos(Angle / 2)
        if Axis == 'x':
            Rot = matrix([[b + 0j, 0 + -a * 1j], [0 + -a * 1j, b + 0j]])
        elif Axis == 'y':
            Rot = matrix([[b, -a], [a, b]])
        elif Axis == 'z':
            Rot = matrix([[b + 1j * sin(-Angle / 2), 0], [0, b + 1j * a]])
        else:
            print('Error!')
        qubit = Rot * qubit
        myWin.updated(qubit, 1)


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.om1 = vtkOrientationMarkerWidget()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.ren = vtkRenderer()
        self.vtkrender.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkrender.GetRenderWindow().GetInteractor()

        # 添加功能
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

        global polygonSource, polygonSource1, polygonSource2, actorarrow, sliderRepN1, sliderRepN2

        colors = vtkNamedColors()

        self.iren.SetInteractorStyle(KeyPressInteractorStyle(parent=self.iren))

        # 创建球体
        actorsphere = createsphere()
        actorsphere.GetProperty().SetColor(colors.GetColor3d('khaki'))
        self.ren.AddActor(actorsphere)

        # Setup a slider widget for each varying parameter
        tubeWidth = 0.008
        sliderLength = 0.008
        titleHeight = 0.04
        labelHeight = 0.04

        # 滑块设置
        sliderRepN1 = vtkSliderRepresentation2D()

        sliderRepN1.SetMinimumValue(0.0)
        sliderRepN1.SetMaximumValue(1.99999)
        sliderRepN1.SetValue(0.0)
        sliderRepN1.SetTitleText('Phi(0~2pi)')

        sliderRepN1.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
        sliderRepN1.GetPoint1Coordinate().SetValue(.1, .1)
        sliderRepN1.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
        sliderRepN1.GetPoint2Coordinate().SetValue(.9, .1)

        sliderRepN1.SetTubeWidth(tubeWidth)
        sliderRepN1.SetSliderLength(sliderLength)
        sliderRepN1.SetTitleHeight(titleHeight)
        sliderRepN1.SetLabelHeight(labelHeight)

        self.sliderWidgetN1 = vtkSliderWidget()
        self.sliderWidgetN1.SetInteractor(self.vtkrender.GetRenderWindow().GetInteractor())
        self.sliderWidgetN1.SetRepresentation(sliderRepN1)
        self.sliderWidgetN1.EnabledOn()

        self.sliderWidgetN1.AddObserver("InteractionEvent", self.callbackphi)

        sliderRepN2 = vtkSliderRepresentation2D()

        sliderRepN2.SetMinimumValue(0.0)
        sliderRepN2.SetMaximumValue(1.0)
        sliderRepN2.SetValue(0.0)
        sliderRepN2.SetTitleText('Theta(0~pi)')

        sliderRepN2.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
        sliderRepN2.GetPoint1Coordinate().SetValue(.1, .9)
        sliderRepN2.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
        sliderRepN2.GetPoint2Coordinate().SetValue(.9, .9)

        sliderRepN2.SetTubeWidth(tubeWidth)
        sliderRepN2.SetSliderLength(sliderLength)
        sliderRepN2.SetTitleHeight(titleHeight)
        sliderRepN2.SetLabelHeight(labelHeight)

        self.sliderWidgetN2 = vtkSliderWidget()
        self.sliderWidgetN2.SetInteractor(self.iren)
        self.sliderWidgetN2.SetRepresentation(sliderRepN2)
        self.sliderWidgetN2.EnabledOn()

        self.sliderWidgetN2.AddObserver("InteractionEvent", self.callbacktheta)

        # 设置坐标系
        axes1 = MakeAxesActor()
        self.om1.SetOrientationMarker(axes1)
        self.om1.SetViewport(0.35, 0.35, 0.65, 0.65)
        self.om1.SetInteractor(self.vtkrender.GetRenderWindow().GetInteractor())
        self.om1.EnabledOn()
        self.om1.InteractiveOff()

        # 窗口和相机设置
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
        polygonSource = vtkRegularPolygonSource()
        polygonSource.GeneratePolygonOff()
        polygonSource.SetNumberOfSides(360)
        polygonSource.SetRadius(0.0)
        polygonSource.SetCenter(0.0, 0.0, 1.0)
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(polygonSource.GetOutputPort())
        actorcircle = vtkActor()
        actorcircle.SetMapper(mapper)
        actorcircle.GetProperty().SetLineWidth(5)
        actorcircle.GetProperty().SetColor(colors.GetColor3d('green'))
        self.ren.AddActor(actorcircle)

        polygonSource1 = vtkRegularPolygonSource()
        polygonSource1.GeneratePolygonOff()
        polygonSource1.SetNumberOfSides(360)
        polygonSource1.SetRadius(1.0)
        polygonSource1.SetCenter(0.0, 0.0, 0.0)
        mapper1 = vtkPolyDataMapper()
        mapper1.SetInputConnection(polygonSource1.GetOutputPort())
        actorcircle1 = vtkActor()
        actorcircle1.SetMapper(mapper1)
        actorcircle1.GetProperty().SetLineWidth(5)
        actorcircle1.GetProperty().SetColor(colors.GetColor3d('red'))
        self.ren.AddActor(actorcircle1)
        actorcircle1.RotateX(-90)

        polygonSource2 = vtkRegularPolygonSource()
        polygonSource2.GeneratePolygonOff()
        polygonSource2.SetNumberOfSides(360)
        polygonSource2.SetRadius(1.0)
        polygonSource2.SetCenter(0.0, 0.0, 0.0)
        mapper2 = vtkPolyDataMapper()
        mapper2.SetInputConnection(polygonSource2.GetOutputPort())
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
        actorarrow = vtkActor()
        actorarrow.SetMapper(mapper)
        actorarrow.SetOrientation(0, -90, 0)
        actorarrow.GetProperty().SetColor(colors.GetColor3d('Cyan'))
        self.ren.AddActor(actorarrow)

        self.ren.SetBackground(colors.GetColor3d('SlateGray'))

    def updated(self, qubit, model=0):
        alpha, beta = qubit
        if complex(qubit[0]).imag != 0:
            a1, a2, b1, b2 = alpha.real, beta.real, alpha.imag, beta.imag
            a = 1 / sqrt((a1 ** 2 + b1 ** 2) ** 2 + (a1 * a2 + b1 * b2) ** 2 + (a1 * b2 - a2 * b1) ** 2)
            a = float(a)
            qubit_0 = conj(complex(qubit[0])) * qubit
            qubit_0 = a * qubit_0
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
        polygonSource.SetRadius(r)
        polygonSource.SetCenter(0.0, 0.0, z)
        polygonSource1.SetRadius(r1)
        polygonSource1.SetCenter(0.0, 0.0, x1)
        polygonSource2.SetRadius(r2)
        polygonSource2.SetCenter(0.0, 0.0, x2)
        actorarrow.SetOrientation(0, theta * 180 / pi - 90, phi * 180 / pi)
        P1 = round(float(abs(alpha) ** 2), 5)
        P2 = round(1 - P1, 5)
        self.wavefunction.setText('|psi> = {0}|0> +\n        {1}|1>'.format(complex(alpha), complex(beta)))
        self.probability.setText('概率\n|0>:{0}\n|1>:{1}'.format(P1, P2))

        if model == 1:
            sliderRepN1.SetValue(phi / pi)
            sliderRepN2.SetValue(theta / pi)
            myWin.iren.Initialize()

    def callbacktheta(self, obj, event):
        theta = obj.GetRepresentation().GetValue() * pi
        phi = self.sliderWidgetN1.GetRepresentation().GetValue() * pi
        qubit = self.getstate(theta, phi)
        self.updated(qubit)

    def callbackphi(self, obj, event):
        phi = obj.GetRepresentation().GetValue() * pi
        theta = self.sliderWidgetN2.GetRepresentation().GetValue() * pi
        qubit = self.getstate(theta, phi)
        self.updated(qubit)

    def getstate(self, theta=None, phi=None):
        if theta is None:
            theta = sliderRepN2.GetValue() * pi
        if phi is None:
            phi = sliderRepN1.GetValue() * pi
        alpha = cos(theta / 2)
        beta = exp(1j * phi) * sin(theta / 2)
        qubit = matrix([alpha, beta]).T

        return qubit

    # Gates and States
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
        qubit = X * qubit
        self.updated(qubit, 1)

    def Gatey(self):
        qubit = self.getstate()
        qubit = Y * qubit
        self.updated(qubit, 1)

    def Gatez(self):
        qubit = self.getstate()
        qubit = Z * qubit
        self.updated(qubit, 1)

    def Gates(self):
        qubit = self.getstate()
        qubit = S * qubit
        self.updated(qubit, 1)

    def Gatet(self):
        qubit = self.getstate()
        qubit = T * qubit
        self.updated(qubit, 1)

    def Gateh(self):
        qubit = self.getstate()
        qubit = H * qubit
        self.updated(qubit, 1)

    def Rotatex(self):
        global Axis
        Inputwindow.show()
        Axis = 'x'

    def Rotatey(self):
        global Axis
        Inputwindow.show()
        Axis = 'y'

    def Rotatez(self):
        global Axis
        Inputwindow.show()
        Axis = 'z'

    def Linestate(self):
        global Lstate
        self.actorx.SetVisibility(Lstate)
        self.actory.SetVisibility(Lstate)
        self.actorz.SetVisibility(Lstate)
        self.iren.Initialize()
        Lstate = not Lstate


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Inputwindow = Dialog()
    wrong = Wrong()
    myWin = MyWindow()
    myWin.show()
    myWin.iren.Initialize()
    sys.exit(app.exec_())
