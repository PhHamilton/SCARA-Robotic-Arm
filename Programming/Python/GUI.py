from calendar import c
import tkinter as tk 
from tkinter import ANCHOR, ttk
from warnings import filters
from ConnectSSH.connectToSSH import connectToSSH
from Server.serverThread import serverClass
from ColorRecognition.lib.ColorRecognition import detectColor
from readQRCode.readQR import QRCalibration
from readQRCode.warpImage import warpImage, QRDistance, getPoint
from HSVSettings import HSVsettings
import threading, time
from PIL import Image, ImageTk
import cv2
import numpy as np

# Global defines
padX = 5
padY = 5
canvasWidth = 648
canvasHeight = 486

class RaspberryPIConnection():
    def __init__(self, master, ROW = 0, COL = 0):
        IPFrame = tk.LabelFrame(master, text = "Network Connection")
        IPFrame.grid(row = ROW, 
                     column = COL, 
                     padx = padX, 
                     pady = padY, 
                     sticky = "NESW")

        self.host = None
        self.hostVal = tk.StringVar()
        self.hostVal.set("pi")
        self.password = None
        self.passwordVal = tk.StringVar()
        self.passwordVal.set("raspberry")

        self.IP = "192.168.1.175"
        self.connected = False
        
        self.IP01 = None
        self.IP01Val = tk.StringVar()
        self.IP01Val.set("192")
        self.IP02 = None
        self.IP02Val = tk.StringVar()
        self.IP02Val.set("168")
        self.IP03 = None
        self.IP03Val = tk.StringVar()
        self.IP03Val.set("1")
        self.IP04 = None
        self.IP04Val = tk.StringVar()
        self.IP04Val.set(175)

        ipField = tk.Frame(IPFrame)
        ipField.grid(row = 0, column = 0, columnspan = 2, padx = padX, pady = padY, sticky = "NESW")
        self.addEntryField(ipField, 0, 0)
        self.addHostNamePWD(IPFrame, 1, 0)
        self.password.configure(show = "*")
        self.updateIPEntry()
        self.button = self.addButton(IPFrame, 2, 0, "Connect..")




        self.ssh = connectToSSH(self.IP, self.hostVal.get(), self.passwordVal.get())
        self.server = serverClass('192.168.1.142')
        self.serverThread = threading.Thread(target = self.server.run)
    
    def updateHostNPWD(self, host, PWD): 
        self.host = host
        self.password = PWD

    def addButton(self, root, ROW, COL, txt):
        button = tk.Button(root, text = txt, command = self.clicked)
        button.grid(row = ROW,
                    column = COL,
                    columnspan = 2,
                    padx = padX,
                    pady = padY,
                    sticky = "NESW")

        return button

    def clicked(self): 
        if(self.connected is False):
            terminal.update("Conneting to {}".format(self.IP))
            self.button.configure(text = "Connecting..")
            self.button.configure(state = tk.DISABLED)      
            plotCanvas.canvas.delete("NSC")  
            plotCanvas.canvas.create_text(canvasWidth/2, canvasHeight/2, text = "Connecting to stream..", font = "Arial")
            plotCanvas.canvas.update_idletasks()
            self.ssh.connect()
            terminal.update("Connection established")

            self.serverThread.start()
            time.sleep(1)
            plotCanvas.startServer()
            
            self.connected = True
        else:
            terminal.update("Disconnecting..")
            terminal.update("Disconnected from stream")
            self.button.configure(text = "Connect..")
            self.connected = False
        
        self.updateIPEntry()

    def addHostNamePWD(self, root, ROW, COL): 
        self.host = self.addEntry(root, 5, ROW, COL)
        self.password = self.addEntry(root, 5, ROW, COL + 1)

    def addEntryField(self, root, ROW, COL): 
        self.IP01 = self.addEntry(root, 3, ROW + 0, COL + 0, 0, 0)
        label = tk.Label(root, text = ".").grid(row = ROW + 0, column = COL + 1)
        self.IP02 = self.addEntry(root, 3, ROW + 0, COL + 2, 0, 0)
        label = tk.Label(root, text = ".").grid(row = ROW + 0, column = COL + 3)
        self.IP03 = self.addEntry(root, 1, ROW + 0, COL + 4, 0, 0)
        label = tk.Label(root, text = ".").grid(row = ROW + 0, column = COL + 5)
        self.IP04 = self.addEntry(root, 3, ROW + 0, COL + 6, 0, 0)

    def addEntry(self, root, entryWidth, ROW, COL, padXDefault = padX, padyDefault = padY): 
        entry = tk.Entry(root, width = entryWidth)
        entry.grid(row = ROW, 
                   column = COL, 
                   padx = padXDefault,#padX, 
                   pady = padyDefault,#padY, 
                   sticky = "NESW")
        return entry

    def updateIPEntry(self): 
        self.updateEntry(self.IP01, self.IP01Val.get())
        self.updateEntry(self.IP02, self.IP02Val.get())
        self.updateEntry(self.IP03, self.IP03Val.get())
        self.updateEntry(self.IP04, self.IP04Val.get())

        self.updateEntry(self.host, self.hostVal.get())
        self.updateEntry(self.password, self.passwordVal.get())

        self.IP = self.IP01Val.get() + "." + self.IP02Val.get() + "." + self.IP03Val.get() + "." + self.IP04Val.get()

    def updateEntry(self, obj, val): 
        obj.delete(0, "end")
        obj.insert(0, val)

