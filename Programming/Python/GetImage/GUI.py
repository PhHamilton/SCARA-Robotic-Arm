import tkinter as tk 
from tkinter import ttk
from turtle import fillcolor

from getImage import getImageClass

WIDTH = 640
HEIGHT = 480

class connectSSH():
    def __init__(self, parent, IP = None, PWD = None): 
        self.parent = parent
        if(IP == None): 
            self._IP = "192.168.1.106"
        else: 
            self._IP = IP
        if (PWD == None):
            self._PWD = "1234"
        else: 
            self._PWD = PWD

        self.padX = 5
        self.padY = 5

        self.connected = False
        self.color = "red"

        self.addIPEntry(self.parent, 0, 0)
        self.addConnectButton(self.parent, 0, 7)
        self.addLightIndication(self.parent,0,8)

        self.network = getImageClass(WIDTH, HEIGHT, None, self._IP, self._PWD, None)

    def addLightIndication(self, frame, ROW, COL): 
        size = 10
        self.canvas = tk.Canvas(frame, width = size, height = size) 
        self.connectCircle = self.canvas.create_oval(4, 4, 10, 10, fill = self.color)
        self.canvas.grid(row = ROW, column = COL, padx = self.padX, pady = self.padY)


    def caputeImage(self):
        self.network.captureImage()
        self.network.sendImage()


    def updateColor(self, state): 
        if(state== False): 
            self.color = "red"
        else: 
            self.color = "green2"

    def connect(self): 
        if(self.connected == False): 
            self.connected = self.network.connectToNetwork()
            self.button["text"] = "Disconnect"
        else: 
            self.connected = self.network.disconnect()
            self.button["text"] = "Connect"

        self.updateColor(self.connected)
        self.canvas.itemconfig(self.connectCircle, fill = self.color)

    def disconnect(self): 
        self.network.disconnect()
        self.connected = False
        self.updateColor(self.connected)

    def addConnectButton(self, frame, ROW, COL): 
        self.button = ttk.Button(frame, text = "Connect", width = 10, command = self.connect)
        self.button.grid(row = ROW, column = COL, padx = self.padX, pady = self.padY)


    def addIPEntry(self, frame,  ROW, COL): 
        self.entry0 = self.addEntry(frame, 0, 0, 3)
        self.addDot(frame, 0, 1)
        self.entry1 = self.addEntry(frame, 0, 2, 3)
        self.addDot(frame, 0, 3)
        self.entry2 = self.addEntry(frame, 0, 4, 1)
        self.addDot(frame, 0, 5)
        self.entry3 = self.addEntry(frame, 0, 6, 3)

        self.updateEntry(self.entry0, self._IP[0:3])
        self.updateEntry(self.entry1, self._IP[4:7])
        self.updateEntry(self.entry2, self._IP[8])
        self.updateEntry(self.entry3, self._IP[10:13])
    
    def addDot(self, parent, ROW, COL): 
        label = ttk.Label(parent, text = ".")
        label.grid(row = ROW, column = COL)


    def addEntry(self, parent, ROW, COL, WIDTH): 
        entry = ttk.Entry(parent, width = WIDTH)
        entry.grid(row = ROW, column = COL, padx = self.padX, pady = self.padY)
        return entry
    def updateEntry(self, entry, value): 
        entry.delete("0", tk.END)
        entry.insert("0", value)

    def updateIP(self, IP): 
        self._IP = IP

    def updatePWD(self, PWD): 
        self._PWD = PWD


    
def main():

    IP = "192.168.1.106"
    PWD = "1234"
    padX = 5
    padY = 5
    imageWidth = 640
    imageHeight = 480
    #a = getImageClass(imageWidth, imageHeight, None, IP, PWD, None)

    root = tk.Tk()
    networkFrame = ttk.LabelFrame(root)
    networkFrame.grid(row = 0, column = 0, padx = padX, pady = padY)
    nw = netWorkGUI(networkFrame, IP, PWD)
    

    canvas = tk.Canvas(root, width = imageWidth, height = imageHeight)
    canvas.grid(row = 0, column = 1, padx = padX, pady = padY)

    getImageButton = ttk.Button(root, text = "Get New Image!", command = nw.caputeImage)
    getImageButton.grid(row = 1, column = 1, padx = padX, pady = padY)

    

    root.mainloop()
if __name__ == "__main__":
    main()