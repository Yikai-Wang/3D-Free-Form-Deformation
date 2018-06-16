import vtk
import FFD

#  xl means how long is x. For example, if xl==2, then there are 3 control points in x-axe.
#  In fact, this is not the real world distance. I set real world distance to be 1.
xl = 5
yl = 5
zl = 5


def xyz2index(x, y, z):
    'For example, xyz2index(0,0,0)=0, xyz2index(0,0,1)=1'
    index = (xl + 1) * (yl + 1) * z + (xl + 1) * y + x
    return index


def index2xyz(i):
    'For example, index2xyz(1)=(0,0,1)'
    z = i // ((xl + 1) * (yl + 1))
    y = (i - z * (xl + 1) * (yl + 1)) // (xl + 1)
    x = i % (xl + 1)
    return x, y, z


def xyz2realworld(x, y, z):
    'Input x, y, z is int. Output xr, yr, zr is float. 0<=xr<=1.'
    xr = float(x) / xl
    yr = float(y) / yl
    zr = float(z) / zl
    return xr, yr, zr


def index2realworld(i):
    'Input an index. Output the position of that point in realworld. 0<=xr<=1.'
    if i >= (xl + 1) * (yl + 1) * (zl + 1):
        print('Error! Index not exists!')
        return 0
    x, y, z = index2xyz(i)
    xr, yr, zr = xyz2realworld(x, y, z)
    return xr, yr, zr


def neighbor(i):
    'i is index, return its neighbor points'
    x, y, z = index2xyz(i)
    n = []
    if x > 0:
        n.append(xyz2index(x - 1, y, z))
    if x < xl:
        n.append(xyz2index(x + 1, y, z))
    if y > 0:
        n.append(xyz2index(x, y - 1, z))
    if y < yl:
        n.append(xyz2index(x, y + 1, z))
    if z > 0:
        n.append(xyz2index(x, y, z - 1))
    if z < zl:
        n.append(xyz2index(x, y, z + 1))
    # print('i, x, y, z', i, x, y, z)
    # print('its neighbor points\' index', n)
    return n


def sphereCallback(obj, event):
    count = 0
    for i in range(totalsphere):
        # x, y, z = index2xyz(i)
        # if (x + y + z) % 2 == 0:
        n = neighbor(i)
        for j in n:
            # print('j:', j)
            # print('spherelist:', len(spherelist))
            # 对于一个球体i 获取球心的位置
            x1, y1, z1 = spherelist[i].GetCenter()
            # 对于这个球体i的邻居j 获取球心的位置
            x2, y2, z2 = spherelist[j].GetCenter()
            # 设置一条线的起点和终点
            sourcelist[count].SetPoint1(x1, y1, z1)
            sourcelist[count].SetPoint2(x2, y2, z2)
            # Filter的连接可以通过方法SetInputConnection()和GetOutputPort()
            # 输出通过方法SetInputConnection()设置为vtkPolyDataMapper对象的输入
            mapperlist[count].SetInputConnection(sourcelist[count].GetOutputPort())
            # 设置定义几何信息的mapper到这个actor里
            # 在里 mapper的类型是vtkPolyDataMapper 也就是用类似点、线、多边形(Polygons)等几何图元进行渲染的
            actorlist[count].SetMapper(mapperlist[count])
            # vtkActor.GetProperty()->SetColor() not working for me
            # ref: http://vtk.1045678.n5.nabble.com/vtkActor-GetProperty-gt-SetColor-not-working-for-me-td5722373.html
            actorlist[count].GetMapper().ScalarVisibilityOff()
            # 设置Actor的颜色 该方法用RGB值来设置一个Actor的红、绿、蓝分量的颜色 每个分量的取值范围从0到1
            actorlist[count].GetProperty().SetColor(0, 1.0, 0)
            # 使用renderer的方法AddActor()把要渲染的actor加入到renderer中去。
            ren.AddActor(actorlist[count])
            count += 1



# create a rendering window and renderer
# 为了渲染actor需要创建图形对象, 先创建vtkRenderer的实例ren
ren = vtk.vtkRenderer()
# 设置背景颜色
# ren.SetBackground(1, 1, 1)

# add face 
filename = "/Users/ranshihan/Coding/3D-Free-Form-Deformation/zxh-ape.obj"
reader = vtk.vtkOBJReader()
reader.SetFileName(filename)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

