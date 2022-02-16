
from pyzbar.pyzbar import decode

import numpy 
import cv2 

img = cv2.imread("img/QRPlate.png")
nImage = decode(img)
print(nImage)