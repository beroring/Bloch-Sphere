import sys
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
            print('hello,world!\n')


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
        self.setupUi(self)
        self.vtkwin()

    def vtkwin(self):
        ren = vtk.vtkRenderer()
        self.vtkrender.GetRenderWindow().AddRenderer(ren)
        self.iren = self.vtkrender.GetRenderWindow().GetInteractor()
        # self.vtkrender.setWindowOpacity(0.5)
        # self.iren.SetInteractorStyle(KeyPressInteractorStyle(parent=self.iren)
        self.blochsphere(ren)

    def blochsphere(self, ren):
        colors = vtkNamedColors()

        self.iren.SetInteractorStyle(KeyPressInteractorStyle(parent=self.iren))

        # 创建球体
        actorsphere = createsphere()
        actorsphere.GetProperty().SetColor(colors.GetColor3d('khaki'))
        ren.AddActor(actorsphere)

        # 设置坐标系
        # axes1 = MakeAxesActor()
        # om1 = vtk.vtkOrientationMarkerWidget()
        # om1.SetOrientationMarker(axes1)
        # om1.SetViewport(0.35, 0.35, 0.65, 0.65)
        # om1.SetInteractor(self.iren)
        # om1.EnabledOn()
        # om1.InteractiveOff()

        # 窗口和相机设置
        ren.SetBackground(colors.GetColor3d("AliceBlue"))

        camera = vtk.vtkCamera()
        camera.SetPosition(4.6, 2.0, 3.8)
        camera.SetFocalPoint(0.0, 0.0, 0.0)
        camera.SetClippingRange(3.2, 10.2)
        camera.SetViewUp(0.3, 0.13, 1.0)
        ren.SetActiveCamera(camera)

        # 坐标系参考线
        actorx = createline()
        actory = createline([0, -2, 0], [0, 2, 0])
        actorz = createline([0, 0, -2], [0, 0, 2])
        ren.AddActor(actorx)
        ren.AddActor(actory)
        ren.AddActor(actorz)

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
        ren.AddActor(actorcircle)

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
        ren.AddActor(actorcircle1)
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
        ren.AddActor(actorcircle2)
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
        ren.AddActor(actorarrow)

        ren.SetBackground(colors.GetColor3d('SlateGray'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    myWin.iren.Initialize()
    sys.exit(app.exec_())
