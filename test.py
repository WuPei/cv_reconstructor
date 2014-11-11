from Tkinter import *
import os
import numpy as np
from sklearn.neighbors import NearestNeighbors
import cv2
import timeit

import videoMaker as vmaker

def medianOfColor(mylist):
    length = len(mylist)
    grayScale = [0 for i in range(length)]
    for x in range(length):
        grayScale[x] = (mylist[x][0] + mylist[x][1] + mylist[x][2])/3
    sorts = [x for (y,x) in sorted(zip(grayScale,mylist),key = lambda pair:pair[0])]
    if not length % 2:
        return (sorts[length/2] + sorts[length/2-1]) / 2
    return sorts[length / 2]


dir = 'testData/imgs/'

# files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
files = []
for x in range(26):
	filename = os.path.join(dir,"points_"+str(x)+".png")
	files.append(filename)
for x in range(26):
	filename = os.path.join(dir,"img_"+str(x)+".png")
	print filename
	files.append(filename)

width = 1632
height = 1224

vm = vmaker.VideoMaker(52, width, height, 0, 0)
vm.generateVideoFromFiles(files)

# image = cv2.imread("imgs/result.png",cv2.CV_LOAD_IMAGE_COLOR)

# width = image.shape[1] 
# height= image.shape[0]
# start = timeit.default_timer()
# for x in range(width):
#  	for y in range(height):
#  		zero = np.array([0 for i in range(3)])
#  		if not (image[y][x] == zero).all or y < 800:
#  			continue
#  		rgbs = []
#  		for i in xrange(-1,2):
#  			for j in xrange(-1,2):
#  				if x+i < 0 or x+i >= width or y+j<0 or y+j>=height:
#  					continue
#  				rgbs.append(image[y+j][x+i])
#  		# if len(rgbs) == 0 or :
#  		# 	continue
#  		image[y][x] = medianOfColor(rgbs)

# cv2.imwrite("testing.png",image)
# print "Processing Time:", timeit.default_timer()-start,"s"
# list_a = [2,55,150,24,434]
# list_b = [2,23,214,545,24]
# sorts = [(x,y) for (y,x) in sorted(zip(list_a,list_b))]
# print sorts
# x_cords = [10,10,30,40,24,343,24,124]
# y_cords = [10,10,3434,40234,243,33,243,12344]
# rgb_values = [[132,231,234],[132,231,234],[132,23,23],[13,23,234],[132,23,23],[132,23,234],[12,233,234],[132,232,234]]
# pts = [np.int32]
# pts = np.array([[ 668,  33],[ 60,  323],[ 670,  323],[ 670,  321]],np.int32)



# print f5(zip(x_cords,y_cords))

# out_frame = np.zeros((800, 800, 3), np.uint8)
# cv2.fillPoly(out_frame, [pts], [132,231,234])
# cv2.imwrite("img1.png",out_frame)
# print np.array(list(set(tuple(p) for p in rgb_values)))
# print np.unique(np.array(rgb_values))

# X = np.array(zip(x_cords,y_cords))
# knn = NearestNeighbors(n_neighbors=4)
# knn.fit(X)
# NearestNeighbors(algorithm='auto', leaf_size=30, n_neighbors=4, p=2,radius=1.0, warn_on_equidistant=True)
# indexArr = knn.kneighbors(X[0], return_distance=False)
# print indexArr
# neighbourPts = []
# rgbs = []
# for x in range(len(indexArr)):
# 	index = indexArr[x]
# 	print X[index]
# 	print np.asarray(rgb_values)[index]
# 	neighbourPts.append(X[index])
# 	rgbs.append(np.asarray(rgb_values)[index])
# print "neightbour",neighbourPts[0].tolist()
# if neighbourPts[0].tolist().count(neighbourPts[0].tolist()[0]) >=2:
#    print "haha"
# median_color = medianOfColor(rgbs[0])
# print median_color,neighbourPts
# out_frame = np.zeros((600, 800, 3), np.uint8)
# cv2.fillPoly(out_frame, neighbourPts, median_color)
# cv2.imwrite("img1.png",out_frame)

