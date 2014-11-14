import fileManager as fm
import camera
import numpy as np
import cv2
import shader as pts_shader
import os 
import timeit
from texture import Mesh
from SortBuilding import SortBuilding as sb
import math

def sortBasedOnZ(mylist,refer_list):
	return [x for (y,x) in sorted(zip(refer_list,mylist),key = lambda pair:pair[0],reverse = False)]


def sortMeshes(points,rgb_values,camera_pos):
	#STORE EACH FOUR PONITS INTO A MESH
	print "-----start sorting the meshes for frame:"+str(t)+"------" 
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
	return points,rgb_values

def generate1stPath(frame_num):
	cam_pos = [camera_pos for x in range(frame_num)]
	cam_ori = [camera_ori for x in range(frame_num)]
	for each_angle in range(frame_num):
		cam = camera.Camera(points, camera_pos, camera_ori, 1)
		cam.rotateCamera(y_axis,-37.2+each_angle*1*37.2/56)
		theta = each_angle*1.0/180*np.pi
		alpha = math.atan(200.0/300)
		beta= alpha + theta 
		R = 300.0/math.cos(alpha)
		cam_ori[each_angle] = cam.ori_mat
		cam_pos[each_angle] = [0,300-R*math.cos(beta),0,-R*math.sin(beta)]
		#print "x,z",300-R*math.cos(beta),-R*math.sin(beta)
	return cam_pos,cam_ori

def generate2ndPath(frame_num):
	camera_pos = [0, 300, 0, -200]
	cam_pos = [camera_pos for x in range(frame_num)]
	cam_ori = [camera_ori for x in range(frame_num)]
	for each_angle in range(frame_num):
		cam = camera.Camera(points, camera_pos, camera_ori, 1)
		cam.rotateCamera(x_axis,-each_angle*1*42.6/180)
		theta = each_angle*2.0/180*np.pi
		R = 200.0
		cam_ori[each_angle] = cam.ori_mat
		cam_pos[each_angle] = [0,300,(200-R*math.cos(theta)),-200-R*math.sin(theta)]
	return cam_pos,cam_ori

width = 1632
height = 1224
y_axis = [0, 1, 0]
x_axis = [1, 0, 0]
file = fm.FileManager()
dir = 'testData/Models/'
outDir = "testData/imgs/"
skyDir = "sky.png"

frame_num = 90
#90 for 2nd path
#112 for 1st path 
previous_img = [cv2.imread(skyDir,cv2.CV_LOAD_IMAGE_COLOR) for i in range(frame_num)]
camera_pos = [0, 0, 0, -200]
I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
camera_ori = np.matrix(I)
points = []
sort_build = sb()
result = sort_build.SortBuildings(camera_pos)

sorted_models = [x for [x,y] in result]
print "sorted models:",sorted_models

#cam_pos,cam_ori = generate1stPath(frame_num)
cam_pos,cam_ori = generate2ndPath(frame_num)
mode = 1 

init = 0
end = frame_num

print "initial:",init,"end:",end
for t in range(init,end):	
	for index in range(len(sorted_models)):
		if index ==0:
			continue
		fileindex = sorted_models[index]
		filename = os.path.join(dir,"model_"+str(fileindex)+".dat")
		print filename
		points, rgb_values = file.importPointsWithRGB(filename)	

		start = timeit.default_timer()
		#sort the points based on meshes
		points, rgb_values = sortMeshes(points,rgb_values,cam_pos[t])
		#create the camera
		cam = camera.Camera(points, cam_pos[t], cam_ori[t], 1)				
		print "----------get projected points-------------"
		x_cords, y_cords ,z_cords = cam.getProjectedPts(height, width)
		#shading the projected points 
		shader = pts_shader.Shader(width, height,previous_img[t])
		print "----projected poitns generated-----"
		out_img = shader.shading(x_cords,y_cords,rgb_values,mode)
		print "Processing Time:", timeit.default_timer()-start,"s"
		print "-----points shaded------------------"
		#write all the middle frames
		cv2.imwrite(os.path.join(outDir,"frame_"+str(t)+"_img_"+str(index)+".png"),out_img)

		print "---img_"+str(t)+"_frame_"+str(index)+".png created!"
		previous_img[t] = out_img

#this main file is used to create the middle frames, for creating a video, please use makingVideoMain
for i in range(init,end):
	cv2.imwrite(os.path.join(outDir,"result_"+str(i)+".png"),previous_img[i])

print "------------Main Part Finished------------"
print "--All Results has been output, please use makingVideoMain.py to generate a video--"
