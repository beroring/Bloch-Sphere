from math import sqrt, sin, cos, pi
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


def updated(theta, phi):
    global polygonSource, polygonSource1, polygonSource2, actorarrow
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


def callbackphi(obj, event):
    global actorarrow
    phi = obj.GetRepresentation().GetValue()
    theta = actorarrow.GetOrientation()[2]
    updated(theta, phi)


def callbacktheta(obj, event):
    global actorarrow
    theta = obj.GetRepresentation().GetValue()
    phi = actorarrow.GetOrientation()[1]
    phi = phi + 90
    updated(theta, phi)


class KeyPressInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.parent = vtkRenderWindowInteractor()
        if parent is not None:
            self.parent = parent

        self.AddObserver("KeyPressEvent", self.keyPress)

    def keyPress(self, obj, event):
        key = self.parent.GetKeySym()
        if key == '0':
            updated(0.0, 0.0)
            sliderRepN1.SetValue(0.0)
            sliderRepN2.SetValue(0.0)
            renderWindow.Render()
        if key == 'Up':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            updated(theta, phi + 1)
            sliderRepN1.SetValue(phi + 1)
            sliderRepN2.SetValue(theta)
            renderWindow.Render()
        if key == 'Down':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            updated(theta, phi - 1)
            sliderRepN1.SetValue(phi - 1)
            sliderRepN2.SetValue(theta)
            renderWindow.Render()
        if key == 'Left':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            updated(theta - 1, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta - 1)
            renderWindow.Render()
        if key == 'Right':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            updated(theta + 1, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta + 1)
            renderWindow.Render()
        if key == 'x':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            phi = 180 - phi
            theta = 360 - theta
            updated(theta, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta)
            renderWindow.Render()
        if key == 'y':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            phi = 180 - phi
            theta = 180 - theta
            updated(theta, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta)
            renderWindow.Render()
        if key == 'z':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            if theta >= 180:
                theta = theta - 180
            else:
                theta = theta + 180
            updated(theta, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta)
            renderWindow.Render()
        if key == 's':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            if theta < 90:
                theta = theta + 270
            else:
                theta = theta - 90
            updated(theta, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta)
            renderWindow.Render()
        if key == 't':
            phi = sliderRepN1.GetValue()
            theta = sliderRepN2.GetValue()
            if theta < 45:
                theta = theta + 315
            else:
                theta = theta - 45
            updated(theta, phi)
            sliderRepN1.SetValue(phi)
            sliderRepN2.SetValue(theta)
            renderWindow.Render()


def main():
    global actorarrow, renderWindow, sliderRepN1, sliderRepN2, polygonSource, polygonSource1, polygonSource2
    colors = vtkNamedColors()

    # Setup a renderer, render window, and interactor
    # 渲染器设置
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()

    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.SetInteractorStyle(KeyPressInteractorStyle(parent=renderWindowInteractor))

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

    sliderWidgetN1 = vtkSliderWidget()
    sliderWidgetN1.SetInteractor(renderWindowInteractor)
    sliderWidgetN1.SetRepresentation(sliderRepN1)
    sliderWidgetN1.EnabledOn()

    sliderWidgetN1.AddObserver("InteractionEvent", callbackphi)

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

    sliderWidgetN2 = vtkSliderWidget()
    sliderWidgetN2.SetInteractor(renderWindowInteractor)
    sliderWidgetN2.SetRepresentation(sliderRepN2)
    sliderWidgetN2.EnabledOn()

    sliderWidgetN2.AddObserver("InteractionEvent", callbacktheta)

    buttonRepN1 = vtk.vtkTexturedButtonRepresentation2D()
    # buttonRepN1.CreateDefaultProperties()
    # buttonRepN1.SetNumberOfStates(2)
    # bmpReader = vtk.vtkBMPReader()
    # bmpReader.SetFileName("Earth.bmp")
    # texture = vtk.vtkTexture()
    # texture.SetInputConnection(bmpReader.GetOutputPort())
    # texture.InterpolateOn()
    # buttonRepN1.SetButtonTexture(1, texture)
    # buttonRepN1.SetButtonTexture(2, 'Earth.bmp')

    buttonWidgetN1 = vtkButtonWidget()
    buttonWidgetN1.SetInteractor(renderWindowInteractor)
    buttonWidgetN1.SetRepresentation(buttonRepN1)
    buttonWidgetN1.EnabledOn()

    # 球体创建
    actorsphere = createsphere()
    actorsphere.GetProperty().SetColor(colors.GetColor3d('khaki'))
    renderer.AddActor(actorsphere)

    # 设置坐标系
    axes1 = MakeAxesActor()
    om1 = vtk.vtkOrientationMarkerWidget()
    om1.SetOrientationMarker(axes1)
    om1.SetViewport(0.35, 0.35, 0.65, 0.65)
    om1.SetInteractor(renderWindowInteractor)
    om1.EnabledOn()
    om1.InteractiveOff()

    # 窗口和相机设置
    renderer.SetBackground(colors.GetColor3d("AliceBlue"))
    renderWindow.SetSize(512, 512)

    camera = vtk.vtkCamera()
    camera.SetPosition(4.6, 2.0, 3.8)
    camera.SetFocalPoint(0.0, 0.0, 0.0)
    camera.SetClippingRange(3.2, 10.2)
    camera.SetViewUp(0.3, 0.13, 1.0)
    renderer.SetActiveCamera(camera)

    # 坐标系参考线
    actorx = createline()
    actory = createline([0, -2, 0], [0, 2, 0])
    actorz = createline([0, 0, -2], [0, 0, 2])
    renderer.AddActor(actorx)
    renderer.AddActor(actory)
    renderer.AddActor(actorz)

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
    renderer.AddActor(actorcircle)

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
    renderer.AddActor(actorcircle1)
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
    renderer.AddActor(actorcircle2)
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
    renderer.AddActor(actorarrow)

    renderer.SetBackground(colors.GetColor3d('SlateGray'))

    # 窗口显示及标题
    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderWindow.SetWindowName('A sphere')
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
