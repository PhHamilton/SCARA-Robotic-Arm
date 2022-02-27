from calendar import c
import tkinter as tk 
from tkinter import ANCHOR, ttk
from ConnectSSH.connectToSSH import connectToSSH
from Server.serverThread import serverClass
from ColorRecognition.lib.ColorRecognition import detectColor
from readQRCode.readQR import QRCalibration
from readQRCode.warpImage import warpImage, QRDistance
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
        self.server = serverClass('192.168.1.143')
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

class HSVsettings():
    def __init__(self, master, ROW = 0, COL = 0): 
        HSVSettings = tk.LabelFrame(master, text = "HSV Color Settings")
        HSVSettings.grid(row = ROW, 
                     column = COL, 
                     padx = padX, 
                     pady = padY, 
                     sticky = "NESW")

        self.CBEntries = ('Red', 'Blue', 'Green')
        self.CBVar = tk.StringVar()

        
        self.HVal = None
        self.SVal = None
        self.VVal = None
        self.addComboBox(HSVSettings, 0, 0)
        sliderFrame = tk.Frame(HSVSettings)
        sliderFrame.grid(row = ROW+1, 
                     column = COL, 
                     columnspan = 2,
                     padx = padX, 
                     pady = padY, 
                     sticky = "NESW")
        self.addHSVSliders(sliderFrame, 1, 0)

        button = tk.Button(sliderFrame, text = "Save..")
        button.grid(row = 4, 
                     column = COL+1, 
                     padx = padX, 
                     pady = padY, 
                     sticky = "NESW")

    def addHSVSliders(self, root, ROW, COL):
        label = tk.Label(root, text = "H:").grid(row = ROW, column = COL, padx = padX, pady = padY, sticky = "NESW") 
        self.addSlider(root, ROW, COL+1, 0, 180)

        label = tk.Label(root, text = "S:").grid(row = ROW+1, column = COL, padx = padX, pady = padY, sticky = "NESW") 
        self.addSlider(root, ROW+1, COL+1, 0, 255)

        label = tk.Label(root, text = "V:").grid(row = ROW+2, column = COL, padx = padX, pady = padY, sticky = "NESW") 
        self.addSlider(root, ROW+2, COL+1, 0, 255)

    def addSlider(self, root, ROW, COL,  minVal, maxVal, defaultValue = 0): 
        slider = tk.Scale(root, 
                          from_ = minVal, 
                          to = maxVal, 
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

    def addComboBox(self, root, ROW, COL):
        cBox = ttk.Combobox(root, 
                            textvariable = self.CBVar,
                            values = self.CBEntries,
                            width = 15,
                            state = "readonly")
        cBox.set(self.CBEntries[1])
        cBox.grid(row = ROW, 
                  column = COL, 
                  padx = padX, 
                  pady = padY, 
                  sticky = "NESW")

class plotSettings():
    def __init__(self, root, ROW = 0, COL= 0): 
        plotSettingsFrame = tk.LabelFrame(root, text = "Plot settings")
        plotSettingsFrame.grid(row = ROW, 
                        rowspan = 2,
                        column = COL, 
                        padx = padX, 
                        pady = padY, 
                        sticky = "NESW")
            
        self.QRVar = tk.IntVar()
        self.QRVar.set(1)
        self.QRCB = self.addTextAndCheckBox(plotSettingsFrame, 
                                            "QR Rectangles", 
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
                                            "Zoom to Grid Position", 
                                            self.zToGrid, 
                                            ROW+3,
                                            COL)




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
                getQRCorners.wMsk = (80,80,80)
                if(self.cornersFound is False):
                    self.corners = getQRCorners.getCorners(img = open_cv_image)
                    if(getQRCorners.validEntries(self.corners) is True):
                        self.cornersFound = True
                getQRCorners.getImage(open_cv_image)
                
                if(pSettings.zToGrid.get() == 1):
                    width = self.corners[2,0] - self.corners[0,0]

                    warped = warpImage(getQRCorners.img, width)
                    warped.warpImage(self.corners)
                    img = cv2.cvtColor(warped.warpedImage, cv2.COLOR_BGR2RGB)
                    xPos = (canvasWidth - canvasHeight)/2
                    cWidth = canvasHeight
                    cHeight = canvasHeight
                else: 
                    xPos = 0
                    cWidth = canvasWidth
                    cHeight = canvasHeight
                    getQRCorners.drawRectangle(getQRCorners.img, self.corners)
                    img = cv2.cvtColor(getQRCorners.img, cv2.COLOR_BGR2RGB)

                im_pil = Image.fromarray(img)

                        # For reversing the operation:
                im_np = np.asarray(im_pil)

                testImage = ImageTk.PhotoImage(image = im_pil.resize((cWidth,cHeight)))
                    # except: 
                    #     testImage = ImageTk.PhotoImage(image = image.resize((canvasWidth,canvasHeight)))

                self.canvas.create_image(xPos,0,anchor=tk.NW,image=testImage)

                if(self.firstImageEntry == True):
                    raspiConnection.button.configure(state = tk.NORMAL)
                    raspiConnection.button.configure(text = "Disconnect..")
                    self.firstImageEntry = False
            # except:
            #     print("No image available")
            time.sleep(1)
    def startServer(self): 
        self.canvasThread.start()

class terminalScreen():
    def __init__(self, master, ROW = 0, COL = 0):
        terminalFrame = tk.LabelFrame(master, text = "Terminal Output")
        terminalFrame.grid(row = ROW, 
                            column = COL, 
                            padx = padX, 
                            pady = padY, 
                            sticky = "NESW")

        self.textField = tk.Text(terminalFrame, height = 5)
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

    raspiConnection = RaspberryPIConnection(root)
    HSVsettings(root, 1)
    pSettings = plotSettings(root, 2)
    plotCanvas = plotScreen(root, 0, 1)
    
    root.mainloop()

    
    
    
    