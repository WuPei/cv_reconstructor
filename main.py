import fileManager as fm
import camera
import videoMaker as vmaker
import numpy as np
import cv2
from random import shuffle
import shader as pts_shader

def shuffleTwoLists(list1, list2):
    list1_shuf = []
    list2_shuf = []
    index_shuf = range(len(list1))
    shuffle(index_shuf)
    for i in index_shuf:
        list1_shuf.append(list1[i])
        list2_shuf.append(list2[i])
    return list1_shuf, list2_shuf

# initial camera

width = 1632
height = 1224
y_axis = [0, 1, 0]
x_axis = [1, 0, 0]
file = fm.FileManager("testData/test.dat")
#points, rgb_values = file.importPointsWithRGB()
# points,rgb_values = shuffleTwoLists(points,rgb_values)

if file.importProjectedPoints():
    x_cords,y_cords,rgb_values = file.importProjectedPoints()
    print "--read from files for projected points"
else:
    points, rgb_values = file.importPointsWithRGB()
    camera_pos = [0, 100, -100, -500]  # (500,100,100) as initial position
    I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    camera_ori = np.matrix(I)
    cam = camera.Camera(points, camera_pos, camera_ori, 1)
    x_cords, y_cords, z_cords = cam.getProjectedPts(height, width)
    print "-----projectd points generated------"
    file.saveProjectedPointsWithRGB(x_cords,y_cords,rgb_values)


shader = pts_shader.Shader(x_cords, y_cords, width, height)
out_img_point = shader.plotPoints(rgb_values)
cv2.imwrite("points.png", out_img_point)
print "-----points plotted-----------------"
out_img = shader.testShading(rgb_values)
print "-----points shaded------------------"
cv2.imwrite("img.png",out_img)
# #intialize the frames
# num_frame = 25

# vm = vmaker.VideoMaker(num_frame, width, height, cam, rgb_values)

# vm.generateVideo()
