from readQRCode.readQR import QRCalibration
from readQRCode.warpImage import warpImage, setPoint

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
    obj.drawCross(img, x, y, crosshairColor, 20)

if __name__ == "__main__": 
    path = r'/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/readQRCode/img/testWColors.jpg'
    test = QRCalibration()
    corners = test.getCorners(path)
    
    width = corners[2,0] - corners[0,0]
    # # height = corners[1,1] - corners[0,1]

    warped = warpImage(test.img, width)
    warped.warpImage(corners)

    # setPoint(10, -40, warped.warpedImage, width)
    colorDetection = detectColor(path)
    findColor(colorDetection, warped.warpedImage, "Blue")

    # colorDetection.setName("Blue")
    # colorDetection.setLowerBound(90,50,50)
    # colorDetection.setUpperBound(130,255,255)
    # colorDetection.setKernel(10)
    # colorDetection.findColor()
    # x,y = colorDetection.getCoordinates()
    # colorDetection.drawCross(warped.img,x, y, (255,255,255), 20)
    warped.showImage()
    cv2.imshow(colorDetection.name, warped.warpedImage)
    cv2.waitKey(0)
    # test.showImage()
    # warped.showImage()