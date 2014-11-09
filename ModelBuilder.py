# CS4243: Computer Vision and Pattern Recognition
# Zhou Bin
# 29th, Oct, 2014

import numpy as np
from Vertex import Vertex as vt
from Texel import Texel as tx
from Polygon import Polygon
from shape import Shape
from shape import Cylinder
from shape import Cuboid
from shape import Prism
from shape import Frustum
from shape import Ground
from shape import Sky
from shape import Face
from shape import Tree

class ModelBuilder:

	###########################################################
	# Build cuboid from four vertex
	###########################################################
	# center is the middle point on the bottom surface
	# len, wid and hei indicate length,width,height for cuboid
	# UVs is a list containing all texel needed for eight vertices
	def BuildCuboid (self, center, length, width, height, UVs):
		#-------------------------------------------------------
		# Generate all vertices from given 4 vertices
		# with ver1-4 on bottom, ver5-8 on top
		cx = center[0]
		cy = center[1]
		cz = center[2]
		ver1 = vt(cx-length/2, cy, cz+width/2)
		ver2 = vt(cx+length/2, cy, cz+width/2)
		ver3 = vt(cx+length/2, cy, cz-width/2)
		ver4 = vt(cx-length/2, cy, cz-width/2)
		ver5 = vt(cx-length/2, cy+height, cz+width/2)
		ver6 = vt(cx+length/2, cy+height, cz+width/2)
		ver7 = vt(cx+length/2, cy+height, cz-width/2)
		ver8 = vt(cx-length/2, cy+height, cz-width/2)
		'''
		ver1 = vt.equal(v1)
		ver2 = vt.equal(v2)
		ver3 = vt.sum(v1, vt.sum(vt.diff(v4,v1),vt.diff(v2,v1)))
		ver4 = vt.equal(v4)
		ver5 = vt.equal(v3)
		ver6 = vt.sum(v3, vt.diff(v2, v1))
		ver7 = vt.sum(ver3, vt.diff(v3, v1))
		ver8 = vt.sum(v3, vt.diff(v4, v1))
		'''
		

		#-------------------------------------------------------
		# Store corresponding Texel coordinates
		exist_front = False
		exist_left = False
		exist_right = False
		exist_top = False
		uv_front = []
		#uv_back = []
		uv_left = []
		uv_right = []
		uv_top = [] 
		#uv_btm = []
		# Assign uvs from input
		for i in UVs:
			# Left surface
			if(i.faceOrientation=="Left"):
				exist_left = True
				for j in i.facePoints:
					uv_left.append(tx(j[0], j[1]))
			# Right surface
			elif(i.faceOrientation=="Right"):
				exist_right = True
				for j in i.facePoints:
					uv_right.append(tx(j[0], j[1]))
			# Front surface
			elif(i.faceOrientation=="Front"):
				exist_front = True
				for j in i.facePoints:
					uv_front.append(tx(j[0], j[1]))
			# Upper surface
			elif(i.faceOrientation=="Upper"):
				exist_top = True
				for j in i.facePoints:
					uv_top.append(tx(j[0], j[1]))
			else:
				print "Face denifition got errors!! Nor left, right, front or Upper."
		# Invent surfaces not provided in inputs
		# Invent front surface if not exist
		if(exist_front == False):
			if(exist_left): # Use left surface as FRONT also
				for i in uv_left:
					uv_front.append(i)
				exist_front = True
			else:
				if(exist_right): # use right surface as FRONT also
					for i in uv_right:
						uv_front.append(i)
					exist_front = True
				else:
					print "Front surface wanna copy from left or right, BUT Fail !!!"
		# Invent left surface if not exist. (front surface already exist here)
		if(exist_left == False):
			if(exist_right): # use right surface as LEFT also
				for i in uv_right:
					uv_left.append(i)
				exist_left = True
			else :
				if(exist_front): # use front surface as LEFT also
					for i in uv_front:
						uv_left.append(i)
					exist_left = True
				else:
					print "Left surface wanna copy from right or front, BUT Fail !!!"
		# Invent right surface is not exist. (front, left already exist here)
		if(exist_right == False):
			if(exist_left): # use right surface as RIGHT also
				for i in uv_left:
					uv_right.append(i)
				exist_right = True
			else :
				if(exist_front): # use front surface as RIGHT also
					for i in uv_front:
						uv_right.append(i)
					exist_right = True
				else:
					print "Right surface wanna copy from left or front, BUT Fail !!!"
		# Invent top surface 
		if(exist_top == False):
			if(exist_front):
				for i in uv_front:
					uv_top.append(i)
				exist_top = True
			else:
				print "Top surface wanna copy from front, BUT Fail !!!"
		# Invent btm surface
		# if(exist_top):
		# 	for i in uv_top:
		# 		uv_btm.append(i)
		# else:
		# 	print "Bottom surface wanna copy from top, BUT Fail !!!"
		# # Invent back surface
		# if(exist_front):
		# 	for i in uv_front:
		# 		uv_back.append(i)
		# else:
		# 	print "Back surface wanna copy from front, BUT Fail !!!"

			
		

		#-------------------------------------------------------
		# Generate polygons
		#poly1 = Polygon([ver1, ver2, ver3, ver4], uv_btm)
		poly2 = Polygon([ver5, ver6, ver7, ver8], uv_top)
		poly3 = Polygon([ver1, ver2, ver6, ver5], uv_front)
		poly4 = Polygon([ver2, ver3, ver7, ver6], uv_right)
		#poly5 = Polygon([ver3, ver4, ver8, ver7], uv_back)
		poly6 = Polygon([ver4, ver1, ver5, ver8], uv_left)
		

		#-------------------------------------------------------
		# Return list of polygons
		polyList = [poly2, poly3, poly4, poly6]
		return polyList
		
		
	
	###########################################################
	# Build Cylinder
	###########################################################
	# Given two points, compute the middle point between them on circle
	# center being center of circle.
	def ComputeMidVector (self, a, b, center, r):
		temp = vt.sum(vt.diff(a, center), vt.diff(b, center))
		temp = vt.normalize(temp)
		temp = vt.scale(temp, r)
		temp = vt.sum(center, temp)
		return temp
	def BuildCylinder (self, center, radius, height, UVs):
		#-------------------------------------------------------
		cx = center[0]
		cy = center[1]
		cz = center[2]
		center = vt(cx, cy, cz)
		# Generate vertices on bottom surface
		btm_v = [None] * 16
		# Compute btm_v0, 4, 8, 12
		btm_v[0] = vt(cx+radius, cy, cz)
		btm_v[8] = vt(cx-radius, cy, cz)
		btm_v[4] = vt(cx, cy, cz+radius)
		btm_v[12] = vt(cx, cy, cz-radius)
		# Compute btm_v2, 6, 10, 14
		for i in [0, 4]:
			btm_v[i+2] = self.ComputeMidVector(btm_v[i], btm_v[i+4], center, radius)
			btm_v[i+2+8] = vt.sum(center, vt.diff(center, btm_v[i+2]))
		# Compute vtm_1,3,5,7 and 9,11,13,15
		for i in [0, 2, 4, 6]:
			btm_v[i+1] = self.ComputeMidVector(btm_v[i], btm_v[i+2], center, radius)
			btm_v[i+1+8] = vt.sum(center, vt.diff(center, btm_v[i+1]))

		# Generate vertices on top surface
		top_v = []
		for i in range(16):
			temp = vt(btm_v[i].x, btm_v[i].y+height, btm_v[i].z)
			top_v.append(temp)

		# Generate all vertices from given
		# Vertex on one circle surface
		'''ver1 = vt.equal(center)
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
		ver9 = vt.sum(v1, vt.diff(ver1, ver6))'''


		#-------------------------------------------------------
		# Store corresponding Texel coordinates
		print "----------------------------"
		tx1 = UVs[0].facePoints[0]
		#print tx1
		tx2 = UVs[0].facePoints[1]
		#print tx2
		tx3 = UVs[0].facePoints[2]
		#print tx3
		tx4 = UVs[0].facePoints[3]
		#print tx4
		dis_btm = [tx2[0]-tx1[0], tx2[1]-tx1[1]]
		dis_top = [tx3[0]-tx4[0], tx3[1]-tx4[1]]
		dis_left = [tx4[0]-tx1[0], tx4[1]-tx1[1]]
		dis_right = [tx3[0]-tx2[0], tx3[1]-tx2[1]]
		#print dis_btm
		#print dis_top
		tx_btm = [] # store all nice texels on bottom edge 
		tx_top = [] # store all nice texels on top edge 
		tx_left = [] # store all five texels on left edge
		tx_right = [] # store all five texels on right edge
		uv_front = []
		uv_back = []
		uv_top = []
		uv_btm = []
		# Divide two texels into 9 texels on top and btm edge
		for i in range(9):
			tx_btm.append(tx(tx1[0]+i*dis_btm[0]/8.0, tx1[1]+i*dis_btm[1]/8.0))
			tx_top.append(tx(tx4[0]+i*dis_top[0]/8.0, tx4[1]+i*dis_top[1]/8.0))
		# Divde two texels into 5 texels on left and right edge
		for i in range(4):
			tx_right.append(tx(tx2[0]+i*dis_right[0]/4.0, tx2[1]+i*dis_right[1]/4.0))
			tx_left.append(tx(tx4[0]-i*dis_left[0]/4.0, tx4[1]-i*dis_left[1]/4.0))

		# Generate the 16 side surfaces based on 18 texels
		for i in range(8):
			uv_front.append([tx_btm[i], tx_btm[i+1], tx_top[i+1], tx_top[i]])
			uv_back.append([tx_btm[i], tx_btm[i+1], tx_top[i+1], tx_top[i]])
		# Generate the top and btm surface's texels
		for i in range(4):
			uv_btm.append(tx_btm[2*i])
			uv_top.append(tx_btm[2*i])
		for i in range(4):
			uv_btm.append(tx_right[i])
			uv_top.append(tx_right[i])
		for i in range(4):
			uv_btm.append(tx_top[2*i])
			uv_top.append(tx_top[8 - 2*i])
		for i in range(4):
			uv_btm.append(tx_left[i])
			uv_top.append(tx_left[i])


		
		#-------------------------------------------------------
		# Generate polygons
		polyList = []
		temp_top = []
		temp_btm = []
		# The two circle polygon on top and bot
		for i in range(16):
			temp_top.append(top_v[i])
			temp_btm.append(btm_v[i])
		#polyList.append(Polygon(temp_btm, uv_btm))
		polyList.append(Polygon(temp_top, uv_top))
		# The 16 polygons on side
		for i in range(16):
			if(i < 8):
				tempPolygon = Polygon([btm_v[i], btm_v[(i+1)%16], top_v[(i+1)%16], top_v[i]], uv_front[i])
			else:
				tempPolygon = Polygon([btm_v[i], btm_v[(i+1)%16], top_v[(i+1)%16], top_v[i]], uv_back[i-8])
			polyList.append(tempPolygon)
		

		#-------------------------------------------------------
		# Return list of polygons
		return polyList
		
		
		
	###########################################################
	# Build a plane (ground and sky)
	###########################################################	
	# a, b, c are vertices of the plane
	# UVs are all texel values
	def BuildPlane (self, height, facePoints):
		length = 500
		width = 500
		#-------------------------------------------------------
		# Generate all four vectors
		ver1 = vt(-length, height, width)
		ver2 = vt(length, height, width)
		ver3 = vt(length, height, -width)
		ver4 = vt(-length, height, -width)


		#-------------------------------------------------------
		# Store corresponding Texel coordinates
		uvs = []
		for i in facePoints:
			uvs.append(tx(i[0], i[1]))


		#-------------------------------------------------------
		poly = Polygon([ver1, ver2, ver3, ver4], uvs)
		polyList = [poly]
		return polyList
	
	
	
	###########################################################
	# Build frustum (normally for roofs)
	###########################################################	
	# The top and bottom surface are rectangle with length and width to be
	# btm_len, btm_wid, top_len, top_wid. Height is the distance between them
	# UVs are all texels needed for all surfaces
	def BuildFrustum (self, center, btm_len, btm_wid, top_len, top_wid, height, UVs):
		#-------------------------------------------------------
		# Generate all vertices
		cx = center[0]
		cy = center[1]
		cz = center[2]
		ver1 = vt(cx-btm_len/2, cy, cz+btm_wid/2)
		ver2 = vt(cx+btm_len/2, cy, cz+btm_wid/2)
		ver3 = vt(cx+btm_len/2, cy, cz-btm_wid/2)
		ver4 = vt(cx-btm_len/2, cy, cz-btm_wid/2)
		ver5 = vt(cx-top_len/2, cy+height, cz+top_wid/2)
		ver6 = vt(cx+top_len/2, cy+height, cz+top_wid/2)
		ver7 = vt(cx+top_len/2, cy+height, cz-top_wid/2)
		ver8 = vt(cx-top_len/2, cy+height, cz-top_wid/2)

		
		#-------------------------------------------------------
		# Store corresponding Texel coordinates
		exist_front = False
		exist_left = False
		exist_right = False
		exist_top = False
		uv_front = []
		#uv_back = []
		uv_left = []
		uv_right = []
		uv_top = [] 
		#uv_btm = []
		# Assign uvs from input
		for i in UVs:
			# Left surface
			if(i.faceOrientation=="Left"):
				exist_left = True
				for j in i.facePoints:
					uv_left.append(tx(j[0], j[1]))
			# Right surface
			elif(i.faceOrientation=="Right"):
				exist_right = True
				for j in i.facePoints:
					uv_right.append(tx(j[0], j[1]))
			# Front surface
			elif(i.faceOrientation=="Front"):
				exist_front = True
				for j in i.facePoints:
					uv_front.append(tx(j[0], j[1]))
			# Upper surface
			elif(i.faceOrientation=="Upper"):
				exist_top = True
				for j in i.facePoints:
					uv_top.append(tx(j[0], j[1]))
			else:
				print "Face denifition got errors!! Nor left, right, front or Upper."
		# Invent surfaces not provided in inputs
		# Invent front surface if not exist
		if(exist_front == False):
			if(exist_left): # Use left surface as FRONT also
				for i in uv_left:
					uv_front.append(i)
				exist_front = True
			else:
				if(exist_right): # use right surface as FRONT also
					for i in uv_right:
						uv_front.append(i)
					exist_front = True
				else:
					print "Front surface wanna copy from left or right, BUT Fail !!!"
		# Invent left surface if not exist. (front surface already exist here)
		if(exist_left == False):
			if(exist_right): # use right surface as LEFT also
				for i in uv_right:
					uv_left.append(i)
				exist_left = True
			else :
				if(exist_front): # use front surface as LEFT also
					for i in uv_front:
						uv_left.append(i)
					exist_left = True
				else:
					print "Left surface wanna copy from right or front, BUT Fail !!!"
		# Invent right surface is not exist. (front, left already exist here)
		if(exist_right == False):
			if(exist_left): # use right surface as RIGHT also
				for i in uv_left:
					uv_right.append(i)
				exist_right = True
			else :
				if(exist_front): # use front surface as RIGHT also
					for i in uv_front:
						uv_right.append(i)
					exist_right = True
				else:
					print "Right surface wanna copy from left or front, BUT Fail !!!"
		# Invent top surface 
		if(exist_top == False):
			if(exist_front):
				for i in uv_front:
					uv_top.append(i)
				exist_top = True
			else:
				print "Top surface wanna copy from front, BUT Fail !!!"
		# # Invent btm surface
		# if(exist_top):
		# 	for i in uv_top:
		# 		uv_btm.append(i)
		# else:
		# 	print "Bottom surface wanna copy from top, BUT Fail !!!"
		# # Invent back surface
		# if(exist_front):
		# 	for i in uv_front:
		# 		uv_back.append(i)
		# else:
		# 	print "Back surface wanna copy from front, BUT Fail !!!"


		#-------------------------------------------------------
		# Generate polygons
		#poly1 = Polygon([ver1, ver2, ver3, ver4], uv_btm)
		poly2 = Polygon([ver5, ver6, ver7, ver8], uv_top)
		poly3 = Polygon([ver1, ver2, ver6, ver5], uv_front)
		poly4 = Polygon([ver2, ver3, ver7, ver6], uv_right)
		#poly5 = Polygon([ver3, ver4, ver8, ver7], uv_back)
		poly6 = Polygon([ver4, ver1, ver5, ver8], uv_left)
		

		#-------------------------------------------------------
		# Return list of polygons
		polyList = [poly2, poly3, poly4, poly6]
		return polyList
		
	

	###########################################################
	# Build prism (normally for roofs)
	###########################################################	
	def BuildPrism (self, center, length, width, height, UVs):
		#-------------------------------------------------------
		# Define all 6 vertices
		cx = center[0]
		cy = center[1]
		cz = center[2]
		ver1 = vt(cx-length/2, cy, cz+width/2)
		ver2 = vt(cx+length/2, cy, cz+width/2)
		ver3 = vt(cx+length/2, cy, cz-width/2)
		ver4 = vt(cx-length/2, cy, cz-width/2)
		ver5 = vt(cx, cy+height, cz+width/2)
		ver6 = vt(cx, cy+height, cz-width/2)


		#-------------------------------------------------------
		# Store corresponding Texel coordinates
		exist_front = False
		exist_left = False
		exist_right = False
		uv_front = []
		#uv_back = []
		uv_left = []
		uv_right = []
		#uv_btm = []
		# Assign uvs from input
		for i in UVs:
			# Left surface
			if(i.faceOrientation=="Left"):
				exist_left = True
				for j in i.facePoints:
					uv_left.append(tx(j[0], j[1]))
			# Right surface
			elif(i.faceOrientation=="Right"):
				exist_right = True
				for j in i.facePoints:
					uv_right.append(tx(j[0], j[1]))
			# Front surface
			elif(i.faceOrientation=="Front"):
				exist_front = True
				for j in i.facePoints:
					uv_front.append(tx(j[0], j[1]))
			else:
				print "Face denifition got errors!! Nor left, right, front or Upper."
		# Invent surfaces not provided in inputs
		# Invent front surface if not exist
		if(exist_front == False):
			if(exist_left): # Use left surface as FRONT also
				for i in range(3):
					uv_front.append(uv_left[i])
				exist_front = True
			else:
				if(exist_right): # use right surface as FRONT also
					for i in range(3):
						uv_front.append(uv_right[i])
					exist_front = True
				else:
					print "Front surface wanna copy from left or right, BUT Fail !!!"
		# Invent left surface if not exist. (front surface already exist here)
		if(exist_left == False):
			if(exist_right): # use right surface as LEFT also
				for i in uv_right:
					uv_left.append(i)
				exist_left = True
			else :
				if(exist_front): # use front surface as LEFT also
					for i in range(2):
						uv_left.append(uv_front[i]) # only contains two texels
					uv_left.append(tx(uv_front[2].u, uv_front[2].v)) # add the third texel
					uv_left.append(uv_front[2]) # add the fourth texel
					uv_left[2].u = uv_front[2].u+uv_front[1].u-uv_front[0].u
					uv_left[2].v = uv_front[2].v+uv_front[1].v-uv_front[0].v
					exist_left = True
				else:
					print "Left surface wanna copy from right or front, BUT Fail !!!"
		# Invent right surface is not exist. (front, left already exist here)
		if(exist_right == False):
			if(exist_left): # use right surface as RIGHT also
				for i in uv_left:
					uv_right.append(i)
				exist_right = True
			else :
				if(exist_front): # use front surface as RIGHT also
					for i in range(2):
						uv_left.append(uv_front[i]) # only contains two texels
					uv_left.append(tx(uv_front[2].u, uv_front[2].v)) # add the third texel
					uv_left.append(uv_front[2]) # add the fourth texel
					uv_left[2].u = uv_front[2].u+uv_front[1].u-uv_front[0].u
					uv_left[2].v = uv_front[2].v+uv_front[1].v-uv_front[0].v
					exist_right = True
				else:
					print "Right surface wanna copy from left or front, BUT Fail !!!"
		# # Invent btm surface
		# if(exist_left):
		# 	for i in uv_left:
		# 		uv_btm.append(i)
		# else:
		# 	print "Bottom surface wanna copy from left, BUT Fail !!!"
		# # Invent back surface
		# if(exist_front):
		# 	for i in uv_front:
		# 		uv_back.append(i)
		# else:
		# 	print "Back surface wanna copy from front, BUT Fail !!!"


		#-------------------------------------------------------
		# Generate polygons
		#poly1 = Polygon([ver1, ver2, ver3, ver4], uv_btm)
		poly2 = Polygon([ver1, ver2, ver5], uv_front)
		poly3 = Polygon([ver2, ver3, ver6, ver5], uv_right)
		#poly4 = Polygon([ver3, ver4, ver6], uv_back)
		poly5 = Polygon([ver4, ver1, ver5, ver6], uv_left)
		

		#-------------------------------------------------------
		# Return list of polygons
		polyList = [poly2, poly3, poly5]
		return polyList



	###########################################################
	# Build tree
	###########################################################	
	def BuildTree (self, center, height, faces):
		# Generate vertices
		# cx = center[0]
		# cy = center[1]
		# cz = center[2]
		# # V1 on bot, v1 on top, v3-v6 on side
		# v1 = vt(cx, cy, cz)
		# v2 = vt(cx, cy+height, cz)
		# v3 = vt()

		# Generate texels

		# Generate polygon 

		# Generate polygon list and return

		return 1



	###########################################################
	# Build Functions called by GUI to build 3D models.
	###########################################################	
	def BuildModel (self, model):
		if(isinstance(model, Cuboid)):
			print "Model's type is Cuboid"
			return self.BuildCuboid(model.center, model.length, model.width, model.height, model.faces)
		elif(isinstance(model, Cylinder)):
			print "Model's type is Cylinder"
			return self.BuildCylinder(model.center, model.radius, model.height, model.faces)
		elif(isinstance(model, Ground)):
			print "Model's type is Ground"
			return self.BuildPlane(0, model.faces)
		elif(isinstance(model, Sky)):
			print "Model's type is Sky"
			return self.BuildPlane(400, model.faces)
		elif(isinstance(model, Frustum)):
			print "Model's type is Frustum"
			return self.BuildFrustum(model.center, model.lowerLength, model.lowerWidth, model.upperLength, model.upperWidth, model.height, model.faces)
		elif(isinstance(model, Prism)):
			print "Model's type is Prism"
			return self.BuildPrism(model.center, model.length, model.width, model.height, model.faces)
		elif(isinstance(model, Tree)):
			print "Model's type is Tree"
			#return self.BuildTree(model.center, model.height, model.faces)
		else :
			print "Model's type is Wrong..."