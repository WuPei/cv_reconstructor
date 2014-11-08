# CS4243: Computer Vision and Pattern Recognition
# Zhou Bin
# 29th, Oct, 2014

import numpy as np
from Vertex import Vertex


class Polygon:
    def __init__(self, newVertexList, newTexelList):
        # Create list to store all vertex
        self.Vertex = []
        for i in newVertexList:
            self.Vertex.append(i)

        # Create list to store all texel value
        self.Texel = []
        for i in newTexelList:
            self.Texel.append(i)
			