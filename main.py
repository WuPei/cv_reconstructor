import fileManager as fm
import camera
import videoMaker as vmaker
import numpy as np
import cv2
from random import shuffle


def shuffleTwoLists(list1, list2):
    list1_shuf = []
    list2_shuf = []
    index_shuf = range(len(list1))
    shuffle(index_shuf)
    for i in index_shuf:
        list1_shuf.append(list1[i])
        list2_shuf.append(list2[i])
    return list1_shuf, list2_shuf


file = fm.FileManager("testData/test.dat")
points, rgb_values = file.importPointsWithRGB()
# points,rgb_values = shuffleTwoLists(points,rgb_values)
width = 1632
height = 1224
y_axis = [0, 1, 0]
x_axis = [1, 0, 0]

# initial camera
camera_pos = [0, width/2, height/2, 700]  #(500,100,100) as initial position
I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
camera_ori = np.matrix(I)
cam = camera.Camera(points, camera_pos, camera_ori, 1)

x_cords, y_cords = cam.getProjectedPts(height, width)
print "projected image finished/n"
out_img = np.zeros((width, height, 3), np.uint8)

for i in range(0, len(x_cords), 4):
            point = [0 for index in range(4)]
            print "x,y",len(x_cords),len(y_cords)
            if i+3 > len(x_cords):
            	continue
            else:
            	for j in range(4):
	                x = x_cords[i + j]
	                y = y_cords[i + j]
	                point[j] = [x, y]
            pts = np.array([point[0], point[1], point[3], point[2]], np.int32)
            print  pts
            #get average color from four points
            average_color = (rgb_values[i] + rgb_values[i + 1] + rgb_values[i + 2] + rgb_values[i + 3]) / 4
            #shading using fillPoly with average color
            cv2.fillPoly(out_img, [pts], average_color)

cv2.imshow("img",out_img)
cv2.imwrite("test.png",out_img)
#intialize the frames
num_frame = 30

#vm = vmaker.VideoMaker(num_frame, width, height, cam, rgb_values)

#vm.generateVideo()
