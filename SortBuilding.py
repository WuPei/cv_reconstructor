'''

This file provides a method for sorting all buildings based on 
the distance between camera and all buildings.

'''
import math

class SortBuilding:

	def __init__ (self):
		# camera_pos is a list containing x,y,z; like [0,0,1]
		#self.camera_pos = camera_pos 
		
		# Positions of all buildings; there are two versions.
		# Version 1: each model as one element. (one building contains >=1 models)
		# Versoin 2: each building as one element. 
		self.buildings = [] # total number should be 20 (excluding ground)
		# for now, only combine building 9 and 8; others, roof and body are still separate		
		self.buildings.append([550,0,250]) #B13
		self.buildings.append([330,0,330]) #B12
		self.buildings.append([0,0,280]) #B11
		self.buildings.append([470,0,180]) #B4
		self.buildings.append([-20,0,60]) #B10
		#self.buildings.append([-20,25,50]) #B10_roof
		self.buildings.append([330,0,235]) #B9
		self.buildings.append([200,0,260]) #B8
		self.buildings.append([50,0,190]) #B7
		#self.buildings.append([50,30,190]) #B7_roof
		self.buildings.append([200,0,150]) #B6
		#self.buildings.append([200,30,150]) #B6_roof
		self.buildings.append([330,0,180]) #B5
		#self.buildings.append([330,25,180]) #B5_roof
		self.buildings.append([580,0,180]) #B3
		#self.buildings.append([580,25,180]) #B3_roof
		self.buildings.append([600,0,110]) #B2
		#self.buildings.append([600,30,110]) #B2_roof
		self.buildings.append([600,0,50]) #B1
		#self.buildings.append([600,30,50]) #B1_roof
		
		
		self.models = [] # total number should be 26 (excluding ground)
		self.models.append([550,0,250]) #B13        0
		self.models.append([330,0,330]) #B12        1
		self.models.append([0,0,280]) #B11   2
		self.models.append([-20,0,60]) #B10_body    3
		self.models.append([-20,25,50]) #B10_roof    4
		self.models.append([300,0,260]) #B9_c       5
		self.models.append([330,0,235]) #B9_b     6
		self.models.append([310,0,235]) #B9_a          7
		self.models.append([370,0,235]) #B9_f          8
		self.models.append([330,140,280]) #B9_d        9
		self.models.append([330,170,280]) #B9_e       10 
		self.models.append([200,0,260]) #B8_body      11
		self.models.append([200,120,260]) #B8_top     12
		self.models.append([50,0,190]) #B7_body       13
		self.models.append([50,30,190]) #B7_roof      14 
		self.models.append([200,0,150]) #B6_body      15
		self.models.append([200,30,150]) #B6_roof     16
		self.models.append([330,0,180]) #B5_body      17
		self.models.append([330,25,180]) #B5_roof     18
		self.models.append([580,0,180]) #B3_body      19
		self.models.append([580,25,180]) #B3_roof     20 
		self.models.append([470,0,180]) #B4           21 
		self.models.append([600,0,110]) #B2_body      22
		self.models.append([600,30,110]) #B2_roof     23
		self.models.append([600,0,50]) #B1_body       24
		self.models.append([600,30,50]) #B1_roof      25
		
		
	# --------------------------------------------------
	# Conmpute the distance between two vertices. (can be 2D, 3D, etc.)
	# --------------------------------------------------
	def ComputeDistance(self, pos1, pos2):
		if(len(pos1) != len(pos2)):
			print "Cannot Compute distance of two different size lists."
			return 
			
		distance = 0
		for i in range(len(pos1)):
			distance += (pos1[i] - pos2[i]) ** 2
		return math.sqrt(distance)
		
	
	# --------------------------------------------------
	# Sort buildings/models based on distance
	# --------------------------------------------------	
	def SortBuildings(self, camera_pos):
		camera_pos = [camera_pos[1],camera_pos[2],camera_pos[3]]
		# Compute Distance
		distance = []
		for i in range(len(self.buildings)):
			distance.append([i+1, self.ComputeDistance(self.buildings[i], camera_pos)])
			
		# Sort distance 
		sorted_dist = sorted(distance, key=lambda tup:tup[1])
		sorted_dist.append([0,1000])
		# Test
		for i in sorted_dist:
			print "index is: ", i[0], "  --------- distance is: ", i[1]
		
		#reverse the order of this array
		return sorted_dist[::-1]
		
	def SortModels(self, camera_pos):
		# Compute Distance
		distance = []
		for i in range(len(self.models)):
			distance.append([i, self.ComputeDistance(self.models[i], camera_pos)])
		
		# Sort distance 
		sorted_dist = sorted(distance, key=lambda tup:tup[1])
		
		# Test
		for i in sorted_dist:
			print "index is: ", i[0], "  --------- distance is: ", i[1]
		
		return sorted_dist		