class plotSettings():
    def __init__(self, root, ROW = 0, COL= 0): 
        plotSettingsFrame = tk.LabelFrame(root, text = "Plot settings")
        plotSettingsFrame.grid(row = ROW, 
                        column = COL, 
                        padx = padX, 
                        pady = padY, 
                        sticky = "NESW")
            
        self.QRVar = tk.IntVar()
        self.QRVar.set(1)
        self.QRCB = self.addTextAndCheckBox(plotSettingsFrame, 
                                            "Rectangle", 
                                            self.QRVar, 
                                            ROW,
                                            COL)

        self.crossHairVar = tk.IntVar()
        self.crossHairVar.set(1)
        self.posCB = self.addTextAndCheckBox(plotSettingsFrame, 
                                            "Crosshair Position", 
                                            self.crossHairVar, 
                                            ROW+1,
                                            COL)

        self.posVar = tk.IntVar()
        self.posVar.set(1)
        self.posCB = self.addTextAndCheckBox(plotSettingsFrame, 
                                            "Item Position", 
                                            self.posVar, 
                                            ROW+2,
                                            COL)

        self.zToGrid = tk.IntVar()
        self.zToGrid.set(0)
        self.zToGridCB = self.addTextAndCheckBox(plotSettingsFrame, 
                                            "Zoom to Grid", 
                                            self.zToGrid, 
                                            ROW+3,
                                            COL)
        self.zToGridCB["state"] = tk.DISABLED




    def addTextAndCheckBox(self, root, txt, var, ROW, COL): 
        label = tk.Label(root, text = txt, anchor = tk.E).grid(row = ROW, column = COL, padx = padX, pady = padY, sticky = "NESW")
        checkBox = tk.Checkbutton(root, 
                                  variable = var,
                                  onvalue = 1,
                                  offvalue = 0)
        checkBox.grid(row = ROW, 
                      column = COL+1, 
                      padx = padX, 
                      pady = padY, 
                      sticky = "NESW")

        return checkBox
    
