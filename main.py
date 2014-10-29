import fileManager as fm
import camera
import numpy as np
import cv2
from random import shuffle

def shuffleTwoLists(list1,list2):
	list1_shuf = []
	list2_shuf = []
	index_shuf = range(len(list1))
	shuffle(index_shuf)
	for i in index_shuf:
	    list1_shuf.append(list1[i])
	    list2_shuf.append(list2[i])
	return list1_shuf,list2_shuf

def ImgsFromCamPath(cam,axis,angle,num_frame,width,height,frames):
	offset_u = width/2
	offset_v = height/2
	for i in range(num_frame):
		cam.translateCameraWithAxisAngle(axis,angle)
		cam.rotateCamera(axis,-angle)
		x_cord, y_cord = cam.getProjectedPts(height,width)

		each_frame = np.zeros((width,height,3),np.uint8)

		# for x in range(len(points)):
		# 	u_fp = x_cord[x]
		# 	v_fp = y_cord[x]
		# 	#move the projected image to the center of image
		# 	if (u_fp+offset_u) >= width or (v_fp+offset_v) >=height or (u_fp+offset_u)<0 or (v_fp+offset_v)<0:
		# 		continue
		# 	rgb = rgb_values[x]
		# 	each_frame[u_fp+offset_u][v_fp+offset_v] = rgb
		# frames[i] = each_frame
		
		for x in range(0,len(points),4):
			
			u_fp = x_cord[x]
		 	v_fp = y_cord[x]
			
			if (u_fp+offset_u) >= width or (v_fp+offset_v) >=height or (u_fp+offset_u)<0 or (v_fp+offset_v)<0:
	 			continue
	 		point = [0 for index in range(4)]
	 		for j in range(4):
	 			point[j] = [y_cord[x+j]+offset_v,x_cord[x+j]+offset_u,]
			pts = np.array([point[0],point[1],point[3],point[2]],np.int32)
			average_color = (rgb_values[x]+rgb_values[x+1]+rgb_values[x+2]+rgb_values[x+3])/4
			cv2.fillPoly(each_frame,[pts],average_color)
			#print each_frame
		frames[i] = each_frame


def generateVideo(width,height,frames):
	fps = 15
	capSize = (height,width)
	fourcc = cv2.cv.CV_FOURCC('m','p','4','v')
	writer = cv2.VideoWriter()
	success = writer.open("output1.mov",fourcc,fps,capSize,True)
	if success:
		for x in range(len(frames)):
			writer.write(frames[x])
		writer.release()


file = fm.FileManager("cylinderRGB.dat")
points,rgb_values = file.importPointsWithRGB()
points,rgb_values = shuffleTwoLists(points,rgb_values)
width = 800
height = 600
y_axis = [0,1,0]
x_axis = [1,0,0]

#initial camera
milisec_for_each_frame = 39
camera_pos = [0,0,0,1000] #(500,100,100) as initial position
I = [[1,0,0],[0,1,0],[0,0,1]]
camera_ori = np.matrix(I)
cam = camera.Camera(points,camera_pos,camera_ori,1)

#intialize the frames
num_frame = 30
blank_image = np.zeros((width,height,3),np.uint8)
frames = [blank_image for x in range(num_frame)]



ImgsFromCamPath(cam,y_axis,10,num_frame,width,height,frames)

generateVideo(width,height,frames)

