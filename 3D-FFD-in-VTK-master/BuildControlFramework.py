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
        print 'Error! Index not exists!'
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
                mapperlist[count].SetInputConnection(sourcelist[count].GetOutputPort())
                actorlist[count].SetMapper(mapperlist[count])
                ren.AddActor(actorlist[count])
                count = count + 1



# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# draw sphere
totalsphere = (xl + 1) * (yl + 1) * (zl + 1)
spherelist = []
for i in range(totalsphere):
    sphereWidget = vtk.vtkSphereWidget()
    sphereWidget.SetInteractor(iren)
    x, y, z = index2realworld(i)
    sphereWidget.SetCenter(x, y, z)
    sphereWidget.SetRadius(0.01)
    sphereWidget.SetRepresentationToSurface()
    sphereWidget.On()
    spherelist.append(sphereWidget)

# draw lines
sourcelist = []
mapperlist = []
actorlist = []
for i in range(3*totalsphere):
    sourcelist.append(vtk.vtkLineSource())
    mapperlist.append(vtk.vtkPolyDataMapper())
    actorlist.append(vtk.vtkActor())

count=0
for i in range(totalsphere):
    x, y, z = index2xyz(i)
    if (x + y + z) % 2 == 0:
        n = neighbor(i)
        for j in n:
            x1, y1, z1 = spherelist[i].GetCenter()
            x2, y2, z2 = spherelist[j].GetCenter()
            sourcelist[count].SetPoint1(x1, y1, z1)
            sourcelist[count].SetPoint2(x2, y2, z2)
            mapperlist[count].SetInputConnection(sourcelist[count].GetOutputPort())
            actorlist[count].SetMapper(mapperlist[count])
            ren.AddActor(actorlist[count])
            count=count+1

# set interaction
for i in range(totalsphere):
    spherelist[i].AddObserver("InteractionEvent", sphereCallback)


# enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()
