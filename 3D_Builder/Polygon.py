# CS4243: Computer Vision and Pattern Recognition
# Zhou Bin
# 29th, Oct, 2014

import numpy as np
from Vertex import Vertex

class Polygon:
	
	def __init__(self, newVertexList, newTexelList):
		# Create list to store all vertex
		self.VertexList = []
		for i in newVertexList:
			self.VertexList.append(i)
			
		# Create list to store all texel value
		self.TexelList = []
		for i in newTexelList:
			self.TexelList.append(i)
			