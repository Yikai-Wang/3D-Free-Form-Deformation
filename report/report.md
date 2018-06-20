---
typora-copy-images-to: ./pics
---

# 数据可视化期末项目

---

**姓名：** 王艺楷、冉诗菡、何占魁

**学号：** 15300180076、15307130424、15307130175

---



## 任务：FFD三维形变平台 

>1. 作业以小组形式:每个小组3个人。提交作业时只要一个代表提交就可以。记住:不要多人重复提交。 
>2. 提交内容包括: 
>   - 报告:在报告中清晰描述问题和数据，数据处理的各个步骤及中间结果，代码结构，开发环境，可执行文件使用手册等细节问题。 
>   - 代码:使用Python(Matlab或C/C++)开发;代码要有非常清晰的注释。 
>   - 提交可执行文件 
>   - 测试数据 
>   - 鼓励用视频解释可视化操作过程与展示结果 
>3. 截止时间
>   - 6月24日23:00 (16周结束)
>   - 7月22日23:00 (20周结束，难度和完成分:(A/10)^2) 

#### 一、问题和数据：

1. ##### 问题描述：

   基于VTK或其他显示库开发一个具有GUI功能的工具，用于实现3D Free-Form Deformation (FFD)的可视化和交互。

   功能要求：

   - 可以人工设置调节每个控制点的位移
   - 可以读入FFD文件设置位移，输出FFD(.FFD格式)
   - 可视化形变场，如使用网格线和surface model(vtk polydata格式)

2. ##### 数据描述：

   ###### OBJ文件：

   ​	OBJ文件是Wavefront公司为它的一套基于工作站的3D建模和动画软件"Advanced Visualizer"开发的一种文件格式。OBJ文件是一种文本文件，可以直接用写字板打开进行查看和编辑修改。支持多边形(Polygon)，直线(Lines)，表面(Surfaces)，和自由形态曲线(Free-form Curves)。直线和多角形通过它们的点来描述，曲线和表面则根据于它们的控制点和依附于曲线类型的额外信息来定义。这些信息支持规则和不规则的曲线，包括那些基于贝塞尔(Bezier)曲线，B样条(B-spline)，基数(Cardinal/Catmull-Rom样条)，和泰勒方程(Taylor equations)的曲线。

   ​	OBJ文件由一行行文本组成，注释行以一个 # 号为开头，空格和空行可以随意加到文件中以增加文件的可读性。有字的行都由一两个标记字母也就是关键字(Keyword)开头，关键字可以说明这一行是什么样的数据。多行可以逻辑地连接在一起表示一行，方法是在每一行最后添加一个连接符(\)。

   ​	在我们的OBJ文件中，以v关键字开头的行表示几何体的顶点数据，以f关键字开头的行表示几何体的面数据。

   ###### FFD文件：

   ​	FFD文件是一种自定义文件格式，用来存储进行FFD变换后每个控制点的位移数据。

   ​	FFD文件的每个区域以双##开头，##内部表明从下一行开始的数据含义，如dimension，offsets等。从##的下一行开始到下一个##号或文件截止为该##号所描述的数据内容。控制点的位移由一个三维的数组表示，具体的：设三个维度为$[x,y,z]$,不同的x维度之间以一个空行隔开，同一x维之间不同的y维由一个换行符隔开，同一xy维之间不同的z维由一个tab隔开，每个xyz维存储一个三维的控制点位移，每个维度之间由空格隔开。

#### 二、数据处理：

