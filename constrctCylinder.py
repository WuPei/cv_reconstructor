import math
import numpy as np

fileRGB = open("cylinderRGB.dat","w+")
fileP = open("cylinder.dat","w+")

height = 200
radius = 100
pi = np.pi
n = 60
m = 100
unit_radian = 2.0*pi/n
unitHeight = 1.0*height/m;

offset_u = 0
offset_v = 0

#draw the bottom circle
for i in range(n):
	theta = i*unit_radian
	point = "{0},{1},{2},{r},{g},{b}\n".format(radius*math.cos(theta)+radius,radius*math.sin(theta)+radius,0,r='255',g='255',b='255')
	fileRGB.write(point)

#draw the middle part(mesh)
for i in range(m):
	for j in range(n):
		theta = j*unit_radian
		point1 = "{0},{1},{2},{r},{g},{b}\n".format(radius*math.cos(theta)+radius,radius*math.sin(theta)+radius,i*unitHeight,r='255',g='255',b='255')
		fileRGB.write(point1)

for i in range(n):
	theta = i*unit_radian
	point = "{0},{1},{2},{r},{g},{b}\n".format(radius*math.cos(theta)+radius,radius*math.sin(theta)+radius,height,r='255',g='255',b='255')
	fileRGB.write(point)

fileRGB.close()
fileP.close()