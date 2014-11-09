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


def medianOfColor(mylist):
    length = len(mylist)
    grayScale = [0 for i in range(length)]
    for x in range(length):
        grayScale[x] = int((mylist[x][0] + mylist[x][1] + mylist[x][2])/3)
    sorts = [x for (y,x) in sorted(zip(grayScale,mylist),key = lambda pair:pair[0])]
    if not length % 2:
        return (sorts[length/2] + sorts[length/2-1]) / 2.0
    return sorts[length / 2]

file = fm.FileManager("testData/test.dat")
points, rgb_values = file.importPointsWithRGB()
# points,rgb_values = shuffleTwoLists(points,rgb_values)
width = 1632
height = 1224
y_axis = [0, 1, 0]
x_axis = [1, 0, 0]

# initial camera
camera_pos = [0, 0, 0, -1000]  # (500,100,100) as initial position
I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
camera_ori = np.matrix(I)
cam = camera.Camera(points, camera_pos, camera_ori, 1)

x_cords, y_cords = cam.getProjectedPts(height, width)
print "projected image finished/n"
out_img1 = np.zeros((height, width, 3), np.uint8)
out_img2 = np.zeros((height, width, 3), np.uint8)

# #draw all points
for i in range(0,len(x_cords)):
#print "x(width)",width,"y(height):",height,x_cords[i],y_cords[i]
    real_height = height - y_cords[i]
    if x_cords[i]>=width or real_height>=height or x_cords[i]<0 or real_height<0:
        continue;
    out_img1[real_height][x_cords[i]] = rgb_values[i]

#draw the polygon
for i in range(0, len(x_cords), 4):
    nextFlag = True
    point = [0 for index in range(4)]
    #print "x,y", len(x_cords), len(y_cords)
    if i + 3 > len(x_cords):
        continue
    else:
        for j in range(4):
            x = x_cords[i + j]
            y = height - y_cords[i + j]
            if x >= width or y >= height or x < 0 or y < 0:
                nextFlag = False
            point[j] = [x, y]
    if not nextFlag:
        continue
    pts = np.array([point[0], point[1], point[3], point[2]], np.int32)
    #print  pts
    #get average color from four points
    #median filtering 
    rgbs = [rgb_values[i], rgb_values[i + 1],rgb_values[i + 2],rgb_values[i + 3]]
    median_color = medianOfColor(rgbs)
    average_color = (rgb_values[i] + rgb_values[i + 1] + rgb_values[i + 2] + rgb_values[i + 3]) / 4
    #shading using fillPoly with average color
    cv2.fillPoly(out_img2, [pts], median_color)

cv2.imwrite("test1.png", out_img1)
cv2.imwrite("test2.png",out_img2)
#intialize the frames
num_frame = 30

#vm = vmaker.VideoMaker(num_frame, width, height, cam, rgb_values)

#vm.generateVideo()
