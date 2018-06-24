# 3D-Free-Form-Deformation

这是我们在数据可视化课程的期末project，项目成员包括[何占魁](https://github.com/AaronHeee)，[冉诗菡](https://github.com/Rshcaroline)和[王艺楷](https://github.com/Wang-Yikai)。

### 开发环境：

系统环境：Windows 10

开发语言： python>=3.5

软件包：numpy>=1.13.0, tensorFlow >= 1.4, vtk==8.1.0, qt==5.9.6 

### 示例：

不使用UI的情形：

```python
python VtkModel.py
```

可直接在vtk的框架下进行3D自由变形操作，支持Windows与Mac

使用UI的情形：

```
python UI.py
```

在pyqt框架下进行所有已实现的操作，包括变形、文件的读取与写入等，仅支持Windows。

### 注意事项：

1. OBJ文件存储时请以.obj为后缀，FFD文件存储时请以.FFD为后缀。
2. UI仅支持Windows系统环境。

### 代码结构：

###### FFD.py

```python
class obj_reader(object):
    def __init__(self, filename):
        """加载obj文件"""
class FFD(object)
    def __init__(self, num_x, num_y, num_z, object_file,object_points):
        """num_x,num_y,num_z,各维度控制点个数
        object_file,obj文件路径
        object_points,obj文件点数据"""
    def initial_ffd(self,initial=True):
        """初始化ffd"""
    def load_cp(self,path):
        """实现加载储存控制点改变值的FFD文件"""
    def save_cp(self,filename):
        """实现将控制点改变值存入FFD文件"""
    def B(self,i,u):
        """计算样条函数值"""
    def T_local(self,object_point):
        """计算FFD"""
    def changed_reset(self):
        """重置被改变的控制点以避免重复计算"""
    def changed_update(self,id,location):
        """更新被改变的控制点"""
    def update_control_point(self):
        """更新控制点位置"""
```

###### VtkModel.py

```python
class VtkModel(object):
    def __init__(self, ren=None, iren=None, filename="zxh-ape.obj", RESIZE = 1, COLOR = True, RADISU = 0.01, xl = 4, yl = 4, zl = 4):
        """
        参数初始化和画图初始化
        """
    def ijk2xyz(self, i, j, k):
        """
        i, j, k为控制点在x轴 y轴 z轴方向分别的索引值
        x, y, z为控制点在坐标系中的坐标
        该坐标由ffd算法根据读入进来的物体的大小自动生成 保证控制点为能恰好包裹住物体的长方体
        """
    def neighbor(self, i, j, k):
        """
        找到第i,j,k号球对应的所有邻居球体的索引值
        即:上下左右前后六个点 通过索引值返回即可 记得考虑索引边界情况
        """
    def loadOBJ(self):
        """
        初始化，加载模型.obj格式文件
        """
    def color(self):
        """
        上色：模型上色，仅对于带有RGB信息的.obj文件有效
        """
    def resize(self, RESIZE):
        """
        调整尺寸，对PolyData进行减采样，仅对于Triangle类型有效
        """
    def drawFace(self, COLOR=False, RESIZE=1.0):
        """
        初始化 画出人脸 可以选择是否需要着色以及是否需要压缩图像
        """
    def drawControlPoints(self):
        """
        生成控制点球体
        """
    def drawLines(self):
        """
        初始化画线 生成用于保存线的sourcelist, mapperlist, actorlist
        获取每个控制点球体的位置并保存在spherelocation中
        将每个控制点与其邻居结点连接起来
        """
    def addControlPointsObserver(self):
        """
        对于每一个球体控制点 添加Observer监听vtkRenderWindowInteractor里的事件
        用户方法通过定义一个回调函数sphereCallback并将其作为参数传入AddObserver来定义
        该函数将GUI交互器与用户自定义的渲染交互窗口交互器的方法关联起来
        """ 
    def sphereCallback(self, obj, event):
        """
        对于控制点的回调交互函数
        主要功能为: 
        	检查控制点是否被拽动
        	对于被拽动的控制点: 去掉旧的邻居结点连线并增加新的连线
        					 去掉旧的人脸并调用ffd算法生成新的人脸
        """
```

###### UI.py

```python
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
	"""设置UI主界面
	"""
class SimpleView(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """继承QMainWindow类，初始化界面
        """
    def initVTK(self, dots=5):
        """初始化VTK
        """
    def showAll(self):
	   """开启界面展示
	   """
    def createActions(self):
       """创建按钮
       """
    def createMenus(self):
       """创建工具栏
       """
    def load_obj(self):
	  """读入.obj文件槽函数"""
	  """后槽函数均结构类似，在此略过"""
```

关于project的更详细介绍请参考[这里](https://github.com/Wang-Yikai/3D-Free-Form-Deformation/blob/master/report/report.md)。

### 致谢：

衷心感谢下列优秀开源项目：

[PRNet](https://github.com/YadiraF/PRNet)

[3D-FFD-in-VTK](https://github.com/Anthony-Xu/3D-FFD-in-VTK)

感谢庄吓海老师和徐辉学长在我们做pj的过程中对我们的帮助！