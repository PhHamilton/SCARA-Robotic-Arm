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
            self.msk = cv2.inRange(hsvImage, self.lowerBound, self.upperBound)
            
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
            print(M['m00'])
            if(M['m00'] == 0.0): 
                continue
            xList.append(int(M['m10']/M['m00']))
            yList.append(int(M['m01']/M['m00']))

        return xList, yList


    def drawCross(self, img, x, y, cross_color, line_length, text = None): 
        for i in range(len(x)):
            cv2.line(img, (x[i]-line_length, y[i]), (x[i]+line_length, y[i]), cross_color, 5)
            cv2.line(img, (x[i], y[i]-line_length), (x[i], y[i]+line_length), cross_color, 5)
            if(text != None): 
                cv2.putText(img, text, (x[i] + 20, y[i]+80), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2)
        # for c in filtered_contours:
        #     M = cv2.moments(c)
        #     x = int(M['m10']/M['m00'])
        #     y = int(M['m01']/M['m00'])
        #     cv2.line(img, (x-line_length, y), (x+line_length, y), cross_color, 2)
        #     cv2.line(img, (x, y-line_length), (x, y+line_length), cross_color, 2)

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

    def convertToPIL(self): 
        pass

        


if __name__ == "__main__":
    # imgPath = "/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/Color Recognition/images/colors.jpg"
    script_dir = sys.path[0]
    Path = "../images/colors.jpg"
    imgPath = os.path.join(script_dir, Path)
    a = detectColor(imgPath)

    if sys.argv[1] == "Blue":
        a.setName("Blue")
        a.setLowerBound(90,50,50)
        a.setUpperBound(130,255,255)
    elif sys.argv[1] == "Orange":
        a.setName("Orange")
        a.setLowerBound(9,0,20)
        a.setUpperBound(25,255,255)

    elif sys.argv[1] == "Red":
        a.setName("Red")
        a.setLowerBound(150,50,20)
        a.setUpperBound(179,255,255)

    # a.setName("Green")
    # a.setLowerBound(50,150,20)
    # a.setUpperBound(70,255,255)
    a.setKernel(10)

    # For example gimp uses H = 0-360, S = 0-100 and V = 0-100. But OpenCV uses  H: 0-179, S: 0-255, V: 0-255.
    # https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv

    a.findColor()
    a.saveImage()

    # filtered = a.process_and_detect("/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/Color Recognition/images/FilteredImage.png")
    x,y = a.getCoordinates()
    
    a.drawCross(a.img, x,y, (255,0,0), 20)

    # cv2.imshow(a.name, a.img)
    cv2.imshow(a.name, a.img)
    cv2.waitKey(0)

    # a.saveImage()
    # a.showAll()