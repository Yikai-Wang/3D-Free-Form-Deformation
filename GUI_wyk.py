#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QSettings, QSize,
        Qt, QTextStream)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
        QMessageBox, QTextEdit)

class MainWindow(QMainWindow):
	"""docstring for MainWindow"""
	def __init__(self):
		super(MainWindow, self).__init__()
		self.createActions()
		self.createMenus()

	def createActions(self):
		self.load_obj_Action = QAction('加载obj文件',self,triggered=self.load_obj)
		self.load_image_Action = QAction('加载照片',self,triggered=self.load_image)
		self.load_ffd_Action = QAction('加载控制点',self,triggered=self.load_ffd)
		self.save_obj_Action = QAction('存储obj文件',self,triggered=self.save_obj)
		self.save_ffd_Action = QAction('存储控制点',self,triggered=self.save_ffd)

	def createMenus(self):
		self.menuBar().setNativeMenuBar(False)
		self.loadMenu = self.menuBar().addMenu('Load')
		self.saveMenu = self.menuBar().addMenu('Save')
		self.loadMenu.addAction(self.load_obj_Action)
		self.loadMenu.addAction(self.load_image_Action)
		self.loadMenu.addAction(self.load_ffd_Action)
		self.saveMenu.addAction(self.save_obj_Action)
		self.saveMenu.addAction(self.save_ffd_Action)

	def load_obj(self):
		return
	def load_image(self):
		return
	def load_ffd(self):
		return
	def save_obj(self):
		return
	def save_ffd(self):
		return

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
		