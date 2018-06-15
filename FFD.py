import numpy as np
import time
class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.mtl=None
        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v=[ float(x) for x in values[1:4]]
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v=[ float(x) for x in values[1:4]]
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                v = [float(x) for x in values[1:3]]
                self.texcoords.append(v)
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = [filename,values[1]]
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))

class FFD(object):

    def __init__(self,nx,ny,nz,object_points,initial=True,cp_path=None):
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.object_points = object_points
        self.initial = initial
        tmp = object_points
        tmp.sort(key=lambda x:x[0])
        self.min_x = tmp[0][0]
        self.max_x = tmp[-1][0]
        tmp.sort(key=lambda x: x[1])
        self.min_y = tmp[0][1]
        self.max_y = tmp[-1][1]
        tmp.sort(key=lambda x: x[2])
        self.min_z = tmp[0][2]
        self.max_z = tmp[-1][2]
        self.cp_num_x = int((self.max_x - self.min_x) / self.nx) + 1
        self.cp_num_y = int((self.max_y - self.min_y) / self.ny) + 1
        self.cp_num_z = int((self.max_z - self.min_z) / self.nz) + 1
        if self.initial:
            self.control_points = [[[np.array([self.min_x+x*self.nx,self.min_y+y*self.ny,self.min_z+z*self.nz])
                                     for z in range(self.cp_num_z)]
                                    for y in range(self.cp_num_y)]
                                   for x in range(self.cp_num_x)]
        else:
            def load_cp(path):
                f = open(path,'r')
                begin = False
                while True:
                    line = f.readline()
                    if not begin:
                        if line.startswith('#'):
                            if '#dimension#' in line:
                                line = f.readline()
                                dimension = int(line.split('\n')[0])
                                continue
                            if '#offsets of the control points#' in line:
                                begin = True
                                x = 0
                                y = 0
                                continue
                            elif '#control grid size#' in line:
                                size = []
                                for i in range(dimension):
                                    line = f.readline()
                                    size.append(int(line.split('\n')[0]))
                                if dimension==3:
                                    control_points = [[[None for z in range(size[2])]
                                                       for y in range(size[1])]
                                                      for x in range(size[0])]
                                continue
                            else:
                                continue
                        else:
                            continue
                    else:
                        if line=='\n':
                            x += 1
                            y = 0
                            if x==size[0]:
                                break
                            else:
                                continue
                        else:
                            line = line.split('\t')[:-1]
                            for z in range(len(line)):
                                control_points[x][y][z] = line[z].split(' ')
                            y += 1
                return control_points
            self.control_points = load_cp(cp_path)
    def B(self,i, u):
        if i == 0:
            return (1 - u) ** 3 / 6
        elif i == 1:
            return (3 * u ** 3 - 6 * u ** 2 + 4) / 6
        elif i == 2:
            return (-3 * u ** 3 + 3 * u ** 2 + 3 * u + 1) / 6
        elif i == 3:
            return u ** 3 / 6

    def T_local(self,object_point):
        [x,y,z]= object_point
        i=int(x/self.nx)-1
        j=int(y/self.ny)-1
        k=int(z/self.nz)-1
        u=x/self.nx-i-1
        v=y/self.ny-j-1
        w=z/self.nz-k-1
        result = np.array([0., 0., 0.])
        for l in range(4):
            if 0<=i+l<self.cp_num_x:
                for m in range(4):
                    if 0<=j+m<self.cp_num_y:
                        for n in range(4):
                            if 0<=k+n<self.cp_num_z:
                                result += self.B(l,u)*self.B(m,v)*self.B(n,w)*self.control_points[i+l][j+m][k+n]
        return result

    # Change one control point, we will get the [u,v,w] of the control point.
    def update_control_point(self, changed_control_point, new_control_point):
        [u, v, w] = changed_control_point
        self.control_points[u][v][w]=new_control_point[0]
        for i in range(len(self.object_points)):
            self.object_points[i]=self.T_local(self.object_points[i])

start = time.clock()
zxh = OBJ('zxh-ape.obj')
end = time.clock()
print(end-start)
start = time.clock()
ffd = FFD(nx=10,ny=10,nz=10,object_points=zxh.vertices)
end = time.clock()
print(end-start)
start = time.clock()
ffd.update_control_point([5,5,5],np.array([260, 460, 79]))
end = time.clock()
print(end-start)