import math
import numpy as np
import matplotlib.pyplot as plt

file = open("cylinder.dat","w+")

height = 200
radius = 100
pi = np.pi
n = 60
m = 100
unit_radian = 2.0*pi/n
unitHeight = 1.0*height/m;

offset_u = 400
offset_v = 400

#draw the bottom circle
for i in range(n):
	theta = i*unit_radian
	point = "{0},{1},{2},{r},{g},{b}\n".format(radius*math.cos(theta)+offset_u,radius*math.sin(theta)+offset_v,0,r='255',g='255',b='255')
	file.write(point)

#draw the middle part(mesh)
for i in range(m):
	for j in range(n):
		theta = j*unit_radian
		point1 = "{0},{1},{2},{r},{g},{b}\n".format(radius*math.cos(theta)+offset_u,radius*math.sin(theta)+offset_v,i*unitHeight,r='255',g='255',b='255')
		file.write(point1)

for i in range(n):
	theta = i*unit_radian
	point = "{0},{1},{2},{r},{g},{b}\n".format(radius*math.cos(theta)+offset_u,radius*math.sin(theta)+offset_v,height,r='255',g='255',b='255')
	file.write(point)

file.close()