1. ##### 算法描述：

   ###### 3D Free-Form Deformation (FFD)

   FFD的主要目的是通过对全局形变函数和局部形变函数的构造达到对非刚性形变的模拟。即将形变函数:
   $$
   \textbf{T}:(x,y,z)\rightarrow (x^{'},y^{'},z^{'})
   $$
   构造为为全局形变函数和局部形变函数的组合：
   $$
   \textbf{T}(x,y,z)=\textbf{T}_{global}(x,y,z)+\textbf{T}_{local}(x,y,z)
   $$
   其中，全局性变函数是一个自由变换(affine transformation).定义为：
   $$
   \textbf{T}_{global}(x,y,z)=\left(\begin{matrix}\theta_{11}&\theta_{12}&\theta_{13}\\\theta_{21}&\theta_{22}&\theta_{23}\\\theta_{31}&\theta_{32}&\theta_{33}\end{matrix}\right)\left(\begin{matrix}x\\y\\z\end{matrix}\right)+\left(\begin{matrix}\theta_{14}\\\theta_{24}\\\theta_{34}\end{matrix}\right)
   $$
   为了定义基于样条函数的局部形变FFD，我们定义物体所占据的区域为$\Omega=\{(x,y,z)|0\leq x<X,0\leq y <Y,0\leq z<Z\}$.定义$\Phi$为体积为$n_x*n_y*n_z$的控制点网络，其中$n_i$为第i个维度相邻控制点之间的距离。那么FFD可以被定义为一维立方B样条的三维张量积：
   $$
   \textbf{T}_{local}(x,y,z)=\sum_{l=0}^3\sum_{m=0}^3\sum_{n=0}^3B_t(u)B_m(v)B_n(w)\phi_{i+l,j+m,k+n}
   $$
   其中$i=\lfloor x/n_x\rfloor-1,j=\lfloor y/n_y\rfloor-1,k=\lfloor z/n_z\rfloor-1,\\u=x/n_x-\lfloor x/n_x\rfloor,v=y/n_y-\lfloor y/n_y\rfloor,w=z/n_z-\lfloor z/n_z\rfloor$

   样条函数的定义如下:
   $$
   B_0(u)=\frac{(1-u)^3}{6}\\
   B_1(u)=\frac{3u^3-6u^2+4}{6}\\
   B_2(u)=\frac{-3u^3+3u^2+3u+1}{6}\\
   B_1(u)=\frac{u^3}{6}
   $$



   ###### Control Framework

   - **控制点生成**
     - 确定控制点位置和数量：首先需要根据读入文件的坐标位置确定控制点的位置，我们在目标物体的周围生成$n\times n\times n$的立方体，使得该立方体恰好“包裹”住目标物体。
     - 生成球体：在每一个控制点的位置利用`vtk.vtkSphereWidget()`生成一个球体，配置球体半径、颜色等属性。
   - **控制点间邻居结点连线生成**
     - 计算邻居结点：对于每一个控制点球体，计算以它为中心的前后上下左右的六个邻居结点的位置。
     - 邻居结点连线：将每个控制点与他们所对应的邻居结点用`vtk.vtkLineSource()`连接起来。
   - **设置控制点监听器**
     - 对于每一个控制点，利用`AddObserver`监听`vtkRenderWindowInteractor`里的事件。
   - **进行交互**
     - 我们定义回调函数`sphereCallback`来实现交互。
     - 在该回调函数中，会对每个控制点球体的位置进行查询，如果球体位置发生更新，则重新生成该球体与邻居结点的连线，并把该球体的新位置返回给FFD算法进行计算形变。
     - 获取FFD算法计算好后的数据，用`RemoveActor`去除之前显示的物体并用`AddActor`显示更新形变后的物体。

   ###### GUI(@he)

   

2. ##### 图像处理：

   ###### 利用照片重建3D人脸

   - 利用论文 [Joint 3D Face Reconstruction and Dense Alignment with Position Map Regression Network](https://arxiv.org/abs/1803.07835) 提出的PRNet对照片中的人脸进行3D重建。

   - 将人脸导出成带有纹理信息的obj文件，方便后期读入obj文件用FFD算法对人脸进行形变。

     ![alignment](pics/reconstruct.jpg)

   

   ###### OBJ文件读入和纹理着色(@kai读入 @he着色)

   OBJ文件的读入分为两个部分：
   1. 通过vtk的OBJReader读取OBJ文件进行画图
   2. 按照OBJ文件的规则读取每个点的坐标，存储到内存中，为FFD算法的计算做准备。

   ###### 控制点位置确定

   首先由读入的OBJ文件计算初始的控制点位置，其次若加载FFD文件则对每一个控制点更新位移。具体的，初始控制点的计算方法为：
   1. 将OBJ文件形成的3D人脸嵌入长方体中，计算得出长方体的长宽高。
   2. 根据预先定义的控制点间隔将长方体切割，切割成的每个小长方体的顶点作为控制点的坐标。

   

3. ##### 变形结果：

   ==放几个截图==

   ![image-20180620220609903](pics/image-20180620220609903.png)

      

   ==可以列举不同文件的形变耗时对比==





#### 三、代码结构：(@kai @he)

##### FFD算法(@kai)



##### 控制点框架

```python
class VtkModel(object):
    def __init__(self):
        # 参数初始化及进行初始化画图

    def xyz2index(self, x, y, z):
        """
        xyz为控制点在xyz轴方向分别的index
        index为控制点在self.totalsphere这么多个球中的index
        """

    def index2xyz(self, i):
        """
        index转xyz
        """

    def xyz2realworld(self, x, y, z):
        """
        xr, yr, zr为控制点在realworld中的坐标
        该坐标由ffd算法根据读入进来的物体的大小自动生成 保证控制点为能恰好包裹住物体的长方体
        """

    def index2realworld(self, i):
        """
        找到第i号球对应的真实坐标
        """

    def neighbor(self, i):
        """
        找到第i号球对应的所有邻居球体的index
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
        生成self.totalsphere这么多个控制点球体
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
        主要功能为: 检查控制点是否被拽动 连接新的线 去掉人脸并调用ffd算法生成新的人脸
        """
```


##### GUI(@he)

 



#### 四、开发环境：
-  **系统环境：**macOS High Serria
-  **开发语言：**Python>=3.5
-  **软件包：**Numpy>=1.13.0,  TensorFlow >= 1.4




#### 五、可执行文件使用： 

-  **使用环境：**macOS

-  **文件名称**：

-  **使用方式：**

-  **补充说明：**



#### 六、一些尝试：

#### 

#### 七、合作者贡献：

-  **王艺楷：**FFD算法实现，报告撰写

-  **冉诗菡：**控制点算法及交互实现，报告撰写

-  **何占魁：** GUI实现，报告撰写

   ​


