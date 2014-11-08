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


file = fm.FileManager("testData/cylinderRGB.dat")
points, rgb_values = file.importPointsWithRGB()
# points,rgb_values = shuffleTwoLists(points,rgb_values)
width = 800
height = 600
y_axis = [0, 1, 0]
x_axis = [1, 0, 0]

#initial camera
camera_pos = [0, 0, 0, 1000]  #(500,100,100) as initial position
I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
camera_ori = np.matrix(I)
cam = camera.Camera(points, camera_pos, camera_ori, 1)

#intialize the frames
num_frame = 30

vm = vmaker.VideoMaker(num_frame, width, height, cam, rgb_values)

vm.generateVideo()
