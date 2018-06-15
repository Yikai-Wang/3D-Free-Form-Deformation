import vtk

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
    z = i / ((xl + 1) * (yl + 1))
    y = (i - z * (xl + 1) * (yl + 1)) / (xl + 1)
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
        n.append(int(xyz2index(x - 1, y, z)))
    if x < xl:
        n.append(int(xyz2index(x + 1, y, z)))
    if y > 0:
        n.append(int(xyz2index(x, y - 1, z)))
    if y < yl:
        n.append(int(xyz2index(x, y + 1, z)))
    if z > 0:
        n.append(int(xyz2index(x, y, z - 1)))
    if z < zl:
        n.append(int(xyz2index(x, y, z + 1)))
    # print('i, x, y, z', i, x, y, z)
    # print('its neighbor points\' index', n)
    return n


def sphereCallback(obj, event):
    count = 0
    for i in range(totalsphere):
        x, y, z = index2xyz(i)
        if (x + y + z) % 2 == 0:
            n = neighbor(i)
            for j in n:
                x1, y1, z1 = spherelist[i].GetCenter()
                x2, y2, z2 = spherelist[j].GetCenter()
                sourcelist[count].SetPoint1(x1, y1, z1)
                sourcelist[count].SetPoint2(x2, y2, z2)
                # Filter的连接可以通过方法SetInputConnection()和GetOutputPort()
                # 输出通过方法SetInputConnection()设置为vtkPolyDataMapper对象的输入
                mapperlist[count].SetInputConnection(sourcelist[count].GetOutputPort())
                # 设置定义几何信息的mapper到这个actor里
                # 在里 mapper的类型是vtkPolyDataMapper 也就是用类似点、线、多边形(Polygons)等几何图元进行渲染的
                actorlist[count].SetMapper(mapperlist[count])
                # 使用renderer的方法AddActor()把要渲染的actor加入到renderer中去。
                ren.AddActor(actorlist[count])
                count = count + 1



# create a rendering window and renderer
# 为了渲染actor需要创建图形对象, 先创建vtkRenderer的实例ren
ren = vtk.vtkRenderer()
# vtkRenderer的实例ren协调渲染窗口renWin的视口（viewport）的渲染过程
renWin = vtk.vtkRenderWindow()
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
    x, y, z = index2realworld(i)
    # 设置球状体在真实空间中的xyz坐标
    sphereWidget.SetCenter(x, y, z)
    # 设置球状体的半径大小
    sphereWidget.SetRadius(0.01)
    # 设置填充球状体的表面
    sphereWidget.SetRepresentationToSurface()
    # 要是没有这一行 球状体就不会显示出来了
    sphereWidget.On()
    spherelist.append(sphereWidget)

# draw lines
# 画线的
sourcelist = []
mapperlist = []
actorlist = []
for i in range(3 * totalsphere):
    sourcelist.append(vtk.vtkLineSource())
    # 添加vtkPolyDataMapper对象
    mapperlist.append(vtk.vtkPolyDataMapper())
    # 创建actor对象（要渲染的对象） 
    actorlist.append(vtk.vtkActor())

# The following code seems repeated with function sphereCallback(obj, event)
# count=0
# for i in range(totalsphere):
#     x, y, z = index2xyz(i)
#     if (x + y + z) % 2 == 0:
#         n = neighbor(i)
#         for j in n:
#             x1, y1, z1 = spherelist[i].GetCenter()
#             x2, y2, z2 = spherelist[j].GetCenter()
#             sourcelist[count].SetPoint1(x1, y1, z1)
#             sourcelist[count].SetPoint2(x2, y2, z2)
#             # 输出通过方法SetInputConnection()设置为vtkPolyDataMapper对象的输入
#             mapperlist[count].SetInputConnection(sourcelist[count].GetOutputPort())
#             # 设置定义几何信息的mapper到这个actor里
#             actorlist[count].SetMapper(mapperlist[count])
#             # 使用renderer的方法AddActor()把要渲染的actor加入到renderer中去。
#             ren.AddActor(actorlist[count])
#             count=count+1

# set interaction
# 用户方法通过定义一个函数并将其作为参数传入AddObserver来定义
# 添加Observer监听vtkRenderWindowInteractor里的事件，定义一系列回调函数（或命令）来实现交互。
# 将GUI交互器与用户自定义的渲染交互窗口交互器的方法关联起来
for i in range(totalsphere):
    spherelist[i].AddObserver("InteractionEvent", sphereCallback)


# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()
