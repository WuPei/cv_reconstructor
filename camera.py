import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

class Camera:
    def __init__(self,fileName,cameraInitPoint,translationAxisAngles,orientationAsixAngles):
        self.fileName = fileName;
        self.translationAxisAngles = translationAxisAngles
        self.orientationAsixAngles = orientationAsixAngles
        self.camearPositions =[cameraInitPoint]
        self.rotationMatrices = [np.matrix(np.identity(3))]
    
    def importPoints(self):
        self.pts = []
        for line in open(fileName,'r'):
        pointStr = np.array(line.rstrip().split(","),dtype ='|S4')
        point = pointStr.astype(np.float)
        self.pts.append(point)
    
    def cameraPosition(self):
        for i in range(self.translationAxisAngles.shape[0]):
            axis = self.translationAxisAngles[i][0]
            angle = self.translationAxisAngles[i][1]
            q = axisangle_to_q(axis,angle)
            self.cameraPosition.append ( getNewPoint(self.cameraPosition[i], q) )

    def cameraOrientation(self):
        for i in range(self.orientationAsixAngles.shape[0]):
            axis = self.orientationAsixAngles[i][0]
            angle = self.orientationAsixAngles[i][1]
            q = axisangle_to_q(axis,angle)
            R = quat2rot(q)
            self.cameraOrientation.append(R)

    def quatmult(self,q1, q2):
        #used to rotate the camera's initial position
        result = [0, 0, 0, 0]
        #---- you need to fill in the code here ----
        result[0] = q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] - q1[3]*q2[3]
        result[1] = q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] - q1[3]*q2[2]
        result[2] = q1[0]*q2[2] - q1[1]*q2[3] + q1[2]*q2[0] + q1[3]*q2[1]
        result[3] = q1[0]*q2[3] + q1[1]*q2[2] - q1[2]*q2[1] + q1[3]*q2[0]
        return result
    
    def axisangle_to_q(self,axis,theta):
        out = [0,0,0,0]
        x,y,z = axis
        out = [math.cos(theta/2),math.sin(theta/2)*x,math.sin(theta/2)*y,math.sin(theta/2)*z]
        return out
    
    def conjugate(self,q):
        return [q[0],-q[1],-q[2],-q[3]]
    
    def quat2rot(self,q):
        #used to rotate the camera's direction
        #---- you need to fill in the code here ----
        M = [[0 for y in range(3)] for x in range(3)];
        M[0][0] = q[0]**2+q[1]**2-q[2]**2-q[3]**2
        M[0][1] = 2*(q[1]*q[2]-q[0]*q[3])
        M[0][2] = 2*(q[1]*q[3]+q[0]*q[2])
        
        M[1][0] = 2*(q[1]*q[2]+q[0]*q[3])
        M[1][1] = q[0]**2+q[2]**2-q[1]**2-q[3]**2
        M[1][2] = 2*(q[2]*q[3]-q[0]*q[1])
        
        M[2][0] = 2*(q[1]*q[3]-q[0]*q[2])
        M[2][1] = 2*(q[2]*q[3]+q[0]*q[1])
        M[2][2] = q[0]**2+q[3]**2-q[1]**2-q[2]**2
        return np.matrix(M)
    
    def getNewPoint(self,point,q):
        temp = quatmult(q,point)
        return quatmult(temp,self.conjugate(q))
    
    def perspProj(self,point,ori_mat,posi_mat,u_0 =0,v_0=0,beta_u=1,beta_v=1,f=1):
        #beta_u pixel scaling factor in horizontal direction
        #beta_v pixel scaling factor in vertical direction
        s_p = point
        #t_f is the camera translation matrix
        t_f = np.matrix([posi_mat[1],posi_mat[2],posi_mat[3]])
        #i_f horizontal axis , x is horizontal axis
        i_f = ori_mat[0].T
        #j_f vertical axis here, y is vertical axis
        j_f = ori_mat[1].T
        #k_f optical axis
        k_f = ori_mat[2].T
        
        u_fp = (float)(f*(s_p-t_f)*i_f)/(float)((s_p-t_f)*k_f*beta_u) + u_0
        v_fp = (float)(f*(s_p-t_f)*j_f)/(float)((s_p-t_f)*k_f*beta_v) + v_0
        
        return u_fp,v_fp
    
    def orthProj(self,point,ori_mat,posi_mat,u_0 =0,v_0=0,beta_u=1,beta_v=1,f=1):
        s_p = point
        #t_f is the camera translation matrix
        t_f = np.matrix([posi_mat[1],posi_mat[2],posi_mat[3]])
        #i_f horizontal axis , x is horizontal axis
        i_f = ori_mat[0].T
        #j_f vertical axis here, y is vertical axis
        j_f = ori_mat[1].T
        #k_f optical axis
        k_f = ori_mat[2].T
        
        u_fp = (float) ((s_p - t_f)*i_f*beta_u + u_0)
        v_fp = (float) ((s_p - t_f)*j_f*beta_v + v_0)
        
        return u_fp,v_fp

#part 2: plot projecting 3d shape points on to 2d image plane
x_cord = [[0 for i in range(len(pts))] for j in range(4)]
y_cord = [[0 for i in range(len(pts))] for j in range(4)]
u_fp = [0 for i in range(4)]
v_fp = [0 for i in range(4)]
quatmat = [quatmat_1,quatmat_2,quatmat_3,quatmat_4]
p = [p1,p2,p3,p4]

height = 800
width = 600
blank_image = np.zeros((height,width,3),np.uint8)

#2.1 Figure 1 for perspective projection 
for x in range(len(pts)):
	#fr_num represents for the frame number
	for fr_num in range(4):
		u_fp[fr_num],v_fp[fr_num] = perspProj(pts[x],quatmat[fr_num],p[fr_num])
		x_cord[fr_num][x]= round(800*u_fp[fr_num])
		y_cord[fr_num][x]= round(800*v_fp[fr_num])

for x in range(len(pts)):
	u_fp = x_cord[0][x]
	v_fp = y_cord[0][x]
	blank_image[u_fp][v_fp] = (255,255,255)

cv2.imwrite('test.jpg',blank_image)


