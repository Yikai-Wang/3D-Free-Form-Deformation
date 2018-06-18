import vtk

def resize_poly_data(data, resize):
    " resize the poly data"
    pDecimate = vtk.vtkDecimatePro()
    pDecimate.SetInputData(data)
    pDecimate.SetTargetReduction(1-resize)
    pDecimate.PreserveTopologyOff()
    pDecimate.SplittingOn()
    pDecimate.BoundaryVertexDeletionOn()
    pDecimate.SetMaximumError(vtk.VTK_DOUBLE_MAX)
    pDecimate.Update()
    return pDecimate.GetOutput()
    
def read_color_from_ffd(filename):
    colors = []
    with open(filename, "r") as f:
        for lines in f:
            values = lines.strip().split(" ")
            if values[0] == "v" and len(values) == 7:
                colors.append((int(float(values[4])*255), int(float(values[5])*255), int(float(values[6])*255)))
            else:
                continue
    return colors

def color_on_points(data, colors=[]):
    " put color on points"
    Colors = vtk.vtkUnsignedCharArray()
    Colors.SetNumberOfComponents(3)
    Colors.SetName("Colors")
    for r,g,b in colors:
        Colors.InsertNextTuple3(r, g, b)
    data.GetPointData().SetScalars(Colors)

    return data