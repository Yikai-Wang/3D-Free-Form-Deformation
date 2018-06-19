import sys
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QInputDialog, QMessageBox)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from VtkModel import VtkModel
import vtk
import gc


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.initVTK()
        self.showAll()

    def initUI(self):

        resetButton = QPushButton("RESET")
        colorButton = QPushButton("COLOR")
        quitButton = QPushButton("QUIT")
        xyzButton = QPushButton("SET XYZ")
        resizeButton = QPushButton("RESIZE")

        quitButton.clicked.connect(QApplication.instance().quit)
        colorButton.clicked.connect(self.slot_color)
        resetButton.clicked.connect(self.slot_reset)
        xyzButton.clicked.connect(self.slot_xyz)
        resizeButton.clicked.connect(self.slot_resize)


        self.vtkWidget = QVTKRenderWindowInteractor()

        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addWidget(resetButton)
        vbox1.addWidget(colorButton)
        vbox1.addWidget(quitButton)
        vbox1.addWidget(xyzButton)
        vbox1.addWidget(resizeButton)

        self.frame = QtWidgets.QFrame(self.vtkWidget)  
        # self.frame.setGeometry(QtCore.QRect(90, 160, 321, 141))  
        self.frame.setStyleSheet("background-color: rgb(255, 170, 0);")  
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)  
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)  

        hbox = QHBoxLayout()
        hbox.addWidget(self.frame)
        hbox.addWidget(self.vtkWidget)
        hbox.addStretch(1)
        hbox.addLayout(vbox1)

        self.setLayout(hbox)    
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    


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