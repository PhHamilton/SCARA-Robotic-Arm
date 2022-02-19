import io
import socket
import struct
from PIL import Image, ImageTk
import cv2
import numpy as np

import threading
import time


import tkinter as tk

class serverClass():
    def __init__(self, IP, SOCKET = 8000): 
        self.server_socket = socket.socket()
        self.server_socket.bind((IP, 8000))  # ADD IP HERE
        
        self.startServer = True
        self.firstEntry = True
        self.image = None
        self.newImage = False
    
    def run(self): 
        if(self.firstEntry is True): 
            self.server_socket.listen(0)
            # Accept a single connection and make a file-like object out of it
            self.connection = self.server_socket.accept()[0].makefile('rb')
            self.firstEntry = False
        try: 
            print("Thread started")
            while(self.startServer is True): 
                image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(self.connection.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
                image_stream.seek(0)
                self.image = image_stream

                self.newImage = True


                # self.image = Image.open(image_stream)
                # self.image.show()

                # self.cv2Image = np.array(image) 
                # # Convert RGB to BGR 
                # self.cv2Image = self.cv2Image[:, :, ::-1].copy() 
        
                # # cv2.imshow("Image", cv2Image)
                # # cv2.waitKey(500)


                # print('Image is %dx%d' % self.image.size)
                # self.image.verify()

                # print('Image is verified')
        
            self.connection.close()
            self.server_socket.close()
        except: 
            print("Thread creation failed")
    
    def getImage(self): 
        self.newImage = False
        return self.image

def updateCanvas(): 
    while(1):
        try:
            if(server.newImage == True):
                img = server.getImage()
                image = Image.open(img)
                testImage = ImageTk.PhotoImage(image = image.resize((600,600)))
                canvas.create_image(0,0,anchor=tk.NW,image=testImage)
                # canvas.create_image(img = ImageTk.PhotoImage(Image.open(img)))
                # print(img)
            
            # img = ImageTk.PhotoImage(server.image)
            # canvas.create_image(image = img)
        except:
            print("No image available")
        time.sleep(1)
if __name__ == '__main__':
    IP = '192.168.1.143'

    server = serverClass(IP)

    thread = threading.Thread(target = server.run)
    thread.start()

    thread2 = threading.Thread(target = updateCanvas)

    root = tk.Tk()
    root.geometry("800x800")
    canvas = tk.Canvas(root, width = 648, height = 800)
    canvas.grid(row = 0, column = 0, sticky = "NESW")


    thread2.start()
    root.mainloop()