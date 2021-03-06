import math
import numpy as np

pi = np.pi

# This class is a used to get projected 2D points from a bunch of 3D points
#We need to set camera_pos, ori_mat matrix and focal length of camera before using
#The points needed to be projected
#This class support both of orthogonal projection and perspective projection.
class Camera:
    def __init__(self, pts, camera_pos, ori_mat, focal):
        self.pts = pts;
        self.ori_mat = ori_mat
        self.camera_pos = camera_pos
        self.rotationMat = [np.matrix(np.identity(3))]
        self.focal = focal

    def translateCamera(self, translateMat):
        self.camera_pos = self.camera_pos + translateMat

    def translateCameraWithAxisAngle(self, axis, angle,offset_x,offset_z):
        angle = angle * 1.0 / 180 * np.pi
        self.camera_pos = [0,self.camera_pos[1]-offset_x,self.camera_pos[1],self.camera_pos[2]-offset_z]
        q = self.getQuternion(axis, angle)
        self.camera_pos = self.quatmult(self.quatmult(q, self.camera_pos), self.conjugate(q))
        self.camera_pos = [0,self.camera_pos[1]+offset_x,self.camera_pos[1],self.camera_pos[2]+offset_z]

    #angle is negative if clockwise, count-clockwise, the angle must be positive
    def rotateCamera(self, axis, angle):
        theta = angle * 1.0 / 180 * pi
        quter = self.getQuternion(axis, theta)
        R = self.quat2rot(quter)
        self.ori_mat = np.dot(R, self.ori_mat)

    def quatmult(self, q1, q2):
        #used to rotate the camera's initial position
        result = [0, 0, 0, 0]
        #---- you need to fill in the code here ----
        result[0] = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]
        result[1] = q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2]
        result[2] = q1[0] * q2[2] - q1[1] * q2[3] + q1[2] * q2[0] + q1[3] * q2[1]
        result[3] = q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1] + q1[3] * q2[0]
        return result

    def getQuternion(self, axis, theta):
        out = [0, 0, 0, 0]
        x, y, z = axis
        out = [math.cos(theta / 2), math.sin(theta / 2) * x, math.sin(theta / 2) * y, math.sin(theta / 2) * z]
        return out

    def conjugate(self, q):
        return [q[0], -q[1], -q[2], -q[3]]

    def quat2rot(self, q):
        #used to rotate the camera's direction
        #---- you need to fill in the code here ----
        M = [[0 for y in range(3)] for x in range(3)];
        M[0][0] = q[0] ** 2 + q[1] ** 2 - q[2] ** 2 - q[3] ** 2
        M[0][1] = 2 * (q[1] * q[2] - q[0] * q[3])
        M[0][2] = 2 * (q[1] * q[3] + q[0] * q[2])

        M[1][0] = 2 * (q[1] * q[2] + q[0] * q[3])
        M[1][1] = q[0] ** 2 + q[2] ** 2 - q[1] ** 2 - q[3] ** 2
        M[1][2] = 2 * (q[2] * q[3] - q[0] * q[1])

        M[2][0] = 2 * (q[1] * q[3] - q[0] * q[2])
        M[2][1] = 2 * (q[2] * q[3] + q[0] * q[1])
        M[2][2] = q[0] ** 2 + q[3] ** 2 - q[1] ** 2 - q[2] ** 2
        return np.matrix(M)

    #we set the u_0 as offset, it is the half of width of screen
    def perspProj(self, point, ori_mat, posi_mat, focal, u_0=0 , v_0=0, beta_u=1, beta_v=1):
        #beta_u pixel scaling factor in horizontal direction
        #beta_v pixel scaling factor in vertical direction
        s_p = point
        #t_f is the camera translation matrix
        t_f = np.matrix([posi_mat[1], posi_mat[2], posi_mat[3]])
        #i_f horizontal axis , x is horizontal axis
        i_f = ori_mat[0].T
        #j_f vertical axis here, y is vertical axis
        j_f = ori_mat[1].T
        #k_f optical axis
        k_f = ori_mat[2].T
        if (float)((s_p - t_f) * k_f) == 0:
            u_fp = 0
            v_fp = 0
            print "WARNING!The Model is crashing with Camera, reset the position of Models"
        else:
            u_fp = (float)(focal * (s_p - t_f) * i_f) / (float)((s_p - t_f) * k_f * beta_u) + u_0
            v_fp = (float)(focal * (s_p - t_f) * j_f) / (float)((s_p - t_f) * k_f * beta_v) + v_0

        return u_fp, v_fp

    def orthProj(self, point, ori_mat, posi_mat, u_0=0, v_0=0, beta_u=1, beta_v=1, f=1):
        s_p = point
        #t_f is the camera translation matrix
        t_f = np.matrix([posi_mat[1], posi_mat[2], posi_mat[3]])
        #i_f horizontal axis , x is horizontal axis
        i_f = ori_mat[0].T
        #j_f vertical axis here, y is vertical axis
        j_f = ori_mat[1].T
        # #k_f optical axis
        # k_f = ori_mat[2].T

        u_fp = (float)((s_p - t_f) * i_f * beta_u + u_0)
        v_fp = (float)((s_p - t_f) * j_f * beta_v + v_0)

        return u_fp, v_fp

    def getProjectedPts(self, height, width):
        #part 2: plot projecting 3d shape points on to 2d image plane
        x_cord = [0 for i in range(len(self.pts))]
        y_cord = [0 for i in range(len(self.pts))]
        z_cord = [0 for i in range(len(self.pts))]
        #notice: here is normlized x,y coordinates
        #2.1 Figure 1 for perspective projection
        for x in range(len(self.pts)):
            u_fp, v_fp = self.perspProj(self.pts[x],self.ori_mat,self.camera_pos, self.focal)
            x_cord[x] = int(round(height * u_fp)) + 1632/2
            y_cord[x] = int(round(width * v_fp))
            z_cord[x] = int(round(self.pts[x][2]))
        return x_cord, y_cord, z_cord

    def getOrthProjectPts(self,height,width):
        x_cord = [0 for i in range(len(self.pts))]
        y_cord = [0 for i in range(len(self.pts))]
        z_cord = [0 for i in range(len(self.pts))]
        #notice: here is normlized x,y coordinates
        #2.1 Figure 1 for perspective projection
        for x in range(len(self.pts)):
            u_fp, v_fp = self.orthProj(self.pts[x], self.ori_mat, self.camera_pos)
            x_cord[x] = int(round(height * u_fp)) 
            y_cord[x] = int(round(width * v_fp))
            z_cord[x] = int(round(self.pts[x][2]))
        return x_cord, y_cord, z_cord



