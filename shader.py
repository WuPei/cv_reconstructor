import cv2
import numpy as np
# from sklearn.neighbors import NearestNeighbors
from texture import Point
# This class is a shader for a 2D discrete points, the output is a image frame for certain width,height.
#After projection of 3D discrete points, the frame generated will be holes in between points. 
#This shader is trying to fill these holes by finding nearby points, and draw them as filled mesh.
#shading mehtod must be used after intializing.
class Shader:
    def __init__(self, width, height, base_img):
        self.width = width
        self.height = height
        self.out_frame = base_img
        #np.zeros((height, width, 3), np.uint8)

    def medianOfColor(self,mylist):
        length = len(mylist)
        grayScale = [0 for i in range(length)]
        for x in range(length):
            grayScale[x] = int((mylist[x][0] + mylist[x][1] + mylist[x][2])/3)
        sorts = [x for (y,x) in sorted(zip(grayScale,mylist),key = lambda pair:pair[0])]
        if not length % 2:
            return (sorts[length/2] + sorts[length/2-1]) /2
        return sorts[length / 2]

    def shading(self, x_cords, y_cords, rgb_values,mode):
        print "len:",len(x_cords)
        for i in range(0, len(x_cords), 4):
            point = [0 for index in range(4)]
            if self.is_out_of_bounds(x_cords,y_cords,i,mode):
                continue
            for j in range(4):
                x = x_cords[i + j]
                if mode==2:
                    y = -y_cords[i + j]
                elif mode==1:
                    y = self.height- y_cords[i + j]
                point[j] = [x, y]
            pts = np.array([point[0], point[1], point[2], point[3]], np.int32)
            #get average color from four points
            average_color = (rgb_values[i] + rgb_values[i + 1] + rgb_values[i + 2] + rgb_values[i + 3]) / 4
            #shading using fillPoly with average color
            cv2.fillPoly(self.out_frame, [pts], average_color)
        #print each_frame
        print "shading image finished/n"
        return self.out_frame


    def medianShading(self,x_cords, y_cords, rgb_values):
        print "len:",len(self.x_cords)
        for i in range(0, len(self.x_cords), 4):
            point = [0 for index in range(4)]
            if self.is_out_of_bounds(i):
                continue
            for j in range(4):
                x = x_cords[i + j]
                y = y_cords[i + j]
                point[j] = [x, y]
            pts = np.array([point[0], point[1], point[2], point[3]], np.int32)
            #get average color from four points
            rgbs = [rgb_values[i] , rgb_values[i + 1] , rgb_values[i + 2] , rgb_values[i + 3]]
            median_color = self.medianOfColor(rgbs)
            #shading using fillPoly with average color
            cv2.fillPoly(self.out_frame, [pts], median_color)
        #print each_frame
        print "shading image finished/n"
        return self.out_frame

    def plotPoints(self,x_cords, y_cords,rgb_values):
        self.out_frame = np.zeros((self.height, self.width, 3), np.uint8)
        for i in range(0,len(x_cords)):
            real_height = y_cords[i]
            if x_cords[i]>=self.width or real_height>=self.height or x_cords[i]<0 or real_height<0:
                continue;
            self.out_frame[real_height][x_cords[i]] = rgb_values[i]
        return self.out_frame

    def is_out_of_bounds(self, x_cords,y_cords,base,mode):
        for i in range(4):
            x = x_cords[base + i]
            if mode==1:
                y = self.height- y_cords[base + i]
            elif mode==2:
                y = -y_cords[base + i]#self.height- y_cords[i + j]
            if x >= self.width or x < 0:
                return True
            elif y >= self.height or y < 0:
                return True
        return False