class plotScreen():
    def __init__(self, master, ROW = 0, COL = 0):
        self.firstImageEntry = True
        self.cornersFound = False

        plotScreenFrame = tk.LabelFrame(master, text = "Video Feed")
        plotScreenFrame.grid(row = ROW, 
                            rowspan = 3,
                            column = COL, 
                            padx = padX, 
                            pady = padY, 
                            sticky = "NESW")

        
        self.canvas = tk.Canvas(plotScreenFrame,
                           bg = "black",
                           width = canvasWidth,
                           height = canvasHeight)

        self.canvas.create_text(canvasWidth/2, canvasHeight/2, text = "No stream connected..", font = "Arial", tags = "NSC")



        self.canvas.grid(row = ROW, 
                    column = COL, 
                    padx = padX, 
                    pady = padY, 
                    sticky = "NESW")

        self.canvasThread = threading.Thread(target = lambda: self.updateCanvas(raspiConnection.server))
        

    def updateCanvas(self, server): 
        while(1):
            # try:
            if(server.newImage == True):
                img = server.getImage()
                image = Image.open(img)

                open_cv_image = np.array(image) 
                # Convert RGB to BGR 
                open_cv_image = open_cv_image[:, :, ::-1].copy() 

                getQRCorners = QRCalibration()
                getQRCorners.getImage(open_cv_image) 
                sliderVal = int(fSettings.mSlider.get())
                getQRCorners.wMsk = (sliderVal,sliderVal,sliderVal)

                if(self.cornersFound is False):
                    self.corners = getQRCorners.getCorners(img = open_cv_image)
                    if(getQRCorners.validEntries(self.corners) is True):
                        pSettings.zToGridCB.configure(state = tk.NORMAL)
                        width = self.corners[2,0] - self.corners[0,0]
                        self.cornersFound = True
                        terminal.update("QR corners found, zoom option is now available")
                else: 
                    # Check for colors: 
                    fColor = detectColor(None)
                    # Set kernel (Always the same value independent of viewing mode)
                    fColor.setKernel(10)
                    warped = warpImage(open_cv_image, width)
                    # Warp the image to get accurate position of the objects
                    warped.warpImage(self.corners)
                    # Do object decetion on the warped image
                    fColor.img = warped.warpedImage
                    # Check the lower and upper bound
                    HL, SL, VL = hsv_settings.getLowerBoundValues()
                    HH, SH, VH = hsv_settings.getUpperBoundValues()
                    fColor.setLowerBound(HL, SL, VL)
                    fColor.setUpperBound(HH, SH, VH)
                    # Find objects in the image
                    fColor.findColor()
                    x,y = fColor.getCoordinates()
                    # Removes the points outside the rectangle
                    if x:                        
                        x_filtered = [ elements for elements in x if elements > self.corners[0,0] and elements < self.corners[2,0]]
                        y_filtered = [ elements for elements in y if elements > self.corners[0,1] and elements < self.corners[2,1]]

                        # Store the x,y position in mm 
                        xMM = []
                        yMM = []
                        for i in range(len(x_filtered)):
                            try: # Solves a bug that get x_filtered out of range
                                x_converted, y_converted = getPoint(x_filtered[i], y_filtered[i], width)
                                xMM.append(x_converted)
                                yMM.append(y_converted)
                            except: 
                                pass    
                    else: 
                        # If the values does not exist, keep the filtered values empty
                        x_filtered = x
                        y_filtered = y

                    if(pSettings.zToGrid.get() == 1):
                        # If we are zoomed in
                        img = warped.warpedImage
                        # Draw cross and the corresponding position if a point exist
                        if(len(x_filtered) > 0):
                            for i in range(len(xMM)):
                                txt = "({:.1f}, {:.1f})".format(xMM[i], yMM[i])
                                fColor.drawCross(img, x_filtered[i], y_filtered[i], (255,0,0), 20, txt)

                        # Configure settings for plot
                        xPos = (canvasWidth - canvasHeight)/2
                        cWidth = canvasHeight
                        cHeight = canvasHeight

                    else:
                        # If we are zoomed out 
                        img = open_cv_image
                        # We need to detect the colors again
                        fColor.img = img
                        # This might cause an error if the points are discovered in another order
                        fColor.findColor()
                        x,y = fColor.getCoordinates()
                        # Removes the points outside the rectangle
                        if x:
                            x_filtered = [ elements for elements in x if elements > self.corners[0,0] and elements < self.corners[2,0]]
                            y_filtered = [ elements for elements in y if elements > self.corners[0,1] and elements < self.corners[2,1]]
                        else: 
                            x_filtered = x
                            y_filtered = y

                        if(len(x_filtered) > 0):
                            for i in range(len(xMM)):
                                try:
                                    txt = "({:.1f}, {:.1f})".format(xMM[i], yMM[i])
                                    fColor.drawCross(fColor.img, x_filtered[i], y_filtered[i], (255,0,0), 20, txt)
                                except:
                                    print("Did not find the correct location")
                        # Configure settings for plot 
                        xPos = 0
                        cWidth = canvasWidth
                        cHeight = canvasHeight
                        img = getQRCorners.img
                        if(pSettings.QRVar.get() == 1):
                            getQRCorners.drawRectangle(img, self.corners)

                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                    # Convert image for drawing it in the Canvas
                    im_pil = Image.fromarray(img)

                    testImage = ImageTk.PhotoImage(image = im_pil.resize((cWidth,cHeight)))

                    self.canvas.create_image(xPos,0,anchor=tk.NW,image=testImage)

                    if(self.firstImageEntry == True):
                        raspiConnection.button.configure(state = tk.NORMAL)
                        raspiConnection.button.configure(text = "Disconnect..")
                        self.firstImageEntry = False

            time.sleep(1)
    def startServer(self): 
        self.canvasThread.start()


