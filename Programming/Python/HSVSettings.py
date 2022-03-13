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

        self.HLVar = tk.IntVar()
        self.HHVar = tk.IntVar()

        self.SLVar = tk.IntVar()
        self.SHVar = tk.IntVar()

        self.VLVar = tk.IntVar()
        self.VHVar = tk.IntVar()    

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


        loadButton = tk.Button(frame, text = "Load..", command = self.loadData)
        loadButton.grid(row = ROW + 4,
                   column = COL, 
                   columnspan = 3,
                   padx = padX,
                   pady = padY,
                   sticky = "NESW")

        self.CBEntries = ('Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple')
        self.CBVar = tk.StringVar()
        self.CBVar.trace('w', self.comboboxUpdated)

        self.CBVar.set(self.CBEntries[0])
        self.addComboBox(frame, ROW, 0)


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
        print(self.rows)
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
    HSVsettings(root,0,0)
    root.mainloop()