# coding=utf-8
import vtk
from FFD import obj_reader, FFD
import numpy as np
from time import time
from ObjProcessing import resize_poly_data, color_on_points, read_color_from_ffd


class VtkModel(object):
    def __init__(self, ren=None, iren=None, filename="zxh-ape.obj", RESIZE = 1, COLOR = True, RADISU = 0.05, xl = 4, yl = 4, zl = 4):
        # 参数初始化
        self.ren = ren
        self.iren = iren
        self.filename = filename
        self.RESIZE = RESIZE
        self.RADISU = RADISU
        self.COLOR = COLOR
        self.xl = xl
        self.yl = yl
        self.zl = zl
        self.totalsphere = (self.xl + 1) * (self.yl + 1) * (self.zl + 1)

        # 设置背景颜色
        self.ren.SetBackground(237, 237, 237)

        # 用TrackballCamera的交互方式
        InteractorStyle = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(InteractorStyle)

        # 初始化画图
        self.loadOBJ()
        self.drawFace()
        self.drawControlPoints()
        self.drawLines()
        self.addControlPointsObserver()


    def xyz2index(self, x, y, z):
        """
        xyz为控制点在xyz轴方向分别的index
        index为控制点在self.totalsphere这么多个球中的index
        For example, xyz2index(0,0,0)=0, xyz2index(0,0,1)=1
        """
        index = (self.xl + 1) * (self.yl + 1) * z + (self.xl + 1) * y + x
        return index


    def index2xyz(self, i):
        """
        For example, index2xyz(1)=(0,0,1)
        """
        z = i // ((self.xl + 1) * (self.yl + 1))
        y = (i - z * (self.xl + 1) * (self.yl + 1)) // (self.xl + 1)
        x = i % (self.xl + 1)
        return x, y, z


    def xyz2realworld(self, x, y, z):
        """
        xr, yr, zr为控制点在realworld中的坐标
        该坐标由ffd算法根据读入进来的物体的大小自动生成 保证控制点为能恰好包裹住物体的长方体
        """
        xr, yr, zr = self.ffd.control_points_location[x][y][z]
        return xr, yr, zr


    def index2realworld(self, i):
        """
        找到第i号球对应的真实坐标
        """
        'Input an index. Output the position of that point in realworld. 0<=xr<=1.'
        if i >= (self.xl + 1) * (self.yl + 1) * (self.zl + 1):
            print('Error! Index not exists!')
            return 0
        x, y, z = self.index2xyz(i)
        xr, yr, zr = self.xyz2realworld(x, y, z)
        return xr, yr, zr


    def neighbor(self, i):
        """
        找到第i号球对应的所有邻居球体的index
        """
        x, y, z = self.index2xyz(i)
        n = []
        if x > 0:
            n.append(self.xyz2index(x - 1, y, z))
        if x < self.xl:
            n.append(self.xyz2index(x + 1, y, z))
        if y > 0:
            n.append(self.xyz2index(x, y - 1, z))
        if y < self.yl:
            n.append(self.xyz2index(x, y + 1, z))
        if z > 0:
            n.append(self.xyz2index(x, y, z - 1))
        if z < self.zl:
            n.append(self.xyz2index(x, y, z + 1))
        return n
        

    def loadOBJ(self):
        """
        初始化，加载模型.obj格式文件
        """
        self.reader = vtk.vtkOBJReader()
        self.reader.SetFileName(self.filename)
        self.reader.Update()
        self.data = self.reader.GetOutput()

    def color(self):
        """
        上色：模型上色，仅对于带有RGB信息的.obj文件有效
        """
        if self.COLORED:
            return
        else:
            self.data.GetPointData().SetScalars(self.data_color.GetPointData().GetScalars())
            self.COLORED = True
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.data)

        self.ren.RemoveActor(self.actor)
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.ren.AddActor(self.actor)
    
    def resize(self, RESIZE):
        """
        调整尺寸，对PolyData进行减采样，仅对于Triangle类型有效
        """
        self.data = resize_poly_data(self.data, RESIZE)
        self.data_color = resize_poly_data(self.data_color, RESIZE)

        points = self.data.GetPoints()
        vertices = [points.GetPoint(i) for i in range(points.GetNumberOfPoints())]
        self.ffd = FFD(num_x=self.xl + 1, num_y=self.yl + 1, num_z=self.zl + 1, object_points=vertices,object_file=self.filename)
        self.ffd.initial_ffd()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.data)

        self.ren.RemoveActor(self.actor)
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.ren.AddActor(self.actor)

    def drawFace(self, COLOR=False, RESIZE=1.0):
        """
        初始化 画出人脸 可以选择是否需要着色以及是否需要压缩图像
        """

        # 深拷贝一份着色PolyData，解决GUI中上色和RESIZE的逻辑冲突 
        self.data_color = vtk.vtkPolyData()
        self.data_color.DeepCopy(self.data)
        self.data_color = color_on_points(self.data_color, read_color_from_ffd(self.filename))
        self.COLORED = False

        # 如果需要着色的话
        if COLOR :
            self.color()
        # 如果需要压缩图像的话
        if RESIZE != 1:
            self.data = resize_poly_data(self.data, RESIZE)
            self.data_color = resize_poly_data(self.data_color, RESIZE)
            
        points = self.data.GetPoints()
        vertices = [points.GetPoint(i) for i in range(points.GetNumberOfPoints())]
        self.ffd = FFD(num_x=self.xl + 1, num_y=self.yl + 1, num_z=self.zl + 1, object_points=vertices,object_file=self.filename)
        self.ffd.initial_ffd()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.data)

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.ren.AddActor(self.actor)

    def drawControlPoints(self):
        """
        生成self.totalsphere这么多个控制点球体
        """
        self.spherelist = []
        for i in range(self.totalsphere):
            # 定义一个球状体widget
            sphereWidget = vtk.vtkSphereWidget()
            # 渲染窗口交互器实例iren是一个3D的球状体widget
            sphereWidget.SetInteractor(self.iren)
            # 从index对应到真实空间中的xyz坐标
            x, y, z = self.index2realworld(i)
            # 设置球状体在真实空间中的xyz坐标
            sphereWidget.SetCenter(x, y, z)
            # 设置球状体的半径大小
            sphereWidget.SetRadius(self.RADISU)
            # 设置球面的颜色 仍然是通过GetProperty来获取属性并进行设置
            # sphereWidget.GetSphereProperty().SetColor(0, 1.0, 0)
            # 设置填充球状体的表面 三种基本的属性设置方式：点方式，网格方式和面方式
            sphereWidget.SetRepresentationToSurface()
            # 要是没有这一行 球状体就不会显示出来了
            sphereWidget.On()
            # 将球状体添加到球状体的列表中
            self.spherelist.append(sphereWidget)


    def drawLines(self):
        """
        初始化画线 生成用于保存线的sourcelist, mapperlist, actorlist
        获取每个控制点球体的位置并保存在spherelocation中
        将每个控制点与其邻居结点连接起来
        """
        self.sourcelist = []
        self.mapperlist = []
        self.actorlist = []
        # 多初始化一些 存到list里面 因为线的总数是比球的总数多的
        for i in range((self.xl+1) * self.totalsphere):
            self.sourcelist.append(vtk.vtkLineSource())
            # 添加vtkPolyDataMapper对象
            self.mapperlist.append(vtk.vtkPolyDataMapper())
            # 创建actor对象（要渲染的对象） 
            self.actorlist.append(vtk.vtkActor())

        count = 0
        self.spherelocation = []
        for i in range(self.totalsphere):
            # 对于一个球体i 获取球心的位置
            x1, y1, z1 = self.spherelist[i].GetCenter()
            # 初始化时记录球体的位置
            self.spherelocation.append([x1, y1, z1])
            n = self.neighbor(i)
            for j in n:
                # 对于这个球体i的邻居j 获取球心的位置
                x2, y2, z2 = self.spherelist[j].GetCenter()
                # 设置一条线的起点和终点
                self.sourcelist[count].SetPoint1(x1, y1, z1)
                self.sourcelist[count].SetPoint2(x2, y2, z2)
                # Filter的连接可以通过方法SetInputConnection()和GetOutputPort()
                # 输出通过方法SetInputConnection()设置为vtkPolyDataMapper对象的输入
                self.mapperlist[count].SetInputConnection(self.sourcelist[count].GetOutputPort())
                # 设置定义几何信息的mapper到这个actor里
                # 在里 mapper的类型是vtkPolyDataMapper 也就是用类似点、线、多边形(Polygons)等几何图元进行渲染的
                self.actorlist[count].SetMapper(self.mapperlist[count])
                # vtkActor.GetProperty()->SetColor() not working for me
                # ref: http://vtk.1045678.n5.nabble.com/vtkActor-GetProperty-gt-SetColor-not-working-for-me-td5722373.html
                self.actorlist[count].GetMapper().ScalarVisibilityOff()
                # 设置Actor的颜色 该方法用RGB值来设置一个Actor的红、绿、蓝分量的颜色 每个分量的取值范围从0到1
                self.actorlist[count].GetProperty().SetColor(0, 1.0, 0)
                # 使用renderer的方法AddActor()把要渲染的actor加入到renderer中去。
                self.ren.AddActor(self.actorlist[count])
                count += 1


    def addControlPointsObserver(self):
        """
        对于每一个球体控制点 添加Observer监听vtkRenderWindowInteractor里的事件
        用户方法通过定义一个回调函数sphereCallback并将其作为参数传入AddObserver来定义
        该函数将GUI交互器与用户自定义的渲染交互窗口交互器的方法关联起来
        """
        for i in range(self.totalsphere):
            self.spherelist[i].AddObserver("InteractionEvent", self.sphereCallback)


    def sphereCallback(self, obj, event):
        """
        对于控制点的回调交互函数 主要功能为: 检查控制点是否被拽动 连接新的线 去掉人脸并调用ffd算法生成新的人脸
        """
        self._sphereCallback()

    def sphereQt(self, xyz_index, xyz):
        sphere_index = self.xyz2index(*xyz_index)
        self.spherelist[sphere_index].SetCenter(xyz)
        self._sphereCallback()

    def _sphereCallback(self):
        count = 0
        for i in range(self.totalsphere):
            # 对于一个球体i 获取它之前的位置
            x0, y0, z0 = self.spherelocation[i]
            # 对于一个球体i 获取它现在球心的位置
            x1, y1, z1 = self.spherelist[i].GetCenter()

            # 如果球体的位置发生改变 即该控制点被拖动
            if x1!=x0 or y1!=y0 or z1!=z0:
                print('Before location', x0, y0, z0)
                print("New location", x1, y1, z1)
                # 将更新后的坐标点传给ffd算法保存下来
                i, j, k = self.index2xyz(i)
                print(i,j,k)
                self.ffd.changed_update((i, j, k), np.array([x1, y1, z1]))
                # 更新spherelocation里面保存的每一个球体的位置
                self.spherelocation[i] = [x1, y1, z1]

            # 计算邻居结点 方便连线
            n = self.neighbor(i)
            for j in n:
                # 对于这个球体i的邻居j 获取球心的位置
                x2, y2, z2 = self.spherelist[j].GetCenter()
                # 设置一条线的起点和终点
                self.sourcelist[count].SetPoint1(x1, y1, z1)
                self.sourcelist[count].SetPoint2(x2, y2, z2)
                # Filter的连接可以通过方法SetInputConnection()和GetOutputPort()
                # 输出通过方法SetInputConnection()设置为vtkPolyDataMapper对象的输入
                self.mapperlist[count].SetInputConnection(self.sourcelist[count].GetOutputPort())
                # 设置定义几何信息的mapper到这个actor里
                # 在里 mapper的类型是vtkPolyDataMapper 也就是用类似点、线、多边形(Polygons)等几何图元进行渲染的
                self.actorlist[count].SetMapper(self.mapperlist[count])
                # vtkActor.GetProperty()->SetColor() not working for me
                # ref: http://vtk.1045678.n5.nabble.com/vtkActor-GetProperty-gt-SetColor-not-working-for-me-td5722373.html
                self.actorlist[count].GetMapper().ScalarVisibilityOff()
                # 设置Actor的颜色 该方法用RGB值来设置一个Actor的红、绿、蓝分量的颜色 每个分量的取值范围从0到1
                self.actorlist[count].GetProperty().SetColor(0, 1.0, 0)
                # 使用renderer的方法AddActor()把要渲染的actor加入到renderer中去。
                self.ren.AddActor(self.actorlist[count])
                count += 1
            
        print('Begin FFD...')
        print('Calculating...')
        # 更新控制点
        self.ffd.update_control_point()
        points = self.data.GetPoints()

        # 进行计算 并将计算后更改后的数据存入data的points数据中
        t1 = time()
        for i in range(len(self.ffd.object_points)):
            tmp = self.ffd.T_local(self.ffd.object_points[i])
            if tmp[0]!=0 or tmp[1]!=0 or tmp[2]!=0:
                points.SetPoint(i,tuple(self.ffd.object_points[i]+tmp))
        print(time()-t1)

        # 构造mapper
        self.ffd.changed_initial()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.data)

        # 去掉原始的人脸
        self.ren.RemoveActor(self.actor)
        # 添加更改后的新的人脸
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.ren.AddActor(self.actor)
        print('Done FFD')        

if __name__ == "__main__":
    "python VtkModel.py to test"

    ren = vtk.vtkRenderer()
    iren = vtk.vtkRenderWindowInteractor()
    renWin = vtk.vtkRenderWindow()

    renWin.AddRenderer(ren)
    iren.SetRenderWindow(renWin)

    VtkModel(ren=ren, iren=iren)

    iren.Initialize()
    renWin.Render()
    iren.Start()