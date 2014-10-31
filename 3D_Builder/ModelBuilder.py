# CS4243: Computer Vision and Pattern Recognition
# Zhou Bin
# 29th, Oct, 2014

import numpy as np
from Vertex import Vertex as vt
from Polygon import Polygon

class ModelBuilder:

	###########################################################
	# Build cuboid from four vertex
	###########################################################
	# V1 is on front, left, bottom corner
	# V2 is on front, right, bottom corner
	# V3 is on front, left, top corner
	# V4 is on back, left, bottom corner
	# UVs is a list containing all texel needed for eight vertices
	def BuildCuboid (self, v1, v2, v3, v4, UVs):
		# Generate all vertices from given 4 vertices
		# with ver1-4 on bottom, ver5-8 on top
		ver1 = vt.equal(v1);
		ver2 = vt.equal(v2);
		ver3 = vt.sum(v1, vt.sum(vt.diff(v4,v1),vt.diff(v2,v1)))
		ver4 = vt.equal(v4);
		ver5 = vt.equal(v3);
		ver6 = vt.sum(v3, vt.diff(v2, v1))
		ver7 = vt.sum(ver3, vt.diff(v3, v1))
		ver8 = vt.sum(v3, vt.diff(v4, v1))
		
		# Store corresponding Texel coordinates
		
		# Generate polygons
		poly1 = Polygon([ver1, ver2, ver3, ver4], [])
		poly2 = Polygon([ver5, ver6, ver7, ver8], [])
		poly3 = Polygon([ver1, ver2, ver6, ver5], [])
		poly4 = Polygon([ver2, ver3, ver7, ver6], [])
		poly5 = Polygon([ver3, ver4, ver8, ver7], [])
		poly6 = Polygon([ver4, ver1, ver5, ver8], [])
		
		# Return list of polygons
		polyList = [poly1, poly2, poly3, poly4, poly5, poly6]
		return polyList
		
		
	
	###########################################################
	# Build Cylinder
	###########################################################
	# Given two points, compute the middle point between them on circle
	# c being center of circle.
	def ComputeMidVector (self, a, b, c, r):
		temp = vt.sum(vt.diff(a, c), vt.diff(b, c))
		temp = vt.normalize(temp)
		temp = vt.scale(temp, r)
		temp = vt.sum(c, temp)
		return temp
	# V1 is the center of circle on bottom/top surface
	# V2 is on the circle on bottom/top surface (V1,V2 on same surface)
	# V3 is the center of circle on top/btm surface
	def BuildCylinder (self, v1, v2, v3):
		# Generate radius of circle
		radius = vt.distance(v1, v2)

		# Generate all vertices from given
		# Vertex on one circle surface
		ver1 = vt.equal(v1)
		ver2 = vt.equal(v2)
		ver3 = vt.sum(v1, vt.diff(v1, v2))
		# Generate third&fourth vertices on verticle line
		temp = vt.cross(vt.diff(v2, v1), vt.diff(v3, v1))
		temp = vt.normalize(temp)
		temp = vt.scale(temp, radius)
		ver4 = vt.sum(v1, temp)
		ver5 = vt.sum(v1, vt.diff(ver1, ver4))
		ver6 = self.ComputeMidVector(ver2, ver5, ver1, radius)
		ver7 = vt.sum(v1, vt.diff(ver1, ver6))
		ver8 = self.ComputeMidVector(ver2, ver4, ver1, radius)
		ver9 = vt.sum(v1, vt.diff(ver1, ver6))
		# Vertex on the other circle surface
		ver1_2 = vt.equal(v1)
		ver2_2 = vt.sum(ver2, vt.diff(v3, v1))
		ver3_2 = vt.sum(ver3, vt.diff(v3, v1))
		ver4_2 = vt.sum(ver4, vt.diff(v3, v1))
		ver5_2 = vt.sum(ver5, vt.diff(v3, v1))
		ver6_2 = vt.sum(ver6, vt.diff(v3, v1))
		ver7_2 = vt.sum(ver7, vt.diff(v3, v1))
		ver8_2 = vt.sum(ver8, vt.diff(v3, v1))
		ver9_2 = vt.sum(ver9, vt.diff(v3, v1))
		
		# Generate polygons
		poly1 = Polygon([ver2, ver6, ver6_2, ver2_2], [])
		poly2 = Polygon([ver6, ver5, ver5_2, ver6_2], [])
		poly3 = Polygon([ver5, ver9, ver9_2, ver5_2], [])
		poly4 = Polygon([ver9, ver3, ver3_2, ver9_2], [])
		poly5 = Polygon([ver3, ver7, ver7_2, ver3_2], [])
		poly6 = Polygon([ver7, ver4, ver4_2, ver7_2], [])
		poly7 = Polygon([ver4, ver8, ver8_2, ver4_2], [])
		poly8 = Polygon([ver8, ver2, ver2_2, ver8_2], [])
		poly9 = Polygon([ver2,ver6,ver5,ver9,ver3,ver7,ver4,ver8], [])
		poly10 = Polygon([ver2_2,ver6_2,ver5_2,ver9_2,ver3_2,ver7_2,ver4_2,ver8_2], [])
		
		# Return list of polygons
		polyList = [poly1, poly2, poly3, poly4, poly5, poly6, poly7, poly8, poly9, poly10]
		return polyList
		
		
		
	###########################################################
	# Build a plane (ground and sky)
	###########################################################	
	# a, b, c are vertices of the plane
	# UVs are all texel values
	def BuildPlane (self, a, b, c, UVs):
		# Generate all four vectors
		ver1 = vt.equal(a)
		ver2 = vt.equal(b)
		ver3 = vt.equal(c)
		ver4 = vt.sum(b, vt.sum(vt.diff(a,b), vt.diff(c,b)))
		
		#
		poly = Polygon([ver1, ver2, ver3, ver4], [UVs])
		polyList = [poly]
		return polyList
	
	
	
	###########################################################
	# Build frustum (normally for roofs)
	###########################################################	
	# a is front, left, bottom corner
	# b is front, right, bottom corner
	# c is front, left, top corner
	# d is back, left, bottom corner
	# UVs are all texels needed for all surfaces
	def BuildFrustum (self, a, b, c, d):
		# Generate all vertices
		ver1 = vt.equal(a)
		ver2 = vt.equal(b)
		ver3 = vt.sum(a, vt.sum(vt.diff(b,a), vt.diff(d,a)))
		ver4 = vt.equal(d)
		ver5 = vt.equal(c)
		ver6 = vt(ver2.x-(ver5.x-ver1.x), ver5.y, ver2.z-(ver1.z-ver5.z))
		ver7 = vt(ver3.x-(ver5.x-ver1.x), ver5.y, ver3.z+(ver1.z-ver5.z))
		ver8 = vt(ver4.x+(ver5.x-ver1.x), ver5.y, ver4.z+(ver1.z-ver5.z))
		
		# Generate polygons
		poly1 = Polygon([ver1, ver2, ver3, ver4], [])
		poly2 = Polygon([ver5, ver6, ver7, ver8], [])
		poly3 = Polygon([ver1, ver2, ver6, ver5], [])
		poly4 = Polygon([ver2, ver3, ver7, ver6], [])
		poly5 = Polygon([ver3, ver4, ver8, ver7], [])
		poly6 = Polygon([ver4, ver1, ver5, ver8], [])
		
		# Return list of polygons
		polyList = [poly1, poly2, poly3, poly4, poly5, poly6]
		return polyList
		
		