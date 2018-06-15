# coding:utf-8
import vtk
from copy import copy
from os import remove as osRemove

polygonPolyData = vtk.vtkConeSource()
polygonPolyData.Update()
polygonPolyData = polygonPolyData.GetOutput()


def FFD(polygonPolyData):
    # 按照id顺序获取polydata的vertex坐标
    coord = []
    position = [0.0, 0.0, 0.0]
    for i in range(polygonPolyData.GetNumberOfPoints()):
        polygonPolyData.GetPoint(i, position)
        t = copy(position)
        coord.append(t)

    # 按照cell的id顺序获取构成cell的vertex的id
    cell_ids = []
    for i in range(polygonPolyData.GetNumberOfCells()):
        cell = polygonPolyData.GetCell(i)
        nPoints = cell.GetNumberOfPoints()
        vertex_ids = []
        for j in range(nPoints):
            vertex_ids.append(cell.GetPointId(j))
        cell_ids.append(vertex_ids)

    # vertex坐标变换


    # 重构polydata
    points = vtk.vtkPoints()
    for i in range(len(coord)):
        points.InsertNextPoint(coord[i])

    cells = vtk.vtkCellArray()

    for vertex_ids in cell_ids:
        polygon = vtk.vtkPolygon()
        cell_num = len(vertex_ids)
        polygon.GetPointIds().SetNumberOfIds(cell_num)
        id0 = 0
        for i in vertex_ids:
            polygon.GetPointIds().SetId(id0, i)
            id0 += 1
        cells.InsertNextCell(polygon)

    polygonPolyData = vtk.vtkPolyData()
    polygonPolyData.SetPoints(points)
    polygonPolyData.SetPolys(cells)
    return polygonPolyData

# FFD变换
polygonPolyData = FFD(polygonPolyData)

Mapper = vtk.vtkPolyDataMapper()
Mapper.SetInputData(polygonPolyData)

Actor = vtk.vtkActor()
Actor.SetMapper(Mapper)

Ren1 = vtk.vtkRenderer()
Ren1.AddActor(Actor)


renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(Ren1)

# save the obj data
dir0 = "C:\Users\hxu13\Desktop\pp\ExportData"
porter = vtk.vtkOBJExporter()
porter.SetFilePrefix(dir0+"\cells")
porter.SetInput(renWin)
porter.Write()
osRemove(dir0 + '\cells.mtl')

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()
