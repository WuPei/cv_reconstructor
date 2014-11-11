import fileManager as fm
import camera
import videoMaker as vmaker
import numpy as np
import cv2
from random import shuffle
import shader as pts_shader
import os 
import timeit


def uniqfiy(seq, rgb_values,idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   rgbs = []
   count = -1
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       count+=1
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
       rgbs.append(rgb_values[count])
       
   return result,rgbs

def sortBasedOnZ(mylist,z_cords):
	return [x for (y,x) in sorted(zip(z_cords,mylist),key = lambda pair:pair[0])]

width = 1632
height = 1224
y_axis = [0, 1, 0]
x_axis = [1, 0, 0]
file = fm.FileManager()
#points, rgb_values = file.importPointsWithRGB()
# points,rgb_values = shuffleTwoLists(points,rgb_values)
dir = 'testData/Models/'
outDir = "testData/imgs/"
files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
count = 0

for x in range(len(files)-1):
	filename = os.path.join(dir,"model_"+str(x)+".dat")
	print filename
	if x ==0 :
		continue
	points, rgb_values = file.importPointsWithRGB(filename)	
	camera_pos = [0, 0, 0, -400]  # (500,100,100) as initial position
	I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
	camera_ori = np.matrix(I)
	cam = camera.Camera(points, camera_pos, camera_ori, 1)
	start = timeit.default_timer()
	x_cords, y_cords ,z_cords = cam.getProjectedPts(height, width)
	shader = pts_shader.Shader( width, height)
	print "----projected poitns generated-----"
	out_img = shader.shading(x_cords,y_cords,rgb_values)
	print "Processing Time:", timeit.default_timer()-start,"s"
	print "-----points shaded------------------"
	cv2.imwrite(os.path.join(outDir,"img_"+str(x)+".png"),out_img)
	#out_points = shader.plotPoints(x_cords, y_cords,rgb_values)
	#cv2.imwrite(os.path.join(outDir,"points_"+str(x)+".png"),out_points)
	print "---img_"+str(x)+".png created!"
	result = out_img


cv2.imwrite(os.path.join(outDir,"result.png"),result)
#print "-----points plotted-----------------"
# out_img_point = shader.plotPoints(rgb_values)
# cv2.imwrite("points.png", out_img_point)
