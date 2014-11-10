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
file = fm.FileManager("testData/test.dat")
#points, rgb_values = file.importPointsWithRGB()
# points,rgb_values = shuffleTwoLists(points,rgb_values)
dir = 'testData/Models/'
outDir = "testData/imgs/"
files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
count = 0
for x in range(len(files)):
	file.filename = os.path.join(dir,"model_"+str(x)+".dat")
	print file.filename
	points, rgb_values = file.importPointsWithRGB()	
	camera_pos = [0, 0, 0, -400]  # (500,100,100) as initial position
	I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
	camera_ori = np.matrix(I)
	cam = camera.Camera(points, camera_pos, camera_ori, 1)
	start = timeit.default_timer()
	x_cords, y_cords ,z_cords = cam.getProjectedPts(height, width)
	print "----projected poitns generated-----"
	shader = pts_shader.Shader(x_cords, y_cords, width, height)
	out_img = shader.shading(rgb_values)
	print "Processing Time:", timeit.default_timer()-start,"s"
	print "-----points shaded------------------"
	#cv2.imwrite(os.path.join(outDir,"img_"+str(count)+".png"),out_img)
	print "---img_"+str(count)+".png created!"
	count+=1

cv2.imwrite(os.path.join(outDir,"result.png"),out_img)
# for f in files:
# 	if f != ".DS_Store":
# 		print f

		#file.saveProjectedPointsWithRGB(x_cords,y_cords,rgb_values)
	# else:
	# 	continue

#print "-----points plotted-----------------"
# out_img_point = shader.plotPoints(rgb_values)
# cv2.imwrite("points.png", out_img_point)
