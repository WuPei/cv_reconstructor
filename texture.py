import cv2
#import cv2.cv
import numpy as np
import sys
import math

class Point:
	def __init__(self, x, y, z, r, g, b):
		self.x = x
		self.y = y
		self.z = z
		self.r = r
		self.g = g
		self.b = b
	def getCoord(self):
		return [self.x, self.y, self.z]
	def getColor(self):
		return [self.r, self.g, self.b]

class Texture:
	'''put texture to polygon'''
	def __init__(self, image):
		self.texture = image
	
	def __del__(self):
		self.texture = None
	
	def defineSize(self, polygon):
		maxw=-1.0
		maxh=-1.0
		minw=10000000.0
		minh=10000000.0
		x = 0.0
		y = 0.0
		for i in range(len(polygon.Texel)):
			if polygon.Texel[i].u > maxw:
				maxw = polygon.Texel[i].u
			if polygon.Texel[i].u < minw:
				minw = polygon.Texel[i].v
			if polygon.Texel[i].v > maxh:
				maxh = polygon.Texel[i].v
			if polygon.Texel[i].v < minh:
				minh = polygon.Texel[i].v
			ax = x+1.0/polygon.Texel[i].u
			ay = y+1.0/polygon.Texel[i].v
		return maxw, maxh, minw, minh
	def distanceT(p1, p2):
		return math.fabs(p1[0]-p2[0]),math.fabs(p1[1]-p2[1])
		#return math.sqrt(math.pow(2, p1[0]-p2[0])+math.pow(2, p1[1]-p2[1]))
	
	def setPlane(self, polygon):
		p1 = polygon.Vertex[1].x-polygon.Vertex[0].x
		p2 = polygon.Vertex[1].y-polygon.Vertex[0].y
		p3 = polygon.Vertex[1].z-polygon.Vertex[0].z
		p4 = polygon.Vertex[2].x-polygon.Vertex[0].x
		p5 = polygon.Vertex[2].y-polygon.Vertex[0].y
		p5 = polygon.Vertex[2].z-polygon.Vertex[0].z
		a = p2*p6-p3*p5
		b = p3*p4-p1*p6
		c = p1*p5-p2*p4
		d = a*polygon.Vertex[0].x+b*polygon.Vertex[0].y+c*polygon.Vertex[0].z
		d = -1.0*d
		self.plane.a=a
		self.plane.b=b
		self.plane.c=c
		self.plane.d=d
	
	def getZ(self, rx, ry):
		return -1.0*((self.plane.a*rx+self.plane.b*ry+self.plane.d)/c)
	def insidePolygon(self, polygon, p):
		i =0
		j =len(polygon.Texel)-1
		result = False
		for i in range(len(polygon.Texel)):
			if ((polygon.Vertex[i].y>p[1])!=(polygon.Vertex[j].y>p[1]))and(p[0]<((polygon.Vertex[j].x-polygon.Vertex[i].x)*(p[1]-polygon.Vertex[i].y)/(polygon.Vertex[j].y-polygon.Vertex[i].y)+polygon.Vertex[i].x)):
				result = True
		return result

	def getCoord(self, polygon, texel):
		num = len(polygon.Texel)
		lix = []
		liy = []
		ax = 0.0
		ay = 0.0
		du = 0.0
		dv = 0.0
		rx = 0.0
		ry = 0.0
		rz = 0.0
		for i in range(num):
			du, dv = distanceT(texel, [polygon.Texel[i].u, polygon.Texel[i].v]) 
			lix.append(du)
			liy.append(dv)
			ax = ax + 1.0/du
			ay = ay + 1.0/dv
		for i in range(num):
			lix[i] = 1.0/(lix[i]*ax)
			liy[i] = 1.0/(lix[i]*ay)
		for i in range(num):
			rx = rx+lix[i]*polygon.Vertex[i].x
			ry = ry+liy[i]*polygon.Vertex[i].y
		rz = self.getZ(self, rx, ry)
		return [rx, ry, rz]
	
	def putTexture(self, polygon):
		self.setPlane(polygon)
		plist = []
		maxw, maxh, minw, minh = self.defineSize(polygon)
		for i in range(minw, maxw):
			for j in range(minh, maxh):
				if insidePolygon(polygon, [i, j]):
					dp = getCoord(polygon, [i, j])
					plist.append(Point(dp[0], dp[1], dp[2], self.texture[i,j,0], self.texture[i,j,1], self.texture[i,j,2]))
		return plist
						

				
		
