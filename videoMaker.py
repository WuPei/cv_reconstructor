import cv2
import numpy as np


class VideoMaker:
    def __init__(self, num_frame, width, height):
        self.num_frame = num_frame
        self.width = width
        self.height = height
        blank_image = np.zeros((height, width, 3), np.uint8)
        self.frames = [blank_image for x in range(num_frame)]

        # this method will create a video which the object rotating respect to certain angle.

    def generateVideoFromFiles(self,files):
        fps = 25
        capSize = (self.width,self.height)
        fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
        writer = cv2.VideoWriter()
        success = writer.open("result.mov", fourcc, fps, capSize, True)
        if success:
            for f in files:
                img = cv2.imread(f,cv2.CV_LOAD_IMAGE_COLOR)
                writer.write(img)
                print f
            writer.release()
