import cv2
import numpy as np
import sys, os

class detectColor():
    def __init__(self, image, path = None):
        if(path != None): 
            self.img = cv2.imread(image)
        else: 
            self.img = image
        self.FilteredImage = None
        self.cannyImage = None

        self.name = None

        self.lowerBoundSet = False
        self.upperBoundSet = False

        self.lowerBound = None 
        self.upperBound = None
        self.msk = None
        self.kernel = None

        self.colorsFound = False
        self.colorPositions = None

        self.GaussianKernel = None

    def findColor(self): 
        if(self.upperBoundSet and self.upperBoundSet): 
            hsvImage = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
            try: 
                self.msk = cv2.inRange(hsvImage, self.lowerBound, self.upperBound)
            except: 
                pass
            
            if(self.kernel is not None):
                self.FilteredImage = self.erodeImage()
            else:
                self.FilteredImage = cv2.bitwise_and(hsvImage, hsvImage, mask = self.msk)

            self.colorsFound = True
        else: 
            print("Error: Upper and Lower bounds must be set")

    def findCenter(self, img_path):
        thresh = cv2.threshold(img_path, 100, 255, cv2.THRESH_BINARY)[1]
        contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        
        return contours
    
    def getCoordinates(self):
        contours = self.findCenter(self.FilteredImage)
        xList = []
        yList = []
        for c in contours:
            M = cv2.moments(c)
            # print(M['m00'])
            if(M['m00'] == 0.0): 
                continue
            xList.append(int(M['m10']/M['m00']))
            yList.append(int(M['m01']/M['m00']))
            
        return xList, yList


    def drawCross(self, img, x, y, cross_color, line_length, text = None): 
        cv2.line(img, (x-line_length, y), (x+line_length, y), cross_color, 5)
        cv2.line(img, (x, y-line_length), (x, y+line_length), cross_color, 5)
        if(text != None): 
            cv2.putText(img, text, (x + 20, y+80), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2)

    def erodeImage(self):
        return cv2.erode(self.msk, self.kernel, iterations = 2)

    def setName(self, name): 
        self.name = name

    def setKernel(self, size): 
        self.kernel = np.ones((size, size), np.uint8)
    
    def setLowerBound(self, R, G, B):
        self.lowerBound = np.array([R,G,B])
        self.lowerBoundSet = True

    def setUpperBound(self, R, G, B):
        self.upperBound = np.array([R,G,B])
        self.upperBoundSet = True
        
    def showOriginalImage(self):
        cv2.imshow('Original', self.img)
        cv2.waitKey(0)

    def showFilteredimage(self): 
        cv2.imshow('Filtered', self.FilteredImage)
        cv2.waitKey(0)

    def showMask(self):
        cv2.imshow('Mask', self.msk)
        cv2.waitKey(0)

    def showAll(self):
        cv2.imshow('Mask', self.msk)
        cv2.imshow('Filtered', self.FilteredImage)
        cv2.imshow('Original', self.img)
        cv2.imshow('Canny', self.cannyImage)
        cv2.waitKey(0)
    
    def saveImage(self): 
        cv2.imwrite("/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/Color Recognition/images/FilteredImage.png", self.FilteredImage)