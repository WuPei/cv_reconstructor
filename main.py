import fileManager as fm
import camera
import numpy as np
import cv2

def ImgsFromCamPath(cam,axis,angle,times,width,height):
	offset_u = width/2
	offset_v = height/2
	for i in range(times):
		cam.translateCameraWithAxisAngle(axis,angle)
		cam.rotateCamera(axis,-angle)
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

		#cv2.imwrite("test1.jpg",blank_image)
		cv2.imshow("test.jpg",blank_image)
		cv2.waitKey(100)
	cv2.destroyAllWindows()


file = fm.FileManager("cylinderRGB.dat")
points,rgb_values = file.importPointsWithRGB()

width = 800
height = 600
y_axis = [0,1,0]
x_axis = [1,0,0]

#initial camera
camera_pos = [0,0,0,1000] #(500,100,100) as initial position
I = [[1,0,0],[0,1,0],[0,0,1]]
camera_ori = np.matrix(I)
cam = camera.Camera(points,camera_pos,camera_ori,1)

ImgsFromCamPath(cam,y_axis,10,18,width,height)