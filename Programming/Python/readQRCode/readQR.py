
from pyzbar.pyzbar import decode

import numpy as np
import cv2 


class QRCalibration():
    def __init__(self):
        
        self.bMsk = (0,0,0)
        self.wMsk = (90,90,90)
        self.img = None

    def getCorners(self, path, DEBUG = False): 
        self.img = cv2.imread(path)
        mask = cv2.inRange(self.img,(self.bMsk),(self.wMsk))
        thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
        inverted = 255-thresholded # black-in-white

        rctPoints = np.zeros((4,2), np.int32)
        for barCode in decode(inverted):
            pts = np.array([barCode.polygon], np.int32)
            pts.reshape((-1,1,2))
            cv2.polylines(self.img, [pts], True, (255, 0, 0), 10)
            label = barCode.data.decode('utf-8')
            # print(pts[0][2])
            # print(label, pts[0,0])
            if(label == "Top Left"): 
                rctPoints[0,0] = pts[0,0][0]
                rctPoints[0,1] = pts[0,0][1]
            elif(label == "Bottom Left"):
                rctPoints[1,0] = pts[0,1][0]
                rctPoints[1,1] = pts[0,1][1]
            elif(label == "Top Right"):
                rctPoints[3,0] = pts[0,3][0]
                rctPoints[3,1] = pts[0,3][1]
            elif(label == "Bottom Right"):
                rctPoints[2,0] = pts[0,2][0]
                rctPoints[2,1] = pts[0,2][1]

        # rectPts.reshape((-1,1,2))
        # print(pts)
        # print(rectPts)
        cv2.polylines(self.img, [rctPoints], True, (255, 0, 0), 10)
        return rctPoints

    def showImage(self): 
        cv2.imshow("Image", self.img)
        cv2.waitKey(0)


if __name__ == '__main__':
    path = r'/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/readQRCode/img/test.jpg'
    test = QRCalibration()
    test.getCorners(path)
    test.showImage()

# QRDist = 107.5 # [mm]


# img = cv2.imread('/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/readQR/img/test.jpg')
# mask = cv2.inRange(img,(0,0,0),(100,100,100))
# thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
# inverted = 255-thresholded # black-in-white

# rectPts = np.zeros((4,2), np.int32)



# for barCode in decode(inverted):
#     pts = np.array([barCode.polygon], np.int32)
#     pts.reshape((-1,1,2))
#     cv2.polylines(img, [pts], True, (255, 0, 0), 10)
#     label = barCode.data.decode('utf-8')
#     # print(pts[0][2])
#     # print(label, pts[0,0])
#     if(label == "Top Left"): 
#         rectPts[0,0] = pts[0,0][0]
#         rectPts[0,1] = pts[0,0][1]
#     elif(label == "Bottom Left"):
#         rectPts[1,0] = pts[0,1][0]
#         rectPts[1,1] = pts[0,1][1]
#     elif(label == "Top Right"):
#         rectPts[3,0] = pts[0,3][0]
#         rectPts[3,1] = pts[0,3][1]
#     elif(label == "Bottom Right"):
#         rectPts[2,0] = pts[0,2][0]
#         rectPts[2,1] = pts[0,2][1]

# # rectPts.reshape((-1,1,2))
# # print(pts)
# # print(rectPts)
# cv2.polylines(img, [rectPts], True, (255, 0, 0), 10)




# cv2.imshow('img', img)
# cv2.imshow('Inverted img', inverted)
# cv2.waitKey(0)