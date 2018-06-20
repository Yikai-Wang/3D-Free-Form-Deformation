import sys
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton,QHBoxLayout, QVBoxLayout, QApplication, QInputDialog, QMessageBox, QMainWindow,QAction,QFileDialog)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from VtkModel import VtkModel
import vtk
import gc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 700)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.gridlayout = QtWidgets.QGridLayout(self.centralWidget)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        MainWindow.setCentralWidget(self.vtkWidget)


class SimpleView(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.createActions()
        self.createMenus()
        #self.initUI()
        self.initVTK()
        self.showAll()

    def initVTK(self, filename="zxh-ape.obj"):
        self.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()

        self.model = VtkModel(ren=self.ren, iren=self.iren, filename=filename)

    def showAll(self):
        self.iren.Initialize()
        self.show()

    def createActions(self):
        self.load_obj_Action = QAction('Load .OBJ', self, triggered=self.load_obj)
        self.load_image_Action = QAction('Load .PNG', self, triggered=self.load_image)
        self.load_ffd_Action = QAction('Load .FFD', self, triggered=self.load_ffd)
        self.save_obj_Action = QAction('Save .OBJ', self, triggered=self.save_obj)
        self.save_ffd_Action = QAction('Save .FFD', self, triggered=self.save_ffd)
        self.reset_Action = QAction('Reset', self, triggered=self.slot_reset)
        self.color_Action = QAction('Color', self, triggered=self.slot_color)
        self.quit_Action = QAction('Quit', self, triggered=QApplication.instance().quit)
        self.xyz_Action = QAction('Set XYZ', self, triggered=self.slot_xyz)
        self.resize_Action = QAction('Resize', self, triggered=self.slot_resize)

    def createMenus(self):
        self.menuBar().setNativeMenuBar(False)
        self.loadMenu = self.menuBar().addMenu('Load')
        self.saveMenu = self.menuBar().addMenu('Save')
        self.modifyMenu = self.menuBar().addMenu('Modify')
        self.resetMenu = self.menuBar().addMenu('Reset')
        self.loadMenu.addAction(self.load_obj_Action)
        self.loadMenu.addAction(self.load_image_Action)
        self.loadMenu.addAction(self.load_ffd_Action)
        self.saveMenu.addAction(self.save_obj_Action)
        self.saveMenu.addAction(self.save_ffd_Action)
        self.resetMenu.addAction(self.reset_Action)
        self.resetMenu.addAction(self.quit_Action)
        self.modifyMenu.addAction(self.color_Action)
        self.modifyMenu.addAction(self.xyz_Action)
        self.modifyMenu.addAction(self.resize_Action)

    def load_obj(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'Load .OBJ', '')
        if ok:
            self.initVTK(filename)
            self.showAll()
        # return

    def load_image(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'Load .PNG', '')
        if ok:
            self.model.ffd.load_cp(filename)
            self.model.drawControlPoints()
        return

    def load_ffd(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'Load .FFD', '')
        if ok:
            self.model.ffd.load_cp(filename)
            self.model.drawControlPoints()
        return

    def save_obj(self):
        filename, ok = QFileDialog.getSaveFileName(self, 'Save .OBJ', '')
        if ok:
            new_vertices = None #How to get new vertices?
            self.model.ffd.save_obj(filename,new_vertices)
        return

    def save_ffd(self):
        filename, ok = QFileDialog.getSaveFileName(self, 'Save .FFD', '')
        if ok:
            self.model.ffd.save_cp(filename)
        return

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleView()
    window.show()
    window.iren.Initialize()  # Need this line to actually show the render inside Qt
    sys.exit(app.exec_())