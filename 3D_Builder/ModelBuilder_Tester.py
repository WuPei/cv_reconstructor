from ModelBuilder import ModelBuilder
from Vertex import Vertex as vt
from shape import Shape
from shape import Cylinder
from shape import Cuboid
from shape import Prism
from shape import Frustum
from shape import Ground
from shape import Sky
from shape import Face
from shape import Tree

print "ModelBuilder Tester"
mb = ModelBuilder()

'''print "Test BuildCuboid"
center = vt(0,0,0)
length = 10
width = 10
height = 10
face_front = Face([[1, 5],[5, 5],[5, 9],[1, 9]], "Front")
shape1 = Cuboid(center, length, width, height, "Shape1")
shape1.faces.append(face_front)
results = mb.BuildModel(shape1)'''

'''print "Test Build Plane: Sky"
sky = Sky([[1, 5],[5, 5],[5, 9],[1, 9]], "sky")
results = mb.BuildModel(sky)'''

'''print "Test Build Plane: Ground"
ground = Ground([[1, 5],[5, 5],[5, 9],[1, 9]], "sky")
results = mb.BuildModel(ground)'''

'''print "Test Build Frustum"
center = vt(10, 10, 10)
frustum = Frustum(center, 5, 2, 2, 4, 4, "fru")
face_front = Face([[1, 5],[5, 5],[5, 9],[1, 9]], "Front")
face_left = Face([[10, 50],[50, 50],[50, 90],[10, 90]], "Left")
frustum.faces.append(face_front)
frustum.faces.append(face_left)
results = mb.BuildModel(frustum)'''

'''print "Test Build Prism"
center = vt(0, 0, 0)
prism = Prism(center, 8, 6, 4, "pri")
face_front = Face([[1, 5],[5, 5],[5, 9]], "Front")
face_left = Face([[10, 50],[50, 50],[50, 90],[10, 90]], "Left")
face_right = Face([[100, 500],[500, 500],[500, 900],[100, 900]], "Right")
prism.faces.append(face_front)
prism.faces.append(face_left)
prism.faces.append(face_right)
results = mb.BuildModel(prism)'''

for i in results:
    print "In results, the polygon i: "
    print "Vertex: "
    for j in i.VertexList:
        print j.x, j.y, j.z
    print "Texels: "
    for k in i.TexelList:
        print k.u, k.v
