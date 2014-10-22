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
            lineArray = np.array(line.rstrip().split(","),dtype ='|S4')
            values_point = [lineArray[0],lineArray[1],lineArray[2]]
            values_point = values_point.astype(np.float)
            values_rgb = [lineArray[3],lineArray[4],lineArray[5]]
            self.rgb_value.append(values_rgb)
            self.pts.append(values_point)
        return self.pts,self.rgb_value

