import cv2
import numpy as np
import camera
import shader as pts_shader
import cv


class VideoMaker:
    def __init__(self, num_frame, width, height, cam, rgb_values):
        self.num_frame = num_frame
        self.width = width
        self.height = height
        self.cam = cam
        self.rgb_values = rgb_values
        blank_image = np.zeros((height, width, 3), np.uint8)
        self.frames = [blank_image for x in range(num_frame)]

        # this method will create a video which the object rotating respect to certain angle.

    def ImgsFromCamPath(self):
        offset_u = 0#self.width / 2
        offset_v = 0#self.height / 2
        axis = [0, 1, 0]
        angle = 10
        for i in range(self.num_frame):
            self.cam.translateCameraWithAxisAngle(axis, angle)
            self.cam.rotateCamera(axis, -angle)

            x_cords, y_cords = self.cam.getProjectedPts(self.height, self.width)

            shader = pts_shader.Shader(x_cords, y_cords, offset_u, offset_v, self.width, self.height)
            self.frames[i] = shader.shading(self.rgb_values)

    def testCamPath(self):
        #go forward
        axis = [0, 0, 1]
        for i in range(self.num_frame):
            self.cam.camera_pos = self.cam.camera_pos - [0,0,0,100]
            x_cords, y_cords = self.cam.getProjectedPts(self.height, self.width)
            shader = pts_shader.Shader(x_cords, y_cords, self.width, self.height)
            self.frames[i] = shader.shading(self.rgb_values)

    def generateVideo(self):
        #self.ImgsFromCamPath()
        self.testCamPath
        fps = 25
        capSize = (self.height, self.width)
        fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
        writer = cv2.VideoWriter()
        success = writer.open("output.mov", fourcc, fps, capSize, True)
        if success:
            for x in range(len(self.frames)):
                writer.write(self.frames[x])
            writer.release()

    def generateVideoFromFiles(self,files):
        fps = 10
        capSize = (self.width,self.height)
        fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
        writer = cv2.VideoWriter()
        success = writer.open("showcase.mov", fourcc, fps, capSize, True)
        if success:
            for f in files:
                img = cv2.imread(f,cv2.CV_LOAD_IMAGE_COLOR)
                writer.write(img)
                print f
            writer.release()
