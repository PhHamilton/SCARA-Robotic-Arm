from readQRCode.readQR import QRCalibration
from readQRCode.warpImage import warpImage, setPoint, getPoint, QRDistance

from ColorRecognition.lib.ColorRecognition import detectColor
import cv2


def findColor(obj, img, color):
    if color == "Blue": 
        obj.setName("Blue")
        obj.setLowerBound(90,50,50)
        obj.setUpperBound(130,255,255)
        crosshairColor = (255, 0, 0)

    elif color == "Yellow":
        obj.setName("Yellow")
        obj.setLowerBound(0,100,20)
        obj.setUpperBound(20,255,255)
        crosshairColor = (0, 255, 255)
    elif color == "Orange": 
        obj.setName("Orange")
        obj.setLowerBound(0,100,20)
        obj.setUpperBound(10,150,255)
        crosshairColor = (51, 153, 255)
    elif color == "Green": 
        obj.setName("Green")
        obj.setLowerBound(40,100,0)
        obj.setUpperBound(90,255,255)
        crosshairColor = (0, 255, 0)
    elif color == "Red": 
        obj.setName("Red")
        obj.setLowerBound(160,150,10)
        obj.setUpperBound(180,255,255)
        crosshairColor = (0, 0, 255)
    elif color == "Purple": 
        obj.setName("Purple")
        obj.setLowerBound(140,100,20)
        obj.setUpperBound(165,255,255)
        crosshairColor = (51, 0, 103)


    obj.setKernel(10)
    obj.findColor()
    x,y = obj.getCoordinates()
    inMM = getPoint(x,y, width)
    print(inMM)
    txt = "({:.1f}, {:.1f})".format(inMM[0], inMM[1])
    obj.drawCross(img, x, y, crosshairColor, 20, txt)

if __name__ == "__main__": 
    path = r'/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/readQRCode/img/testWColors.jpg'
    test = QRCalibration()
    corners = test.getCorners(path)
    
    width = corners[2,0] - corners[0,0]

    warped = warpImage(test.img, width)
    warped.warpImage(corners)

    colorDetection = detectColor(warped.warpedImage)
    findColor(colorDetection, warped.warpedImage, "Blue")

    warped.showImage()
    
    # test.showImage()
    # warped.showImage()