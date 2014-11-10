import cv2
import numpy as np
# from sklearn.neighbors import NearestNeighbors
from texture import Point
# This class is a shader for a 2D discrete points, the output is a image frame for certain width,height.
#After projection of 3D discrete points, the frame generated will be holes in between points. 
#This shader is trying to fill these holes by finding nearby points, and draw them as filled mesh.
#shading mehtod must be used after intializing.
class Shader:
    def __init__(self, x_cords, y_cords, width, height):
        self.x_cords = x_cords
        self.y_cords = y_cords
        self.width = width
        self.height = height
        self.out_frame = np.zeros((height, width, 3), np.uint8)

    def medianOfColor(self,mylist):
        length = len(mylist)
        grayScale = [0 for i in range(length)]
        for x in range(length):
            grayScale[x] = int((mylist[x][0] + mylist[x][1] + mylist[x][2])/3)
        sorts = [x for (y,x) in sorted(zip(grayScale,mylist),key = lambda pair:pair[0])]
        if not length % 2:
            return (sorts[length/2] + sorts[length/2-1]) /2
        return sorts[length / 2]

    def shading(self, rgb_values):
        print "len:",len(self.x_cords)
        for i in range(0, len(self.x_cords), 4):
            point = [0 for index in range(4)]
            if self.is_out_of_bounds(i):
                continue
            for j in range(4):
                x = self.x_cords[i + j]
                y = self.height - self.y_cords[i + j]
                point[j] = [x, y]
            pts = np.array([point[0], point[1], point[3], point[2]], np.int32)
            #get average color from four points
            average_color = (rgb_values[i] + rgb_values[i + 1] + rgb_values[i + 2] + rgb_values[i + 3]) / 4
            #shading using fillPoly with average color
            cv2.fillPoly(self.out_frame, [pts], average_color)
        #print each_frame
        print "shading image finished/n"
        return self.out_frame

    # def testShading(self, rgb_values,num):
    #     print "len:",len(self.x_cords)
    #     #count = 0 
    #     for i in range(len(self.x_cords)):
    #         points = np.array(zip(self.x_cords,self.y_cords))
    #         knn = NearestNeighbors(n_neighbors=num)
    #         knn.fit(points)
    #         NearestNeighbors(algorithm='auto', leaf_size=30, n_neighbors=num, p=2,radius=1.0, warn_on_equidistant=True)
    #         indexArr = knn.kneighbors(points[i], return_distance=False)
    #         #print indexArr
    #         neighbourPts = []
    #         rgbs = []
    #         for j in range(len(indexArr)):
    #             index = indexArr[j]
    #             point = points[index]
    #             neighbourPts.append(point)
    #             rgbs.append(np.asarray(rgb_values)[index])

    #         uniqueNeighb = np.array(list(set(tuple(p) for p in neighbourPts[0].tolist())),np.int32)
    #         if len(uniqueNeighb) < 3:
    #             #print count
    #             continue
    #         median_color = self.medianOfColor(rgbs[0])
    #         #count = count + 1
    #         #print count
    #         #shading using fillPoly with average color
    #         cv2.fillPoly(self.out_frame, [uniqueNeighb], median_color)
    #     return self.out_frame


    def plotPoints(self,rgb_values):
        for i in range(0,len(self.x_cords)):
            real_height = self.height - self.y_cords[i]
            if self.x_cords[i]>=self.width or real_height>=self.height or self.x_cords[i]<0 or real_height<0:
                continue;
            self.out_frame[real_height][self.x_cords[i]] = rgb_values[i]
        return self.out_frame

    def is_out_of_bounds(self, base):
        for i in range(4):
            x = self.x_cords[base + i]
            y = self.height - self.y_cords[base + i]
            if x >= self.width or x < 0:
                return True
            elif y >= self.height or y < 0:
                return True
        return False