import numpy as np
import shape as sp
import re
import os

class FileManager:
    def __init__(self):
        self.pts = []
        self.rgb_value = []
        self.x_cords = []
        self.y_cords = []
        self.pFileName = "testData/projectedPoints.dat"

    def importPoints(self):
        for line in open(self.fileName, 'r'):
            pointStr = np.array(line.rstrip().split(","), dtype='|S4')
            point = pointStr.astype(np.float)
            self.pts.append(point)
        return self.pts

    def importPointsWithRGB(self,filename):
        print "import file:",filename
        for line in open(filename, 'r'):
            valuesStr = np.array(line.rstrip().split(","), dtype='|S4')
            values = valuesStr.astype(np.float)
            values_point = np.array([values[0], values[1], values[2]])
            values_rgb = np.array([values[3], values[4], values[5]])
            self.pts.append(values_point)
            self.rgb_value.append(values_rgb)
        return self.pts, self.rgb_value

    def importProjectedPoints(self):
        if os.path.isfile(self.pFileName):
            for line in open(self.pFileName, 'r'):
                valuesStr = np.array(line.rstrip().split(","), dtype='|S4')
                values = valuesStr.astype(np.float)
                values_rgb = np.array([values[2], values[3], values[4]])
                self.x_cords.append(values[0])
                self.y_cords.append(values[1])
                self.rgb_value.append(values_rgb)
            return self.x_cords, self.y_cords, self.rgb_value
        else:
            return False
        

    def saveProjectedPointsWithRGB(self,x_cords,y_cords,rgb_values):
        fileRGB = open(self.pFileName, "w+")
        for i in range(len(x_cords)):
            point = "{0},{1},{r},{g},{b}\n".format(x_cords[i], y_cords[i],r=rgb_values[i][0], g=rgb_values[i][1], b=rgb_values[i][2])
            fileRGB.write(point)
        print "projected point saved"

    #the format is as follows
    #0          1       2   3  4    5                       6                                                   7
    #cuboid [600,0,50] 100 40 30 building1 Front:[[1250.0,867.0],[1301.0,867.0],[1301.0,691.0],[1248.0,695.0]]
    #prism [580,25,180] 80 90 20 building2 Front:[[708.0,790.0],[851.0,793.0],[782.0,754.0]]
    #frumstum center hight uL uW lL             lW                                                              name    faces
    def importShapes(self,filename):
        shapes = []
        for line in open(filename,'r'):
            inData = line.rstrip().split(" ")
            if len(inData) >0:

                if inData[0] == "cuboid":
                    inData[1] = map(int,re.findall('\d+', inData[1]))
                    shapes.append( sp.Cuboid (inData[1], int(inData[2]), int(inData[3]), int(inData[4]), inData[5] ))
                    #read faces
                    for i in xrange (6, len(inData)):
                        inData[i] = inData[i].split(":")
                        inData[i][1] = map(float, re.findall('\d+.\d+', inData[i][1]))
                        facePoints = []
                        for j in range(0,len(inData[i][1]), 2):
                            facePoints.append([ inData[i][1][j], inData[i][1][j+1] ] )
                        shapes[len(shapes)-1].faces.append(sp.Face(facePoints, inData[i][0]))
                
                elif inData[0] == "prism":
                    inData[1] = map(int,re.findall('\d+', inData[1]))
                    shapes.append( sp.Prism (inData[1], int(inData[2]), int(inData[3]), int(inData[4]), inData[5] ))
                    #read faces
                    for i in xrange (6, len(inData)):
                        inData[i] = inData[i].split(":")
                        inData[i][1] = map(float, re.findall('\d+.\d+', inData[i][1]))
                        facePoints = []
                        for j in range(0,len(inData[i][1]), 2):
                            facePoints.append([ inData[i][1][j], inData[i][1][j+1] ] )
                        shapes[len(shapes)-1].faces.append(sp.Face(facePoints, inData[i][0]))

                elif inData[0] == "frustum":
                    inData[1] = map(int,re.findall('\d+', inData[1]))
                    shapes.append( sp.Frustum (inData[1], int(inData[2]), int(inData[3]), int(inData[4]), int(inData[5]), int(inData[6]), inData[7] ))
                    #read faces
                    for i in xrange (8, len(inData)):
                        inData[i] = inData[i].split(":")
                        inData[i][1] = map(float, re.findall('\d+.\d+', inData[i][1]))
                        facePoints = []
                        for j in range(0,len(inData[i][1]), 2):
                            facePoints.append([ inData[i][1][j], inData[i][1][j+1] ] )
                        shapes[len(shapes)-1].faces.append(sp.Face(facePoints, inData[i][0]))

                elif inData[0] == "cylinder":
                    inData[1] = map(int,re.findall('\d+', inData[1]))
                    shapes.append( sp.Cylinder (inData[1], int(inData[2]), int(inData[3]), inData[4] ))
                    #read faces
                    for i in xrange (5, len(inData)):
                        inData[i] = inData[i].split(":")
                        inData[i][1] = map(float, re.findall('\d+.\d+', inData[i][1]))
                        facePoints = []
                        for j in range(0,len(inData[i][1]), 2):
                            facePoints.append([ inData[i][1][j], inData[i][1][j+1] ] )
                        shapes[len(shapes)-1].faces.append(sp.Face(facePoints, inData[i][0]))

                elif inData[0] == "sky":
                    shapes.append( sp.Sky (inData[2]))
                    inData[1] = map(float, re.findall('\d+.\d+', inData[1]))
                    facePoints = []
                    for j in range(0,len(inData[1]), 2):
                        facePoints.append( [inData[1][j],inData[1][j+1]] )    
                    
                    shapes[len(shapes)-1].faces.append(sp.Face(facePoints, "face"))

                elif inData[0] == "ground":
                    shapes.append( sp.Ground (inData[2]))
                    inData[1] = map(float, re.findall('\d+.\d+', inData[1]))
                    facePoints = []
                    for j in range(0,len(inData[1]), 2):
                        facePoints.append([ inData[1][j], inData[1][j+1] ] )
                        
                    shapes[len(shapes)-1].faces.append(sp.Face(facePoints, "face"))

                """
                elif inData[0] == "tree":

                    inData[1] = map(float, re.findall('\d+.\d+', inData[1]))
                    facePoints = []
                    for j in range(0,len(inData[1]), 2):
                        facePoints.append([ inData[1][j], inData[1][j+1] ] )
                        
                    shapes.append( sp.Sky (inData[1],inData[2]))
                """

        return shapes
            


                    



