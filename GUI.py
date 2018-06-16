# from tkinter import *  
# from tkinter import messagebox # python3.0的messagebox，属于tkinter的一个组件  
  
# top = Tk()  
# top.title("button test")  
# def callback():  
#     messagebox.showinfo("Python command","人生苦短、我用Python")  
      
# Button(top, text="外观装饰边界附近的标签", width=19,bg="red",relief="raised").pack()  
  
# Button(top, text="设置按钮状态",width=21,state="disable").pack()  
  
# Button(top, text="设置bitmap放到按钮左边位置", compound="left",bitmap="error").pack()  
  
# Button(top, text="设置command事件调用命令", fg="blue",bd=2,width=28,command=callback).pack()  
  
# Button(top, text ="设置高度宽度以及文字显示位置",anchor = 'sw',width = 30,height = 2).pack()  
  
  
      
# top.mainloop()  

#!/usr/bin/env python

from tkinter import *  
from tkinter import messagebox # python3.0的messagebox，属于tkinter的一个组件  
import vtk
from vtk.tk.vtkTkRenderWindowInteractor import vtkTkRenderWindowInteractor

# Setup for root window
root = Tk()
root.title( "Tkinter Test" )
frame = Frame( root )
frame.pack( fill=BOTH, expand=1, side=TOP )

# def callback():
#     messagebox.showinfo("Python command","人生苦短、我用Python")
#
# Button(root, text="设置command事件调用命令", fg="blue",bd=2,width=28,command=callback).pack()

# Setup for renderer
render = vtk.vtkRenderer()
render.SetBackground(0.329412, 0.34902, 0.427451)
render.ResetCameraClippingRange()
 
# Setup for rendering window
renWindow = vtk.vtkRenderWindow()
renWindow.AddRenderer(render)

# Setup for rendering window interactor       
renWinInteract = vtkTkRenderWindowInteractor(root, rw=renWindow, width=400, height=400)
renWinInteract.Initialize()
renWinInteract.pack(side='top', fill='both', expand=1)
renWinInteract.Start()
 
# Begin execution by updating the renderer and
# starting the Tkinter loop
renWindow.Render()
root.mainloop()