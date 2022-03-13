
from pyzbar.pyzbar import decode

import numpy as np
import cv2 

class QRCalibration():
    def __init__(self):
        
        self.bMsk = (0,0,0)
        self.wMsk = (90,90,90)
        self.nTries = 10
        self.points = np.zeros((4,2), np.int32)
        self.img = None

    def getImage(self, img, path = None):
        if path is not None: 
            self.img = cv2.imread(path)
        else: 
            self.img = img

    def getCorners(self, img, path = None, DEBUG = False): 
        self.getImage(img, path)

        mask = cv2.inRange(self.img,(self.bMsk),(self.wMsk))
        thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
        inverted = 255-thresholded 

        for i in range(self.nTries):
            rctPoints = np.zeros((4,2), np.int32)
            for barCode in decode(inverted):
                pts = np.array([barCode.polygon], np.int32)
                pts.reshape((-1,1,2))
                cv2.polylines(self.img, [pts], True, (255, 0, 0), 10)
                label = barCode.data.decode('utf-8')

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
            if len(rctPoints[:,1]) == 4 and self.validEntries(rctPoints) == True:
                self.points = rctPoints
                break
        return self.points

    def drawRectangle(self, img, corners): 
        cv2.polylines(img, [corners], True, (255, 0, 0), 10)

    def validEntries(self, points):
        for i in range(4): 
            # Check that elements are non zero
            if(points[i, 0] == 0 or points[i, 1] == 0):
                return False
            else: 
                continue
        return True

    def showImage(self): 
        cv2.imshow("Image", self.img)
        cv2.waitKey(0)
