import fileManager as fm
import camera
import videoMaker as vmaker
import numpy as np
import cv2
from random import shuffle
import shader as pts_shader
import os 
import timeit
import math


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
	return [x for (y,x) in sorted(zip(z_cords,mylist),key = lambda pair:pair[0],reverse = True)]

def generateImg(file,width,length,cam_pos,cam_ori):
	files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
	count = 0
	previous_img = cv2.imread(skyDir,cv2.CV_LOAD_IMAGE_COLOR)
	for x in range(len(files)-1):
		filename = os.path.join(dir,"model_"+str(x)+".dat")
		print filename
		if x==0:
			continue
		points, rgb_values = file.importPointsWithRGB(filename)	

		#STORE EACH FOUR PONITS INTO A MESH 

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

def theta(angle):
	return angle * 1.0 / 180 * np.pi

def rotateThroughX(angle):
	return [[math.cos(theta(angle)), 0, math.sin(theta(angle))], [0, 1, 0], [math.cos(theta(angle+90)), 0, math.sin(theta(angle+90))]]

def rotateThroughY(angle):
	return [[1,0, 0], [0, math.cos(theta(angle)), math.sin(theta(angle))], [0, math.cos(theta(angle+90)), math.sin(theta(angle+90))]]

def generatePath1(start_pos,start_angle,final_pos,final_angle,frames):
	start_ori = rotateThroughX(start_angle)
	for i in range(1,frames+1):
		factor = i*1.0/20
		x =(final_pos[1]-start_pos[1])*factor + start_pos[1]
		y =(final_pos[2]-start_pos[2])*factor + start_pos[2]
		z =(final_pos[3]-start_pos[3])*factor + start_pos[3]
		camera_pos = [0,x,y,z]
		angle = (final_angle- start_angle)*factor + start_angle
		camera_ori = rotateThroughX(angle)
		print i
		print camera_pos
		print camera_ori
		#generateImg(file,width,height,camera_pos,camera_ori)

def generatePath2(start_pos,start_angle,final_pos,final_angle,frames):
	start_ori = rotateThroughY(start_angle)
	for i in range(1,frames+1):
		factor = i*1.0/20
		x =(final_pos[1]-start_pos[1])*factor + start_pos[1]
		y =(final_pos[2]-start_pos[2])*factor + start_pos[2]
		z =(final_pos[3]-start_pos[3])*factor + start_pos[3]
		camera_pos = [0,x,y,z]
		angle = (final_angle- start_angle)*factor + start_angle
		camera_ori = rotateThroughY(angle)
		print i
		print camera_pos
		print camera_ori
		#generateImg(file,width,height,camera_pos,camera_ori)

def generatePath3(cam_ori,start_pos,final_pos,frames):
	for i in range(1,frames+1):
		factor = i*1.0/20
		x =(final_pos[1]-start_pos[1])*factor + start_pos[1]
		y =(final_pos[2]-start_pos[2])*factor + start_pos[2]
		z =(final_pos[3]-start_pos[3])*factor + start_pos[3]
		camera_pos = [0,x,y,z]
		print i
		print camera_pos
		print cam_ori
		#generateImg(file,width,height,camera_pos,camera_ori)

width = 1632
height = 1224
file = fm.FileManager()
#points, rgb_values = file.importPointsWithRGB()
# points,rgb_values = shuffleTwoLists(points,rgb_values)
dir = 'testData/Models/'
outDir = "testData/imgs/"
skyDir = "sky.png"

pos_1 = [0, 0, 0, -500]  # (500,100,100) as initial position
angle_1x = -45

pos_2 = [0,400,0,-500]
angle_2x = 45

pos_3 = [0,200,0,-500]
angle_3x = 0
angle_3y = 0

pos_4 = [0,200,30,-500]
angle_4y = -45

pos_5 = [0,200,30,-200]

frames=60
#left&right
print "Path1"
generatePath1(pos_1,angle_1x,pos_2,angle_2x,2*frames)
print "Path2"
generatePath1(pos_2,angle_2x,pos_3,angle_3x,frames)

#camera up, and rotate to see ground
#camera down, rotate to I
print "Path3"
generatePath2(pos_3,angle_3y,pos_4,angle_4y,frames)
print "Path4"
generatePath2(pos_4,angle_4y,pos_3,angle_3y,frames)

#go stright
I = [[1,0,0],[0,1,0],[0,0,1]]
print "Path5"
generatePath3(I, pos_3,pos_5, frames)







#print "-----points plotted-----------------"
# out_img_point = shader.plotPoints(rgb_values)
# cv2.imwrite("points.png", out_img_point)
