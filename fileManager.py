import numpy as np

class FileManager:
    def __init__(self,fileName):
        self.fileName = fileName;
        self.pts = []
        self.rgb_value = []

    def importPoints(self):
        for line in open(self.fileName,'r'):
        	pointStr = np.array(line.rstrip().split(","),dtype ='|S4')
        	point = pointStr.astype(np.float)
        	self.pts.append(point)
        return self.pts

    def importPointsWithRGB(self):
    	for line in open(self.fileName,'r'):
            valuesStr = np.array(line.rstrip().split(","),dtype ='|S4')
            values = valuesStr.astype(np.float)
            values_point = np.array([values[0],values[1],values[2]])
            values_rgb = np.array([values[3],values[4],values[5]])
            self.pts.append(values_point)
            self.rgb_value.append(values_rgb)
        return self.pts,self.rgb_value

