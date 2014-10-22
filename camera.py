import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

pi = np.pi

def quatmult(q1, q2):
	#used to rotate the camera's initial position
	result = [0, 0, 0, 0] 
	#---- you need to fill in the code here ----
	result[0] = q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] - q1[3]*q2[3]
	result[1] = q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] - q1[3]*q2[2]
	result[2] = q1[0]*q2[2] - q1[1]*q2[3] + q1[2]*q2[0] + q1[3]*q2[1]
	result[3] = q1[0]*q2[3] + q1[1]*q2[2] - q1[2]*q2[1] + q1[3]*q2[0]

	return result

def quat2rot(q):
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

def getNewPoint(point,q):
	conju_q = [q[0],-q[1],-q[2],-q[3]]

	temp = quatmult(point,conju_q)

	return quatmult(q,temp)

def perspProj(point,ori_mat,posi_mat,u_0 =0,v_0=0,beta_u=1,beta_v=1,f=1):
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

def orthProj(point,ori_mat,posi_mat,u_0 =0,v_0=0,beta_u=1,beta_v=1,f=1):
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

def axisangle_to_q(axis,theta):
	out = [0,0,0,0]
	x,y,z = axis
	out = [math.cos(theta/2),-math.sin(theta/2)*x,-math.sin(theta/2)*y,-math.sin(theta/2)*z]
	return out

def conjugate(q):
	return [q[0],-q[1],-q[2],-q[3]]

def plotFigure(index,color,title):
	fig = plt.figure(index) #will be created by default,just as subplot(1,1,1) as axis
	fig.suptitle(title,fontsize=15)
	#1st frame 
	plt.subplot(2,2,1)
	plt.plot(x_cord[0],y_cord[0],color)
	plt.title("Initial frame")

	plt.subplot(2,2,2)
	plt.plot(x_cord[1],y_cord[1],color)
	plt.title("2nd frame")

	plt.subplot(2,2,3)
	plt.plot(x_cord[2],y_cord[2],color)
	plt.title("3rd frame")

	plt.subplot(2,2,4)
	plt.plot(x_cord[3],y_cord[3],color)
	plt.title("End frame")

pts = []
#1.1define all the 3D points, later project them to 2d image plane.1)orthographic 2)perspective
for line in open("cylinder.dat",'r'):
	pointStr = np.array(line.rstrip().split(","),dtype ='|S4')
	point = pointStr.astype(np.float)
	pts.append(point)

#1.2 Define the camera's translation (quatioent multiplication)
radian = 15.0/180*pi# for 30 degree
y_axis = [0,1,0]
z_axis = [0,0,1]
#as the camera is roated count-clock wise 30 degree based on y-axis
q = [math.cos(-radian),0,math.sin(-radian),0];

#pi as the position of camera
p1 = [0 , 0 , 0, -800] #it's [0,0,-5] in 3D points, the first s0 as scalar.
p2 = getNewPoint(p1,q)	
p3 = getNewPoint(p2,q)
p4 = getNewPoint(p3,q)
#testing the correctness of quat2rot and quatmatmult
#print p2,"\n", quat2rot(q)*np.matrix([0,-5,1]).T

#1.3 Define the camera's orientation (rotation matrix)
ori_q = [math.cos(radian),0,math.sin(radian),0];
R = quat2rot(ori_q)
#quatmat_i as the direction of camera
I = [[1,0,0],[0,1,0],[0,0,1]]
I = np.matrix(I)
quatmat_1 = I 
quatmat_2 = np.dot(R,I)
quatmat_3 = np.dot(R,quatmat_2)
quatmat_4 = np.dot(R,quatmat_3)

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


