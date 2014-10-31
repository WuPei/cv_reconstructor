import sys
import cv2
#import cv2.cv
import math
import numpy as np
import numpy.linalg as la


class Depth:
	def __init__(self, image, sp, ctf, cif, cjf, ckf, f, bu, bv, u0, v0):
		self.texture = image
		self.ctf = ctf
		self.cif = cif
		self.cjf = cjf
		self.ckf = ckf
		self.f = f
		self.bu = bu
		self.bv = bv
		self.u0 = u0
		self.v0 = v0
		self.M = np.matrix([[f*bu, 0, u0, 0],[0,f*bv, v0, 0],[0, 0, 1, 0]])
	
	def getPointCoord(self, cp):
		coord2D = matrix([[cp.x],[cp.y],[cp.z]]) 
		coord3D = la.solve(self.M, coord2D)
		return [coord3D[0,1], coord3D[0,2], coord3D[0,3]]
	
#def getZCoord(self, cp)
		
