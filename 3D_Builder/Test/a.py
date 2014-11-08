# CS4243: Computer Vision and Pattern Recognition
# Zhou Bin
# 29th, Oct, 2014

import os
import sys
# import b
import cv2
from Vertex import Vertex
from texture import Texture
from ModelBuilder import ModelBuilder
from texture import Point

'''
print "Initial and call vertex operations..."
v = Vertex(1,2,3)
v3 = Vertex.equal(v)
v.x = 10
print "v equal after: ", v.x, v.y, v.z
print "v3 equal b4: ", v3.x, v3.y, v3.z

v2 = Vertex(1,2,3)
v3 = Vertex.sum(v, v2)
print "v3 sum: ", v3.x, v3.y, v3.z

v3 = Vertex.diff(v, v2)
print "v3 diff: ",v3.x, v3.y, v3.z

v = Vertex(1,0,0)
v2 = Vertex(0,1,0)
v3 = Vertex.cross(v, v2)
print "v3 cross: ",v3.x, v3.y, v3.z

v3 = Vertex.distance(v, v2)
print "v3 distance: ",v3

v = Vertex(1, 2, 3)
v3 = Vertex.normalize(v)
print "v3 normalize: ",v3.x, v3.y, v3.z

v3 = Vertex.scale(v, 2)
print "v3 scale: ",v3.x, v3.y, v3.z


print "Testing ModelBuilder.py"
mb = ModelBuilder()

print "verifying polygons for cuboid"
temp = mb.BuildCuboid(Vertex(0,0,1),Vertex(1,0,1), Vertex(0,1,1), Vertex(0,0,0))
for i in temp:
	vlst = i.VertexList
	for j in vlst:
		print "i, j:", j.x, j.y, j.z'''

'''print "verifying polygons for cynlinder"
temp = mb.BuildCylinder(Vertex(0,0,0),Vertex(0,0,1), Vertex(0,1,0))
for i in temp:
	vlst = i.VertexList
	print "another polygon:"
	for j in vlst:
		print "i, j:", j.x, j.y, j.z
		
print "Verifying polygonsn for frustum"
temp = mb.BuildFrustum(Vertex(-2,0,2),Vertex(2,0,2), Vertex(-1,1,1), Vertex(-2,0,-2))
for i in temp:
	vlst = i.VertexList
	print "another polygon:"
	for j in vlst:
		print "i, j:", j.x, j.y, j.z'''

mb = ModelBuilder()
UVs = [[200, 200], [200, 300], [300, 500], [300, 150], [200, 200], [200, 300], [300, 500], [300, 150], [200, 200],
       [200, 300], [300, 500], [300, 150], [200, 200], [200, 300], [300, 500], [300, 150], [200, 200], [200, 300],
       [300, 500], [300, 150], [200, 200], [200, 300], [300, 500], [300, 150]]
cube = mb.BuildCuboid(Vertex(0, 0, 1), Vertex(1, 0, 1), Vertex(0, 1, 1), Vertex(0, 0, 0), UVs)
for i in cube:
    vlst = i.Vertex
    for j in vlst:
        print "i, j:", j.x, j.y, j.z
    tlst = i.Texel
    for j in tlst:
        print "u, v:", j.u, j.v

texture = Texture(cv2.imread('project.jpeg', cv2.CV_LOAD_IMAGE_COLOR))
points = []
for i in range(len(cube)):
    points.append(texture.putTexture(cube[i]))

print points	
		
	
