import cv2
import numpy as np

# This class is a shader for a 2D discrete points, the output is a image frame for certain width,height.
#After projection of 3D discrete points, the frame generated will be holes in between points. 
#This shader is trying to fill these holes by finding nearby points, and draw them as filled mesh.
#shading mehtod must be used after intializing.
class Shader:
    def __init__(self, x_cords, y_cords, x_offset, y_offset, width, height):
        self.x_cords = x_cords
        self.y_cords = y_cords
        self.offset_x = x_offset
        self.offset_y = y_offset
        self.width = width
        self.height = height
        self.out_frame = np.zeros((width, height, 3), np.uint8)

    def shading(self, rgb_values):
        for i in range(0, len(self.x_cords), 4):

            point = [0 for index in range(4)]
            if self.is_out_of_bounds(i):
                continue
            for j in range(4):
                x = self.x_cords[i + j] + self.offset_x
                y = self.y_cords[i + j] + self.offset_y
                point[j] = [x, y]
            pts = np.array([point[0], point[1], point[3], point[2]], np.int32)
            #get average color from four points
            average_color = (rgb_values[i] + rgb_values[i + 1] + rgb_values[i + 2] + rgb_values[i + 3]) / 4
            #shading using fillPoly with average color
            cv2.fillPoly(self.out_frame, [pts], average_color)
        #print each_frame
        return self.out_frame

    def is_out_of_bounds(self, base):
        for i in range(4):
            x = self.x_cords[base + i] + self.offset_x
            y = self.y_cords[base + i] + self.offset_y
            if x >= self.width or x < 0:
                return True
            elif y >= self.height or y < 0:
                return True
        return False