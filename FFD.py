import numpy as np

class control_point_class(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setZ(self, z):
        self.z = z

class object_point(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.t = 0
        self.u = 0
        self.v = 0

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getT(self):
        return self.t

    def getU(self):
        return self.u

    def getV(self):
        return self.v

    def setT(self, t):
        self.t = t

    def setU(self, u):
        self.u = u

    def setV(self, v):
        self.v = v

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setZ(self, z):
        self.z = z

def computeTUVData(object_points_array,control_point_min_x,control_point_max_x,control_point_min_y,control_point_max_y,
                   control_point_min_z,control_point_max_z):
    for point in object_points_array:
        t = int((point.getX() - control_point_min_x)/(control_point_max_x - control_point_min_x))
        u = int((point.getY() - control_point_min_y)/(control_point_max_y-control_point_min_y))
        v = int((point.getZ() - control_point_min_z)/(control_point_max_z-control_point_min_z))
        point.setT(t)
        point.setU(u)
        point.setV(v)
    return

def B(i,u):
    if i==0:
        return (1-u)**3/6
    elif i==1:
        return (3*u**3-6*u**2+4)/6
    elif i==2:
        return (-3*u**3+3*u**2+3*u+1)/6
    elif i==3:
        return u**3/6

def T_local(x,y,z):
    result = [0,0,0]
    i = int((x-object_point_min_x)/CONTROL_POINT_NUMBER_X)-1
    j = int((y - object_point_min_y) / CONTROL_POINT_NUMBER_Y) - 1
    k = int((z - object_point_min_z) / CONTROL_POINT_NUMBER_Z) - 1
    u = (x-object_point_min_x)/CONTROL_POINT_NUMBER_X-int((x-object_point_min_x)/CONTROL_POINT_NUMBER_X)
    v = (y - object_point_min_y) / CONTROL_POINT_NUMBER_Y - int((y - object_point_min_y) / CONTROL_POINT_NUMBER_Y)
    w = (z - object_point_min_z) / CONTROL_POINT_NUMBER_Z - int((z - object_point_min_z) / CONTROL_POINT_NUMBER_Z)
    for l in range(4):
        for m in range(4):
            for n in range(4):
                tmp = B(l,u)*B(m,v)*B(n,w)
                result[0] += tmp*control_points_list[i+l][j+m][k+n].getX()
                result[1] += tmp * control_points_list[i + l][j + m][k + n].getY()
                result[2] += tmp * control_points_list[i + l][j + m][k + n].getZ()
    return result

SPACING_DELTA = 10
CONTROL_POINT_NUMBER_X= 20
CONTROL_POINT_NUMBER_Y= 30
CONTROL_POINT_NUMBER_Z= 40
OBJECT = np.random.randint(0,100,size=[60,60,60])
object_point_min_x = 1
object_point_max_x = 2
object_point_min_y = 1
object_point_max_y = 2
object_point_min_z = 1
object_point_max_z = 2
control_point_min_x = 1
control_point_max_x = 2
control_point_min_y = 1
control_point_max_y = 2
control_point_min_z = 1
control_point_max_z = 2
control_points_list = [None]*CONTROL_POINT_NUMBER_X
for x in range(CONTROL_POINT_NUMBER_X):
    control_points_list[x] = [None]*CONTROL_POINT_NUMBER_Y
for x in range(CONTROL_POINT_NUMBER_X):
    for y in range(CONTROL_POINT_NUMBER_Y):
        control_points_list[x][y] = [None]*CONTROL_POINT_NUMBER_Z
for x in range(CONTROL_POINT_NUMBER_X):
    for y in range(CONTROL_POINT_NUMBER_Y):
        for z in range(CONTROL_POINT_NUMBER_Z):
            control_points_list[x][y][z] = control_point_class(x=int(x*control_point_max_x+(CONTROL_POINT_NUMBER_X-1-x)*control_point_min_x)/(CONTROL_POINT_NUMBER_X-1),
                                                               y=int(y*control_point_max_y+(CONTROL_POINT_NUMBER_Y-1-y)*control_point_min_y)/(CONTROL_POINT_NUMBER_Y-1),
                                                               z=int(z*control_point_max_z+(CONTROL_POINT_NUMBER_Z-1-z)*control_point_min_z)/(CONTROL_POINT_NUMBER_Z-1))




















# def NewtonSolve(N, initialGuess , systemOfFunctions):
#
#     counter = 0
#     X0 = initialGuess
#     while(True):
#         Jacobian = calculateJacobian(N,systemOfFunctions, X0)
#
#         #create the system of equations to solve. DF(X0) * DeltaX = - F(X0). From this,
#         #DeltaX can be solved for. DF(X0) is the Jacobian variable from the line before.
#             #Now, create the vector F(X0)
#         size = (N,1)
#         MinusFX0 = numpy.zeros(size)
#
#         for i in range(N):
#             MinusFX0[i] = -systemOfFunctions[i](X0)
#
#         deltaXVector = numpy.linalg.solve(Jacobian, MinusFX0)
#
#         #deltaXVector = X1 - X0. Calculate X1 and use it for the next iteration
#         #deltaXVector + X0 = X1
#         for i in range(N):
#             X0[i] = deltaXVector[i][0] + X0[i]
#
#         counter+=1
#         #to make sure an infinite loop isnt entered
#         if(counter>100):
#             break
#
#         #if the delta x vector's norm is sufficiently small then quit the loop:
#         norm = 0
#         for i in range(N):
#             norm += deltaXVector[i]**2
#
#         norm = norm**(1./float(N))
#         if(norm < CONST_Tolerance):
#             break
#
#     #returning the solution vector
#     return X0
#
#
# #Each function has to take a vector as input. the vector is the vector of variables X
# #X0 is the vector about which the jacobian is calculated
# def calculateJacobian(N,systemOfFunctions, X0):
#
#     #create an N*N matrix of zeros for the jacobian
#     size = (N,N)
#     Jacobian = numpy.zeros(size)
#
#     for r in range(N):
#         for c in range(N):
#             #r is the row of interest and c is the column of interest. The loop will go through one row at a time
#
#             #the column value will dictate which element in the X vector to perturb. Perturb this x position at the
#             #beginning of the loop and then remove the perturbation after calculate an approximation of the partial
#             delfrBydelXcAtX0 = -systemOfFunctions[r](X0)/CONST_dx
#             X0[c] = X0[c] + CONST_dx
#             delfrBydelXcAtX0 += systemOfFunctions[r](X0)/CONST_dx
#
#             Jacobian[r][c] = delfrBydelXcAtX0
#             X0[c] = X0[c] - CONST_dx
#
#     return Jacobian
#
#
#
#




# class zCrossSectionData(object):
#
#     def __init__(self, xValue, yValue, zValue):
#         self.z = zValue
#         self.xMax = xValue
#         self.xMin = xValue
#         self.yMax = yValue
#         self.yMin = yValue
#
#     #The getters
#     def getXMax(self):
#         return self.xMax
#
#     def getXMin(self):
#         return self.xMin
#
#     def getYMax(self):
#         return self.yMax
#
#     def getYMin(self):
#         return self.yMin
#
#     #The setters
#     def setXMax(self, xMax):
#         self.xMax = xMax
#
#     def setXMin(self, xMin):
#         self.xMin = xMin
#
#     def setYMax(self, yMax):
#         self.yMax = yMax
#
#     def setYMin(self, yMin):
#         self.yMin = yMin

# def createFFDMesh(FFDPointArray):
#     FFDdx = (CONST_FFDXMax-CONST_FFDXMin)/(CONST_nXFDD-1)
#     FFDdy = (CONST_FFDYMax - CONST_FFDYMin) / (CONST_nYFDD - 1)
#     FFDdz = (CONST_FFDZMax - CONST_FFDZMin) / (CONST_nZFDD - 1)
#
#     for i in range(CONST_nXFDD):
#         for j in range(CONST_nYFDD):
#             for k in range(CONST_nZFDD):
#                 #print "CREATE i,j,k: " + str(i) + " " + str(j) + " " + str(k)
#
#                 FFDelement = FFDPointElement.FFDPointElement(CONST_FFDXMin+ FFDdx*i, CONST_FFDYMin+ FFDdy*j, CONST_FFDZMin + FFDdz*k)
#                 FFDPointArray[i][j][k] = FFDelement
#
#                 #print str(FFDelement.getX()) + ", " + str(FFDelement.getY()) + ", " + str(FFDelement.getZ())


#reads the points from the solid boundary point file and also creates a rectangular mesh
# def initializeData(x,y,z, solidBoundaryPointArray):
#     solidBoundaryPointSize, XMax, XMin, YMax, YMin, ZMax, ZMin = readData(x, y, z)
#
#     #print "solidBoundaryPointSize: " + str(solidBoundaryPointSize)
#     #print "FFDPointsSize: " + str(FFDPointsSize)
#
#     #create a solidBoundaryPoint element for each point
#     for i in range(solidBoundaryPointSize):
#         bndelement = solidBoundaryPoint.solidBoundaryPoint(x[i],y[i],z[i])
#         solidBoundaryPointArray.append(bndelement)
#
#     return (XMax, XMin, YMax, YMin, ZMax, ZMin)


# def isIncludedZCrossSection(z):
#
#     #iterate through all the keys for the zCrossSections dictionary.
#     #Then, divide each key by the given z value and if the resulting
#     #number is within some epsilon of 1, then we'll say that the number
#     #is included in the dictionary
#
#     for key in GLOBAL_zCrossSectionObjects.keys():
#         if(key==0 and z ==0):
#             return key
#         else:
#             num = key/z
#             if(num<1.05 and num >0.95):
#                 return key
#
#     return None









# def AttachFFDNewton(SolidBoundaryPointArray):
#     for i in range(len(solidBoundaryPointArray)):
#         print("Attach FFD i: " + str(i))
#         element = SolidBoundaryPointArray[i]
#
#         xElem = element.getX()
#         yElem = element.getY()
#         zElem = element.getZ()
#
#         #capture the xElem, yElem and zElem values (these change in the loop so capture these
#         #values for what they are when the lambda function is created)
#         testFunction_1 = (lambda X, xElem = xElem: xElem - Gamma(X)[0])
#         testFunction_2 = (lambda X, yElem = yElem: yElem - Gamma(X)[1])
#         testFunction_3 = (lambda X, zElem = zElem: zElem - Gamma(X)[2])
#
#         testFunctionArray = [testFunction_1, testFunction_2, testFunction_3]
#         AnswerArray = NewtonSolver.NewtonSolve(3, [0.5, 0.5, 0.5], testFunctionArray)
#         element.setT(AnswerArray[0])
#         element.setU(AnswerArray[1])
#         element.setV(AnswerArray[2])


# def createFFDPointsFixedCrossSections(FFDPointArray, zvalue, k):
#     zCrossSectionObject = GLOBAL_zCrossSectionObjects[zvalue]
#     xMax = zCrossSectionObject.getXMax()
#     xMin = zCrossSectionObject.getXMin()
#     yMax = zCrossSectionObject.getYMax()
#     yMin = zCrossSectionObject.getYMin()
#
#     FFDdx = (xMax + 2*CONST_xEpsilon- xMin) / (CONST_nXFDD - 1)
#     FFDdy = (yMax + 2*CONST_yEpsilon - yMin) / (CONST_nYFDD - 1)
#
#     for i in range(CONST_nXFDD):
#         for j in range(CONST_nYFDD):
#             # print "CREATE i,j,k: " + str(i) + " " + str(j) + " " + str(k)
#
#             FFDelement = FFDPointElement.FFDPointElement(xMin - CONST_xEpsilon + FFDdx * i, yMin - CONST_yEpsilon + FFDdy * j,
#                                                          zvalue)
#             FFDPointArray[i][j][k] = FFDelement

            # print str(FFDelement.getX()) + ", " + str(FFDelement.getY()) + ", " + str(FFDelement.getZ())


#The method used to attach the FFD points onto the CRM wing.
# def createFFDMeshCRM(FFDPointArray, solidBoundaryPointArray, solidXMax, solidXMin, solidYMax, solidYMin, solidZMax, solidZMin):
#
#     #sort the keys in the z cross section dictionary
#     zCrossSectionList = GLOBAL_zCrossSectionObjects.keys()
#     zCrossSectionList.sort()
#
#     print(zCrossSectionList)
#
#     dz = (zCrossSectionList[len(zCrossSectionList)-1] - zCrossSectionList[0])/(CONST_nZFDD-1)
#
#     numCrossSections = len(zCrossSectionList)-1
#
#     print("length: " + str(len(zCrossSectionList)))
#
#     # points will be put at index =0 and index = numCrossSections-1
#     # That leaves CONST_nZFDD-2 cross sections left to put.
#
#     #The index seperation between cross sections with FFD points
#     dCrossSections = float(numCrossSections)/float((CONST_nZFDD-1))
#
#     print("d cross: " + str(dCrossSections))
#
#     tolerance = 0.1
#     for k in range(CONST_nZFDD):
#         print("z section exact: " + str(zCrossSectionList[0] + k * dz))
#         zCrossSectionSearch = 0
#         #The z cross section to search for in the dictionary
#         for key in zCrossSectionList:
#             if (key == 0 and (zCrossSectionList[0] + k * dz) == 0):
#                 zCrossSectionSearch = key
#                 break
#             else:
#                 num = key / (zCrossSectionList[0] + k * dz)
#                 print("     num: " + str(num))
#                 if (num < (1 + tolerance) and num > (1-tolerance)):
#                     zCrossSectionSearch = key
#                     break
#
#         if(k==CONST_nZFDD-1):
#             zCrossSectionSearch = zCrossSectionList[len(zCrossSectionList)-1]
#
#         print("z cross section search: " + str(zCrossSectionSearch))
#
#         #index = int(k*dCrossSections)
#         #print "index: " + str(index)
#
#         createFFDPointsFixedCrossSections(FFDPointArray, zCrossSectionSearch, k)


# Printing to the file. The data will be written to the file in the following format
    # FFD Point
        # I,J,K
        # X,Y,Z
    # Solid Boundary Point
        # X,Y,Z
        # T,U,V

# def preprocessingCRM(xsolid,ysolid,zsolid, solidBoundaryPointArray, FFDPointArray):
#     solidXMax, solidXMin, solidYMax, solidYMin, solidZMax, \
#     solidZMin = initializeData(xsolid, ysolid, zsolid, solidBoundaryPointArray)
#
#     createFFDMeshCRM(FFDPointArray, solidBoundaryPointArray, solidXMax, solidXMin, solidYMax, solidYMin, solidZMax, solidZMin)
#
#     #AttachFFDNewton(solidBoundaryPointArray)
#
#     f = open(CONST_DATAFILE, "w")
#     # first write out the FFD Points
#     f.write("FFD Points: X, Y, Z" + "\n")
#
#     for i in range(CONST_nXFDD):
#         for j in range(CONST_nYFDD):
#             for k in range(CONST_nZFDD):
#                 FFDElement = FFDPointArray[i][j][k]
#                 f.write(str(i) + ", " + str(j) + ", " + str(k) + "\n")
#                 f.write(str(FFDElement.getX()) + ", " + str(FFDElement.getY()) + ", " + str(FFDElement.getZ()) + "\n")
#
#     f.write("Solid Boundary Point Data" + "\n")
#     for i in range(len(solidBoundaryPointArray)):
#         element = solidBoundaryPointArray[i]
#         f.write(str(element.getX()) + ", " + str(element.getY()) + ", " + str(element.getZ()) + "\n")
#         f.write(str(element.getT()) + ", " + str(element.getU()) + ", " + str(element.getV()) + "\n")
#
#     f.close()


# def preprocessing(xsolid,ysolid,zsolid, solidBoundaryPointArray, FFDPointArray):
#     solidXMax, solidXMin, solidYMax, solidYMin, solidZMax, \
#     solidZMin = initializeData(xsolid, ysolid, zsolid, solidBoundaryPointArray)
#
#     createFFDMesh(FFDPointArray)
#     AttachFFDNewton(solidBoundaryPointArray)
#
#     # Printing to the file. The data will be written to the file in the following format
#     # FFD Point
#         # I,J,K
#         # X,Y,Z
#     #Solid Boundary Point
#         #X,Y,Z
#         #T,U,V
#
#     f = open(CONST_DATAFILE, "w")
#     # first write out the FFD Points
#     f.write("FFD Points: X, Y, Z" + "\n")
#
#     for i in range(CONST_nXFDD):
#         for j in range(CONST_nYFDD):
#             for k in range(CONST_nZFDD):
#                 FFDElement = FFDPointArray[i][j][k]
#                 f.write(str(i) + ", " + str(j) + ", " + str(k) + "\n")
#                 f.write(str(FFDElement.getX()) + ", " + str(FFDElement.getY()) + ", " + str(FFDElement.getZ()) + "\n")
#
#     f.write("Solid Boundary Point Data" + "\n")
#     for i in range(len(solidBoundaryPointArray)):
#         element = solidBoundaryPointArray[i]
#         f.write(str(element.getX()) + ", " + str(element.getY()) + ", " + str(element.getZ()) + "\n")
#         f.write(str(element.getT()) + ", " + str(element.getU()) + ", " + str(element.getV()) + "\n")
#
#     f.close()

#For reading the data into the data structures from the file
# def initializeDataFromFile(solidBoundaryPointArray, FFDPointArray):
#     fileData = open(CONST_DATAFILE, "r")
#
#     # first read the FFD point data
#     lineFFD = fileData.readline()
#     while(True):
#
#         #read the IJK data line
#         lineIJK = fileData.readline()
#
#         #if all the FFD point data has been read already
#         if(lineIJK == "Solid Boundary Point Data\n"):
#             break
#
#             #otherwise, there are now two lines of FFD data to read. Read the second line too
#         lineXYZ = fileData.readline()
#
#         #parse the IJK data line
#         I = 0
#         J = 0
#         K = 0
#         for i in range(3):
#             Comma = lineIJK.find(",")
#             if (Comma == -1):
#                 # on last number
#                 Num = lineIJK[0: len(lineIJK)]
#                 K = int(Num)
#                 break
#
#             Num = lineIJK[0:Comma]
#             lineIJK = lineIJK[Comma + 1:len(lineIJK)]
#
#             if (i == 0):
#                 I = int(Num)
#             elif (i == 1):
#                 J = int(Num)
#
#         #parse the XYZ line
#         X = 0.0
#         Y = 0.0
#         Z = 0.0
#         for i in range(3):
#             Comma = lineXYZ.find(",")
#             if (Comma == -1):
#                 # on last number
#                 Num = lineXYZ[0: len(lineXYZ)]
#                 Z = float(Num)
#                 break
#
#             Num = lineXYZ[0:Comma]
#             lineXYZ = lineXYZ[Comma + 1:len(lineXYZ)]
#
#             if (i == 0):
#                 X = float(Num)
#             elif (i == 1):
#                 Y = float(Num)
#
#         #create an FFD point element and store the data in the object. place the object in the FFD Point list
#         FFDElement = FFDPointElement.FFDPointElement(X,Y,Z)
#         FFDPointArray[I][J][K] = FFDElement
#
#
#     #Now read the solid boundary point data
#     while(True):
#         lineXYZSolid = fileData.readline()
#         #the end of the solid boundary point data, and the file, has been reached
#         if(lineXYZSolid == ""):
#             break
#
#         #Loop didn't break so there is more data to read
#             #read the T,U,V line
#         lineTUVSolid = fileData.readline()
#
#         # parse the XYZ line
#         Xsolid = 0.0
#         Ysolid = 0.0
#         Zsolid = 0.0
#         for i in range(3):
#             Comma = lineXYZSolid.find(",")
#             if (Comma == -1):
#                 # on last number
#                 Num = lineXYZSolid[0: len(lineXYZSolid)]
#                 Zsolid = float(Num)
#                 break
#
#             Num = lineXYZSolid[0:Comma]
#             lineXYZSolid = lineXYZSolid[Comma + 1:len(lineXYZSolid)]
#
#             if (i == 0):
#                 Xsolid = float(Num)
#             elif (i == 1):
#                 Ysolid = float(Num)
#
#         #parse the TUV line
#         T = 0.0
#         U = 0.0
#         V = 0.0
#         for i in range(3):
#             Comma = lineTUVSolid.find(",")
#             if (Comma == -1):
#                 # on last number
#                 Num = lineTUVSolid[0: len(lineTUVSolid)]
#                 V = float(Num)
#                 break
#
#             Num = lineTUVSolid[0:Comma]
#             lineTUVSolid = lineTUVSolid[Comma + 1:len(lineTUVSolid)]
#
#             if (i == 0):
#                 T = float(Num)
#             elif (i == 1):
#                 U = float(Num)
#
#         #create the solidBoundaryPoint element and store the data into the object. Then add the object to the
#         # solidBoundaryPoint array
#         solidBndElement = solidBoundaryPoint.solidBoundaryPoint(Xsolid,Ysolid,Zsolid)
#         solidBndElement.setT(T)
#         solidBndElement.setU(U)
#         solidBndElement.setV(V)
#
#         solidBoundaryPointArray.append(solidBndElement)
#
#     fileData.close()

# def fillInitialArrays(solidBoundaryPointArray, FFDPointArray, xsolidInitial,
#                       ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial):
#     # filling the object's solid point arrays
#     for element in solidBoundaryPointArray:
#         xsolidInitial.append(element.getX())
#         ysolidInitial.append(element.getY())
#         zsolidInitial.append(element.getZ())
#
#     # filling the FFD arrays
#     for i in range(CONST_nXFDD):
#         for j in range(CONST_nYFDD):
#             for k in range(CONST_nZFDD):
#                 element = FFDPointArray[i][j][k]
#                 xFFDInitial.append(element.getX())
#                 yFFDInitial.append(element.getY())
#                 zFFDInitial.append(element.getZ())
#
# #deform the FFD points arbitrarily
# def deformFFDPoints(FFDPointArray):
#     for i in range(CONST_nXFDD):
#         for j in range(CONST_nYFDD):
#             for k in range(CONST_nZFDD):
#                 #shift on row of ffd points by 0.3 in the y direction
#                 if(k==CONST_nZFDD-1):
#                     element = FFDPointArray[i][j][k]
#                     newYValue = element.getY()+0.3
#                     element.setY(newYValue)




# def modifyShape(solidBoundaryPointArray, FFDPointArray):
#
#     #compute the new coordinates of all the solid boundary points using the FFD points
#
#     # do a sum from i=0 to n, where n is the number of spaces between FFD points (so if there are n xFFD points then
#     # there are n-1 spaces).
#     n = CONST_nXFDD - 1
#     m = CONST_nYFDD - 1
#     l = CONST_nZFDD - 1
#
#     for solidElement in solidBoundaryPointArray:
#
#         xNew = 0
#         yNew = 0
#         zNew = 0
#
#         t = solidElement.getT()
#         u = solidElement.getU()
#         v = solidElement.getV()
#
#         for i in range(CONST_nXFDD):
#             for j in range(CONST_nYFDD):
#                 for k in range(CONST_nZFDD):
#                     xNew = xNew + B(i, n, t) * B(j, m, u) * B(k, l, v) * FFDPointArray[i][j][k].getX()
#                     yNew = yNew + B(i, n, t) * B(j, m, u) * B(k, l, v) * FFDPointArray[i][j][k].getY()
#                     zNew = zNew + B(i, n, t) * B(j, m, u) * B(k, l, v) * FFDPointArray[i][j][k].getZ()
#
#         solidElement.setX(xNew)
#         solidElement.setY(yNew)
#         solidElement.setZ(zNew)


# def FFDSolve():
#     # read the data from the file and fill the data structures
#     initializeDataFromFile(solidBoundaryPointArray, FFDPointArray)
#     solidBoundaryPointArray.sort(key=lambda x: x.getZ(), reverse=True)
#     fillInitialArrays(solidBoundaryPointArray, FFDPointArray, xsolidInitial,
#                       ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial)
#
#     # printFFDAndSolidBndData(FFDPointArray, solidBoundaryPointArray)
#
#     deformFFDPoints(FFDPointArray)
#     modifyShape(solidBoundaryPointArray, FFDPointArray)
#
#     plotFFDandSolidBNDAndInitialFFDandSolidBND(FFDPointArray, solidBoundaryPointArray, xsolidInitial,
#                                                ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial)
#

#Main Method

#The lists that will hold the solid boundary point and FFD point objects
# solidBoundaryPointArray = []
# FFDPointArray = []
# for i in range(CONST_nXFDD):
#     rowj = []
#     for j in range(CONST_nYFDD):
#         rowk = []
#         for k in range(CONST_nZFDD):
#             rowk.append(FFDPointElement.FFDPointElement(0,0,0))
#         rowj.append(rowk)
#     FFDPointArray.append(rowj)
#
#
# #create arrays that will hold the initial object's solid points and the initial FFD points
# # For the initial solid boundary points
# xsolidInitial = []
# ysolidInitial = []
# zsolidInitial = []
#
# # For the initial FFD Points
# xFFDInitial = []
# yFFDInitial = []
# zFFDInitial = []


#The preprocessor. Needs to only be run once to initialize all the data and write it
#into the file.


#preprocessing(xsolidInitial,ysolidInitial,zsolidInitial, solidBoundaryPointArray, FFDPointArray)

#preprocessingCRM(xsolidInitial,ysolidInitial,zsolidInitial, solidBoundaryPointArray, FFDPointArray)


# filling the FFD arrays
# for i in range(CONST_nXFDD):
#     for j in range(CONST_nYFDD):
#         for k in range(CONST_nZFDD):
#             element = FFDPointArray[i][j][k]
#             xFFDInitial.append(element.getX())
#             yFFDInitial.append(element.getY())
#             zFFDInitial.append(element.getZ())
#
# #plotFiguresTemp(xsolidInitial, ysolidInitial, zsolidInitial, xFFDInitial, yFFDInitial, zFFDInitial)
#
# for element in solidBoundaryPointArray:
#     if(element.getT()>1 or element.getU()>1 or element.getV()>1):
#         print("T, U, V: " + str(element.getT()) + "  " + str(element.getU()) + "  " + str(element.getV()))
#         print("x, y ,z: " + str(element.getX()) + "  " + str(element.getY()) + "  " + str(element.getZ()))
#
# FFDSolve()