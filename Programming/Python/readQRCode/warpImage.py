
# from readQR import QRCalibration
import cv2 
import numpy as np

QRDistance = 107.5

def setPoint(x,y, img, imgWidth):
    cv2.circle(img, (np.int32(imgWidth/2 + mmToPixel(x, imgWidth)),np.int32(imgWidth/2 - mmToPixel(y, imgWidth))), 15, (0,0,255),cv2.FILLED)
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
        
if __name__ == '__main__':
    path = r'/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/readQRCode/img/testWColors.jpg'
    test = QRCalibration()
    corners = test.getCorners(path)
    
    width = corners[2,0] - corners[0,0]
    # # height = corners[1,1] - corners[0,1]

    warped = warpImage(test.img, width)
    warped.warpImage(corners)

    setPoint(10, -40, warped.warpedImage, width)
    test.showImage()
    warped.showImage()
    # width = corners[3,0] - corners[0,0]
    # # height = corners[1,1] - corners[0,1]
    # corners = np.float32(corners)
    # pts = np.float32([[0,0], [0, width], [width, width], [width, 0]])
    
    # print(corners)
    # print(pts)
    # print(width/2)
    # tMatrix = cv2.getPerspectiveTransform(corners, pts)

    # img2 = cv2.warpPerspective(test.img, tMatrix, (width, width))
    # cv2.circle(img2, (np.int32(width/2), np.int32(width/2)), 10, (0,0,255),cv2.FILLED)
    # setPoint(40,50,img2, width)
    # cv2.imshow("Transormed Image", img2)
    # test.showImage()
    



    