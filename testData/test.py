import cv2
import numpy as np

width = 800
height = 600
each_frame = np.zeros((width,height,3),np.uint8)

for x in range(0,10,4):
	print x

a = np.array([255,122,255])
b = np.array([12,34,145])
print (a+b)/2

pts = np.array([[100,100],[100,434],[242,424],[400,100]],np.int32)
cv2.fillPoly(each_frame,[pts],[255,255,255])
cv2.imshow("image",each_frame)
cv2.waitKey()