class filterSettings():
    def __init__(self, root, ROW = 0, COL= 0): 
        filterSettingsFrame = tk.LabelFrame(root, text = "Filter settings")
        filterSettingsFrame.grid(row = ROW, 
                        column = COL, 
                        padx = padX, 
                        pady = padY, 
                        sticky = "NESW")
        self.wMaskVal = tk.StringVar()                
        label = tk.Label(filterSettingsFrame, text = "Mask:").grid(row = ROW+2, column = COL, padx = padX, pady = padY, sticky = "NESW") 
        self.mSlider = self.addSlider(filterSettingsFrame, ROW+2, COL+1, 100, 120, self.wMaskVal, 100)

    def addSlider(self, root, ROW, COL,  minVal, maxVal, var, defaultValue = 0): 
        slider = tk.Scale(root, 
                          from_ = minVal, 
                          to = maxVal, 
                          variable = var,
                          resolution  = 1,
                          orient = tk.HORIZONTAL,
                          length = 120,
                          )

        slider.set(defaultValue)                          
        slider.grid(row = ROW, 
                    column = COL, 
                    padx = padX, 
                    pady = padY, 
                    sticky = "NESW")
        return slider
            

class terminalScreen():
    def __init__(self, master, ROW = 0, COL = 0):
        terminalFrame = tk.LabelFrame(master, text = "Terminal Output")
        terminalFrame.grid(row = ROW, 
                            column = COL, 
                            padx = padX, 
                            pady = padY, 
                            sticky = "NESW")

        self.textField = tk.Text(terminalFrame, height = 5, width = 92)
        self.textField.grid(row = ROW, 
                            column = COL, 
                            padx = padX, 
                            pady = padY, 
                            sticky = "NESW")
        self.consoleList = []


    def update(self, txt): 
        self.consoleList.insert(0, txt)
        listLen = len(self.consoleList)
        self.textField.delete("1.0", tk.END)
        for i in range(listLen):
            self.textField.insert(tk.INSERT, self.consoleList[i] + '\n')


if __name__ == "__main__": 
    root = tk.Tk()

    # Console added first to be able to access it from the other classes
    terminal = terminalScreen(root,4,1)
    hsv_settings = HSVsettings(root, 1)
    pSettings = plotSettings(root, 2)
    fSettings = filterSettings(root,4)

    raspiConnection = RaspberryPIConnection(root)
    
    plotCanvas = plotScreen(root, 0, 1)
    
    
    root.mainloop()

    
    
    
    