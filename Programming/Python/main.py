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
    # inMM = getPoint(x,y, width)
    # print(inMM)
    # txt = "({:.1f}, {:.1f})".format(inMM[0], inMM[1])
    # obj.drawCross(img, x, y, crosshairColor, 20, txt)

    return x, y

if __name__ == "__main__": 
    path = r'/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/readQRCode/img/testWColors.jpg'
    test = QRCalibration()
    corners = test.getCorners(path)
    
    width = corners[2,0] - corners[0,0]

    warped = warpImage(test.img, width)
    warped.warpImage(corners)


# Find the colors in the fixed frame to determine their position
    colorDetection = detectColor(warped.warpedImage)
    x, y = findColor(colorDetection, warped.warpedImage, "Yellow")

    xMM, yMM = getPoint(x, y, width)
    print(xMM, yMM)
    
    txt = list(map("({:.1f}, {:.1f})".format, xMM, yMM))
    
    colorDetection2 = detectColor(test.img)
    x2,y2 = findColor(colorDetection2, test.img, "Orange")
    print(x2,y2)
    colorDetection2.drawCross(test.img, x2[0], y2[0], (255,255,255), 20, str(txt[0]))
    test.showImage()


