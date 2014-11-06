#faceOrientation can be any of the following string:
#	"Left"
#	"Right"
#	"Front"
#	"Upper"
#face orientation and facePoints can determine a face in a 3D shape
class Shape:
	def __init__(self):
		self.faces =[]
	def addFace(self,facePoints,faceOrientation):
		self.faces.append([facePoints,faceOrientation])

class Cylinder(Shape):
	def __init__(self,center,radius,height):
		Shape.__init__(self)
		self.center = center
		self.radius = radius
		self.height = height

class Cuboid(Shape):
	def __init__(self,center,length,width,height):
		Shape.__init__(self)
		self.center = center
		self.length = length
		self.width = width
		self.height = height

class Prism(Shape):
	def __init__(self,center,length,width,height):
		Shape.__init__(self)
		self.center = center
		self.length = length
		self.width = width
		self.height = height

class Frustum(Shape):
	def __init__(self,center,height,upperLength,upperWidth,lowerLength,lowerWidth):
		Shape.__init__(self)
		self.center = center
		self.height = height
		self.upperLength = upperLength
		self.upperWidth = upperWidth
		self.lowerLength = lowerLength
		self.lowerWidth = lowerWidth

class Tree():
	def __init__(self,center,heihgt):
		self.center = center
		self.height = height

class Ground():
	def __init__(self,facePoints):
		self.facePoints  = facePoints

class Sky():
	def __init__(self,facePoints):
		self.facePoints  = facePoints