ren.AddActor(actor)

# vtkRenderer的实例ren协调渲染窗口renWin的视口（viewport）的渲染过程
renWin = vtk.vtkRenderWindow()
renWin.SetSize(1024*2, 528*3)
# 通过渲染窗口类的方法AddRenderer()把renderer和渲染窗口关联起来
renWin.AddRenderer(ren)

# create a renderwindowinteractor
# 实例化一个vtkRenderWindowInterator对象 方便用户进行数据交互
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# draw sphere
# 画球体
totalsphere = (xl + 1) * (yl + 1) * (zl + 1)
spherelist = []
for i in range(totalsphere):
    # 定义一个球状体widget
    sphereWidget = vtk.vtkSphereWidget()
    # 渲染窗口交互器实例iren是一个3D的球状体widget
    sphereWidget.SetInteractor(iren)
    # 从index对应到真实空间中的xyz坐标
    x, y, z = index2realworld(i)
    # 设置球状体在真实空间中的xyz坐标
    sphereWidget.SetCenter(x, y, z)
    # 设置球状体的半径大小
    sphereWidget.SetRadius(0.01)
    # 设置球面的颜色 仍然是通过GetProperty来获取属性并进行设置
    # sphereWidget.GetSphereProperty().SetColor(0, 1.0, 0)
    # 设置填充球状体的表面 三种基本的属性设置方式：点方式，网格方式和面方式
    sphereWidget.SetRepresentationToSurface()
    # 要是没有这一行 球状体就不会显示出来了
    sphereWidget.On()
    # 将球状体添加到球状体的列表中
    spherelist.append(sphereWidget)

# draw lines
# 画线
sourcelist = []
mapperlist = []
actorlist = []
# 多初始化一些 存到list里面
for i in range(100 * totalsphere):
    sourcelist.append(vtk.vtkLineSource())
    # 添加vtkPolyDataMapper对象
    mapperlist.append(vtk.vtkPolyDataMapper())
    # 创建actor对象（要渲染的对象） 
    actorlist.append(vtk.vtkActor())

count = 0
for i in range(totalsphere):
    # x, y, z = index2xyz(i)
    # if (x + y + z) % 2 == 0:
    n = neighbor(i)
    for j in n:
        # print('j:', j)
        # print('spherelist:', len(spherelist))
        # 对于一个球体i 获取球心的位置
        x1, y1, z1 = spherelist[i].GetCenter()
        # 对于这个球体i的邻居j 获取球心的位置
        x2, y2, z2 = spherelist[j].GetCenter()
        # 设置一条线的起点和终点
        sourcelist[count].SetPoint1(x1, y1, z1)
        sourcelist[count].SetPoint2(x2, y2, z2)
        # Filter的连接可以通过方法SetInputConnection()和GetOutputPort()
        # 输出通过方法SetInputConnection()设置为vtkPolyDataMapper对象的输入
        mapperlist[count].SetInputConnection(sourcelist[count].GetOutputPort())
        # 设置定义几何信息的mapper到这个actor里
        # 在里 mapper的类型是vtkPolyDataMapper 也就是用类似点、线、多边形(Polygons)等几何图元进行渲染的
        actorlist[count].SetMapper(mapperlist[count])
        # vtkActor.GetProperty()->SetColor() not working for me
        # ref: http://vtk.1045678.n5.nabble.com/vtkActor-GetProperty-gt-SetColor-not-working-for-me-td5722373.html
        actorlist[count].GetMapper().ScalarVisibilityOff()
        # 设置Actor的颜色 该方法用RGB值来设置一个Actor的红、绿、蓝分量的颜色 每个分量的取值范围从0到1
        actorlist[count].GetProperty().SetColor(0, 1.0, 0)
        # 使用renderer的方法AddActor()把要渲染的actor加入到renderer中去。
        ren.AddActor(actorlist[count])
        count += 1


# set interaction
# 用户方法通过定义一个函数并将其作为参数传入AddObserver来定义
# 添加Observer监听vtkRenderWindowInteractor里的事件，定义一系列回调函数（或命令）来实现交互
# 将GUI交互器与用户自定义的渲染交互窗口交互器的方法关联起来
for i in range(totalsphere):
    spherelist[i].AddObserver("InteractionEvent", sphereCallback)

# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()
