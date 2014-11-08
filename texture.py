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
		self.a=0.0
		self.b=0.0
		self.c=0.0
		self.d=0.0
	
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
				minw = polygon.Texel[i].u
			if polygon.Texel[i].v > maxh:
				maxh = polygon.Texel[i].v
			if polygon.Texel[i].v < minh:
				minh = polygon.Texel[i].v
			#ax = x+1.0/polygon.Texel[i].u
			#ay = y+1.0/polygon.Texel[i].v
		return maxw, maxh, minw, minh
	def distanceT(self, p1, p2):
		return math.fabs(p1[0]-p2[0]),math.fabs(p1[1]-p2[1])
		#return math.sqrt(math.pow(2, p1[0]-p2[0])+math.pow(2, p1[1]-p2[1]))
	
	def setPlane(self, polygon):
		p1 = polygon.Vertex[1].x-polygon.Vertex[0].x
		p2 = polygon.Vertex[1].y-polygon.Vertex[0].y
		p3 = polygon.Vertex[1].z-polygon.Vertex[0].z
		p4 = polygon.Vertex[2].x-polygon.Vertex[0].x
		p5 = polygon.Vertex[2].y-polygon.Vertex[0].y
		p6 = polygon.Vertex[2].z-polygon.Vertex[0].z
		a = p2*p6-p3*p5
		b = p3*p4-p1*p6
		c = p1*p5-p2*p4
		d = a*polygon.Vertex[0].x+b*polygon.Vertex[0].y+c*polygon.Vertex[0].z
		d = -1.0*d
		self.a=a
		self.b=b
		self.c=c
		self.d=d
	
	def getZ(self, rx, ry):
		return -1.0*((self.a*rx+self.b*ry+self.d)/self.c)
	def insidePolygon(self, polygon, p):
		i =0
		j =len(polygon.Texel)-1
		result = False
		for i in range(len(polygon.Texel)):
			if ((polygon.Texel[i].v>p[1])!=(polygon.Texel[j].v>p[1]))and(p[0]<((polygon.Texel[j].u-polygon.Texel[i].u)*(p[1]-polygon.Texel[i].v)/(polygon.Texel[j].v-polygon.Texel[i].v)+polygon.Texel[i].u)):
				if result == False:
					result = True
				else:
					result = False
			#print ((polygon.Vertex[i].y>p[1])!=(polygon.Vertex[j].y>p[1])), " ",(polygon.Vertex[i].y>p[1]), " ", (polygon.Vertex[j].y>p[1]) 
			j=i
		print result
		return result

	def getCoord(self, polygon, texel):
		num = len(polygon.Texel)
		lix = []
		liy = []
		li = []
		ax = 0.0
		ay = 0.0
		aa = 0.0
		dd = 0.0
		du = 0.0
		dv = 0.0
		rx = 0.0
		ry = 0.0
		rz = 0.0
		for i in range(num):
			du, dv = self.distanceT(texel, [polygon.Texel[i].u, polygon.Texel[i].v]) 
			#print texel, " ",  [polygon.Texel[i].u, polygon.Texel[i].v]
			'''if du!=0:
				lix.append(du)
				ax = ax + 1.0/du
			if dv!=0:
				liy.append(dv)
				ay = ay + 1.0/dv'''
			dd = math.sqrt(du*du+dv*dv)
			if dd!=0:
				li.append(dd)
				aa = aa + 1.0/dd
		'''for i in range(len(lix)):
			lix[i] = 1.0/(lix[i]*ax)
		for i in range(len(liy)):
			liy[i] = 1.0/(liy[i]*ay)'''
		for i in range(len(li)):
			li[i] = 1.0/(li[i]*aa)
		for i in range(num):
			rx = rx+li[i]*polygon.Vertex[i].x
			ry = ry+li[i]*polygon.Vertex[i].y
			ry = rz+li[i]*polygon.Vertex[i].z
			'''
			rx = rx+lix[i]*polygon.Vertex[i].x
			ry = ry+liy[i]*polygon.Vertex[i].y
		rz = self.getZ(rx, ry)'''
		return [rx, ry, rz]
	
	def putTexture(self, polygon):
		self.setPlane(polygon)
		plist = []
		maxw, maxh, minw, minh = self.defineSize(polygon)
		print minw, " ", maxw, " ", minh, " ", maxh
		for i in range(minw+1, maxw-2):
			for j in range(minh+1, maxh-2):
				if self.insidePolygon(polygon, [i, j]):
					dp = self.getCoord(polygon, [i, j])
					plist.append(Point(dp[0], dp[1], dp[2], self.texture[i,j,0], self.texture[i,j,1], self.texture[i,j,2]))
					#print "zzzzzzzzzzzzzzzzzzzzzz"
		return plist
						

				
		
