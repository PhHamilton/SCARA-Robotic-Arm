
# from readQR import QRCalibration
import cv2 
import numpy as np

QRDistance = 107.5

def setPoint(x,y, img, imgWidth):
    cv2.circle(img, (np.int32(imgWidth/2 + mmToPixel(x, imgWidth)),np.int32(imgWidth/2 - mmToPixel(y, imgWidth))), 15, (0,0,255),cv2.FILLED)

def getPoint(x,y, imgWidth):
    return pixelTomm(x-imgWidth/2, imgWidth) / 10, pixelTomm(imgWidth/2-y,imgWidth) / 10

def mmToPixel(pos, width):
    return width / QRDistance * pos

def pixelTomm(pos, width): 
    return QRDistance/width * pos


class warpImage():
    def __init__(self, img, imageWidth): 
        self.img = img
        self.width = imageWidth
        self.newPoints = np.float32([[0,0], [0, self.width], [self.width, self.width], [self.width, 0]])
        self.warpedImage = None
    def warpImage(self, QRCorners):
        corners = np.float32(QRCorners)
        tMatrix = cv2.getPerspectiveTransform(corners, self.newPoints)
        self.warpedImage = cv2.warpPerspective(self.img, tMatrix, (self.width, self.width))
    def showImage(self): 
        cv2.imshow("TransformedImage", self.warpedImage)
        cv2.waitKey(0)
        
    



    