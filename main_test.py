import fileManager as fm
import camera
import videoMaker as vmaker
import numpy as np
import cv2
from random import shuffle
import shader as pts_shader
import os 
import timeit
from texture import Mesh


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

def sortBasedOnZ(mylist,refer_list):
	return [x for (y,x) in sorted(zip(refer_list,mylist),key = lambda pair:pair[0],reverse = False)]

width = 1632
height = 1224
y_axis = [0, 1, 0]
x_axis = [1, 0, 0]
file = fm.FileManager()
#points, rgb_values = file.importPointsWithRGB()
# points,rgb_values = shuffleTwoLists(points,rgb_values)
dir = 'testData/Models/'
outDir = "testData/imgs/"
skyDir = "sky.png"

files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
count = 0
previous_img = cv2.imread(skyDir,cv2.CV_LOAD_IMAGE_COLOR)
for x in range(len(files)-1):
	filename = os.path.join(dir,"model_"+str(x)+".dat")
	print filename
	if x==0:
		continue
	points, rgb_values = file.importPointsWithRGB(filename)	

	camera_pos = [0, 0, 0, -400]  # (500,100,100) as initial position
	I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
	camera_ori = np.matrix(I)

	#STORE EACH FOUR PONITS INTO A MESH
	meshlist = []
	meshz = []
	for i in range(0, len(points), 4):
		mesh = Mesh([points[i], points[i+1], points[i+2], points[i+3]], [rgb_values[i], rgb_values[i+1], rgb_values[i+2], rgb_values[i+3]])
		meshlist.append(mesh)
		meshz.append(mesh.getZ(camera_pos))
	#Sort Meshes
	meshlist = sortBasedOnZ(meshlist, meshz)

	#Mesh back to points
	points = []
	rgb_values = []
	for i in range(len(meshlist)):
		p1, p2, p3, p4 = meshlist[i].getPoints()
		c1, c2, c3, c4 = meshlist[i].getColors()
		points.append(p1)
		points.append(p2)
		points.append(p3)
		points.append(p4)
		rgb_values.append(c1)
		rgb_values.append(c2)
		rgb_values.append(c3)
		rgb_values.append(c4)

	cam = camera.Camera(points, camera_pos, camera_ori, 1)
	start = timeit.default_timer()
	x_cords, y_cords ,z_cords = cam.getProjectedPts(height, width)
	#x_cords, y_cords ,z_cords = cam.getOrthProjectPts(height, width)

	shader = pts_shader.Shader( width, height,previous_img)
	print "----projected poitns generated-----"
	out_img = shader.shading(x_cords,y_cords,rgb_values)
	print "Processing Time:", timeit.default_timer()-start,"s"
	print "-----points shaded------------------"
	cv2.imwrite(os.path.join(outDir,"img_"+str(x)+".png"),out_img)
	#out_points = shader.plotPoints(x_cords, y_cords,rgb_values)
	#cv2.imwrite(os.path.join(outDir,"points_"+str(x)+".png"),out_points)
	print "---img_"+str(x)+".png created!"
	previous_img = out_img


cv2.imwrite(os.path.join(outDir,"result.png"),previous_img)
#print "-----points plotted-----------------"
# out_img_point = shader.plotPoints(rgb_values)
# cv2.imwrite("points.png", out_img_point)
