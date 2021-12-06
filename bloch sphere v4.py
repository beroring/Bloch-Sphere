import sys
from numpy import sin, cos, pi, sqrt
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_MainWindow import *
import vtkmodules.all as vtk
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkInteractionWidgets import (
    vtkSliderRepresentation2D,
    vtkSliderWidget,
    vtkButtonRepresentation,
    vtkButtonWidget
)
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkSphereSource,
    vtkLineSource
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


class KeyPressInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.parent = vtkRenderWindowInteractor()
        if parent is not None:
            self.parent = parent
        self.AddObserver("KeyPressEvent", self.keyPress)

    def keyPress(self, obj, event):
        key = self.parent.GetKeySym()
        if key == '0':
            myWin.updated(0.0, 0.0)
            sliderRepN1.SetValue(0.0)
            sliderRepN2.SetValue(0.0)
            myWin.iren.Initialize()
        if key == 'Up':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            myWin.updated(theta, phi + 1)
            sliderRepN1.SetValue(phi + 1)
            sliderRepN2.SetValue(theta)
            myWin.iren.Initialize()
        if key == 'Down':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            myWin.updated(theta, phi - 1)
            sliderRepN1.SetValue(phi - 1)
            sliderRepN2.SetValue(theta)
            myWin.iren.Initialize()
        if key == 'Left':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            myWin.updated(theta - 1, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta - 1)
            myWin.iren.Initialize()
        if key == 'Right':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            myWin.updated(theta + 1, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta + 1)
            myWin.iren.Initialize()
        if key == 'x':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            phi = 180 - phi
            theta = 360 - theta
            myWin.updated(theta, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta)
            myWin.iren.Initialize()
        if key == 'y':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            phi = 180 - phi
            theta = 180 - theta
            myWin.updated(theta, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta)
            myWin.iren.Initialize()
        if key == 'z':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            if theta >= 180:
                theta = theta - 180
            else:
                theta = theta + 180
            myWin.updated(theta, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta)
            myWin.iren.Initialize()
        if key == 's':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            if theta < 90:
                theta = theta + 270
            else:
                theta = theta - 90
            myWin.updated(theta, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta)
            myWin.iren.Initialize()
        if key == 't':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            if theta < 45:
                theta = theta + 315
            else:
                theta = theta - 45
            myWin.updated(theta, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta)
            myWin.iren.Initialize()


def createline(p1=None, p2=None):
    if p2 is None:
        p2 = [2, 0, 0]
    if p1 is None:
        p1 = [-2, 0, 0]
    lineSource = vtkLineSource()
    lineSource.SetPoint1(p1)
    lineSource.SetPoint2(p2)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(lineSource.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    return actor


def MakeAxesActor():
    axes = vtk.vtkAxesActor()
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


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.om1 = vtk.vtkOrientationMarkerWidget()
        self.setupUi(self)
        self.ren = vtk.vtkRenderer()
        self.vtkrender.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkrender.GetRenderWindow().GetInteractor()

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
        sliderRepN1.SetMaximumValue(180.0)
        sliderRepN1.SetValue(0.0)
        sliderRepN1.SetTitleText('Phi')

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
        sliderRepN2.SetMaximumValue(360.0)
        sliderRepN2.SetValue(0.0)
        sliderRepN2.SetTitleText('Theta')

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

        camera = vtk.vtkCamera()
        camera.SetPosition(4.6, 2.0, 3.8)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.SetClippingRange(3.2, 10.2)
        camera.SetViewUp(0.3, 0.13, 1.0)
        self.ren.SetActiveCamera(camera)

        # 坐标系参考线
        actorx = createline()
        actory = createline([0, -2, 0], [0, 2, 0])
        actorz = createline([0, 0, -2], [0, 0, 2])
        self.ren.AddActor(actorx)
        self.ren.AddActor(actory)
        self.ren.AddActor(actorz)

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

    def updated(self, theta, phi):
        z = cos(phi / 180.0 * pi)
        r = sin(phi / 180.0 * pi)
        x2 = sin(phi / 180.0 * pi) * cos(theta / 180.0 * pi)
        r2 = sqrt(1 - (sin(phi / 180.0 * pi) * cos(theta / 180.0 * pi)) ** 2)
        x1 = sin(phi / 180.0 * pi) * sin(theta / 180.0 * pi)
        r1 = sqrt(1 - (sin(phi / 180.0 * pi) * sin(theta / 180.0 * pi)) ** 2)
        polygonSource.SetRadius(r)
        polygonSource.SetCenter(0.0, 0.0, z)
        polygonSource1.SetRadius(r1)
        polygonSource1.SetCenter(0.0, 0.0, x1)
        polygonSource2.SetRadius(r2)
        polygonSource2.SetCenter(0.0, 0.0, x2)
        actorarrow.SetOrientation(0, phi - 90, theta)

    def callbackphi(self, obj, event):
        phi = obj.GetRepresentation().GetValue()
        theta = actorarrow.GetOrientation()[2]
        myWin.updated(theta, phi)

    def callbacktheta(self, obj, event):
        theta = obj.GetRepresentation().GetValue()
        phi = actorarrow.GetOrientation()[1]
        phi = phi + 90
        myWin.updated(theta, phi)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    myWin.iren.Initialize()
    sys.exit(app.exec_())
