# faceOrientation can be any of the following string:
#	"Left"
#	"Right"
#	"Front"
#	"Upper"
#   "Surface"
#"Surface" is used to represent a sky or ground face
#face orientation and facePoints can determine a face in a 3D shape
class Shape:
    def __init__(self, name):
        self.faces = []
        self.name = name


class Cylinder(Shape):
    def __init__(self, center, radius, height,name):
        Shape.__init__(self, name)
        self.center = center
        self.radius = radius
        self.height = height


class Cuboid(Shape):
    def __init__(self, center, length, width, height, name):
        Shape.__init__(self, name)
        self.center = center
        self.length = length
        self.width = width
        self.height = height


class Prism(Shape):
    def __init__(self, center, length, width, height, name):
        Shape.__init__(self, name)
        self.center = center
        self.length = length
        self.width = width
        self.height = height


class Frustum(Shape):
    def __init__(self, center, height, upperLength, upperWidth, lowerLength, lowerWidth, name):
        Shape.__init__(self, name)
        self.center = center
        self.height = height
        self.upperLength = upperLength
        self.upperWidth = upperWidth
        self.lowerLength = lowerLength
        self.lowerWidth = lowerWidth


class Tree():
    def __init__(self, center, heihgt,name):
        self.center = center
        self.height = height
        self.name = name
        self.lineIds = []


class Ground():
    def __init__(self, name):
        self.faces =[]
        self.name = name
        self.lineIds = []


class Sky():
    def __init__(self, name):
        self.faces =[]
        self.name = name
        self.lineIds = []


class Face():
    def __init__(self, facePoints, faceOrientation):
        self.facePoints = facePoints
        self.lineIds = []
        self.faceOrientation = faceOrientation


