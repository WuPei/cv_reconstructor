import fileManager as fm
import camera
import numpy as np
import cv2

file = fm.FileManager("cylinderRGB.dat")
points,rgb_values = file.importPointsWithRGB()

camera_pos = [0,100,100,100] #(0,0,-200) as initial position
I = [[1,0,0],[0,1,0],[0,0,1]]
camera_ori = np.matrix(I)

width = 800
height = 600

offset_u = width/2
offset_v = height/2
focalLength = 1
cam = camera.Camera(points,camera_pos,camera_ori,focalLength)
y_axis = [0,1,0]
x_axis = [1,0,0]
cam.rotateCamera(y_axis,0)

x_cord, y_cord = cam.getProjectedPts(height,width)

blank_image = np.zeros((width,height,3),np.uint8)

for x in range(len(points)):
	u_fp = x_cord[x]
	v_fp = y_cord[x]
	#move the projected image to the center of image
	if (u_fp+offset_u) >= width or (v_fp+offset_v) >=height or (u_fp+offset_u)<0 or (v_fp+offset_v)<0:
		continue
	rgb = rgb_values[x]
	blank_image[u_fp+offset_u][v_fp+offset_v] = rgb

cv2.imwrite("test1.jpg",blank_image)
