import tkinter as tk 
from tkinter import StringVar, ttk

padX = 5
padY = 5


 
class HSVsettings(): 
    def __init__(self, master, ROW, COL = 0): 
        frame = tk.LabelFrame(master, text = "HSV Settings")
        frame.grid(row = ROW,
                   column = COL, 
                   padx = padX,
                   pady = padY,
                   sticky = "NESW")

        self.HLVar = tk.StringVar()
        self.HHVar = tk.StringVar()


        self.SLVar = tk.StringVar()
        self.SHVar = tk.StringVar()


        self.VLVar = tk.StringVar()
        self.VHVar = tk.StringVar()    


        self.rows = None
        
        ROW += 1

        labelH = tk.Label(frame, text = "Low")
        labelH.grid(row = ROW,
                   column = COL + 1, 
                   padx = padX,
                   pady = padY,
                   sticky = "NESW")

        labelL = tk.Label(frame, text = "High")
        labelL.grid(row = ROW,
                   column = COL+2, 
                   padx = padX,
                   pady = padY,
                   sticky = "NESW")

        labelH = tk.Label(frame, text = "H")
        labelH.grid(row = ROW + 1,
                   column = COL, 
                   padx = padX,
                   pady = padY,
                   sticky = "NESW")

        self.HL = self.createEntry(frame, self.HLVar, ROW +1, COL+1)
        self.HH = self.createEntry(frame, self.HHVar, ROW +1, COL+2)

        labelS = tk.Label(frame, text = "S")
        labelS.grid(row = ROW + 2,
                   column = COL, 
                   padx = padX,
                   pady = padY,
                   sticky = "NESW")

        self.SL = self.createEntry(frame, self.SLVar, ROW +2, COL+1)
        self.SH = self.createEntry(frame, self.SHVar, ROW +2, COL+2)

        labelV = tk.Label(frame, text = "V")
        labelV.grid(row = ROW + 3,
                   column = COL, 
                   padx = padX,
                   pady = padY,
                   sticky = "NESW")

        self.VL = self.createEntry(frame, self.VLVar, ROW +3, COL+1)
        self.VH = self.createEntry(frame, self.VHVar, ROW +3, COL+2)


        self.CBEntries = ('Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple')
        self.CBVar = tk.StringVar()
        self.CBVar.trace('w', self.comboboxUpdated)

        self.CBVar.set(self.CBEntries[0])
        self.addComboBox(frame, ROW, 0)
        self.loadData()
        loadButton = tk.Button(frame, text = "Update..", command = self.updateCboxValues)
        loadButton.grid(row = ROW + 4,
                   column = COL, 
                   columnspan = 3,
                   padx = padX,
                   pady = padY,
                   sticky = "NESW")


    def getLowerBoundValues(self):
        if self.HLVar.get() == "": 
            self.HLVar.set(0)
        if self.VLVar.get() == "": 
            self.VLVar.set(0)
        if self.VLVar.get() == "": 
            self.VLVar.set(0)

        return int(self.HLVar.get()), int(self.SLVar.get()), int(self.VLVar.get())
    def getUpperBoundValues(self):
        if self.HHVar.get() == "": 
            self.HLHVar.set(0)
        if self.VLVar.get() == "": 
            self.VHVar.set(0)
        if self.VHVar.get() == "": 
            self.VHVar.set(0)
        return int(self.HHVar.get()), int(self.SHVar.get()), int(self.VHVar.get())

    def comboboxUpdated(self, index, value, op):
        idx = self.CBEntries.index(self.CBVar.get())

        self.HLVar.set(self.rows[7*idx + 0])
        self.HHVar.set(self.rows[7*idx + 1])

        self.SLVar.set(self.rows[7*idx + 2])
        self.SHVar.set(self.rows[7*idx + 3])

        self.VLVar.set(self.rows[7*idx + 4])
        self.VHVar.set(self.rows[7*idx + 5])

        self.updateCboxValues()

    
    def updateCboxValues(self):
        self.updateEntry(self.HL, self.HLVar.get())
        self.updateEntry(self.HH, self.HHVar.get())
        self.updateEntry(self.VL, self.VLVar.get())
        self.updateEntry(self.VH, self.VHVar.get())
        self.updateEntry(self.SL, self.SLVar.get())
        self.updateEntry(self.SH, self.SHVar.get())


    def updateEntry(self, obj, val): 
        obj.delete(0, "end")
        obj.insert(0, val)
        

    def loadData(self): 
        localPath = "/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/HSVParameters/Default.txt"
        with open(localPath, 'r') as f: 
            self.rows = f.read().splitlines()
        f.close()

        self.comboboxUpdated(0,0,0) #MIGHT CAUSE AN ISSUE! UNKNOWN EFFECT OF INPUT VALUES!


    def createEntry(self, root, var, ROW, COL): 
        entry = tk.Entry(root, textvariable = var, width = 3)
        entry.grid(row = ROW,
                   column = COL, 
                   padx = padX,
                   pady = padY,
                   sticky = "NESW")

        return entry

    def addComboBox(self, root, ROW, COL):
        cBox = ttk.Combobox(root, 
                            textvariable = self.CBVar,
                            values = self.CBEntries,
                            width = 15,
                            state = "readonly")
        cBox.set(self.CBEntries[0])
        cBox.grid(row = ROW, 
                  column = COL, 
                  columnspan = 3, 
                  padx = padX, 
                  pady = padY, 
                  sticky = "NESW")    

if __name__ == '__main__':
    root = tk.Tk()
    a = HSVsettings(root,0,0)
    print(a.getUpperBoundValues())
    root.mainloop()