import sys
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton,QHBoxLayout, QVBoxLayout, QApplication, QInputDialog, QMessageBox, QMainWindow,QAction,QFileDialog)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from VtkModel import VtkModel
import vtk
import gc

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.createActions()
        self.createMenus()
        #self.initUI()
        self.initVTK()
        self.showAll()

    def createActions(self):
        self.load_obj_Action = QAction('加载obj文件', self, triggered=self.load_obj)
        self.load_image_Action = QAction('加载照片', self, triggered=self.load_image)
        self.load_ffd_Action = QAction('加载控制点', self, triggered=self.load_ffd)
        self.save_obj_Action = QAction('存储obj文件', self, triggered=self.save_obj)
        self.save_ffd_Action = QAction('存储控制点', self, triggered=self.save_ffd)
        self.reset_Action = QAction('RESET', self, triggered=self.slot_reset)
        self.color_Action = QAction('COLOR', self, triggered=self.slot_color)
        self.quit_Action = QAction('QUIT', self, triggered=QApplication.instance().quit)
        self.xyz_Action = QAction('SET XYZ', self, triggered=self.slot_xyz)
        self.resize_Action = QAction('RESIZE', self, triggered=self.slot_resize)

    def createMenus(self):
        self.menuBar().setNativeMenuBar(False)
        self.loadMenu = self.menuBar().addMenu('Load')
        self.saveMenu = self.menuBar().addMenu('Save')
        self.changeMenu = self.menuBar().addMenu('Modify')
        self.loadMenu.addAction(self.load_obj_Action)
        self.loadMenu.addAction(self.load_image_Action)
        self.loadMenu.addAction(self.load_ffd_Action)
        self.saveMenu.addAction(self.save_obj_Action)
        self.saveMenu.addAction(self.save_ffd_Action)
        self.changeMenu.addAction(self.reset_Action)
        self.changeMenu.addAction(self.color_Action)
        self.changeMenu.addAction(self.quit_Action)
        self.changeMenu.addAction(self.xyz_Action)
        self.changeMenu.addAction(self.resize_Action)

    def load_obj(self):
        filename, ok = QFileDialog.getOpenFileName(self, '加载obj文件', '/home')
        if ok:
            self.model.filename=filename
            self.model.loadOBJ()
        return

    def load_image(self):
        filename, ok = QFileDialog.getOpenFileName(self, '加载控制点', '/home')
        if ok:
            self.model.ffd.load_cp(filename)
            self.model.drawControlPoints()
        return

    def load_ffd(self):
        filename, ok = QFileDialog.getOpenFileName(self, '加载控制点', '/home')
        if ok:
            self.model.ffd.load_cp(filename)
            self.model.drawControlPoints()
        return

    def save_obj(self):
        filename, ok = QFileDialog.getOpenFileName(self, '存储obj文件', '/home')
        if ok:
            new_vertices = None #How to get new vertices?
            self.model.ffd.save_obj(filename,new_vertices)
        return

    def save_ffd(self):
        filename, ok = QFileDialog.getOpenFileName(self, '存储控制点', '/home')
        if ok:
            self.model.ffd.save_cp(filename)
        return

    # def initUI(self):
    #
    #
    #
    #     self.vtkWidget = QVTKRenderWindowInteractor()
    #
    #     vbox1 = QVBoxLayout()
    #     vbox1.addStretch(1)
    #     vbox1.addWidget(resetButton)
    #     vbox1.addWidget(colorButton)
    #     vbox1.addWidget(quitButton)
    #     vbox1.addWidget(xyzButton)
    #     vbox1.addWidget(resizeButton)
    #
    #     self.frame = QtWidgets.QFrame(self.vtkWidget)
    #     # self.frame.setGeometry(QtCore.QRect(90, 160, 321, 141))
    #     self.frame.setStyleSheet("background-color: rgb(255, 170, 0);")
    #     self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    #     self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
    #
    #     hbox = QHBoxLayout()
    #     hbox.addWidget(self.frame)
    #     hbox.addWidget(self.vtkWidget)
    #     hbox.addStretch(1)
    #     hbox.addLayout(vbox1)
    #
    #     self.setLayout(hbox)
    #     self.setGeometry(300, 300, 300, 150)
    #     self.setWindowTitle('Buttons')


    def initVTK(self):
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.model = VtkModel(ren=self.ren, iren=self.iren)

    def showAll(self):
        self.iren.Initialize()
        self.show()

    def slot_color(self):
        reply = QMessageBox.question(self, 'Message',
            "The Function Only for OBJ with RGB\n Information. Are You Sure?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.model.color()

        

    def slot_reset(self):
        self.initVTK()
        self.showAll()

    def slot_xyz(self):
        self.model.sphereQt((0,4,2), (10,10,10))

    def slot_resize(self):
        RESIZE, ok = QInputDialog.getInt(self,"RESIZE", "Input from 1 to 100（%）: ", 100, 1, 100, 5)
        if ok :
            print(RESIZE)
            RESIZE = RESIZE / 100
            self.model.resize(RESIZE)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())