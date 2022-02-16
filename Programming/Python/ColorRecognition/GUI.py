import tkinter as tk
from lib.ColorRecognition import detectColor



def GUI():
    def __init__(self): 
        self.root = tk.Tk()
        self.root.title("Image")

        width = 257 
        height = 260
        self.imageFrame = tk.Canvas(self.root, width = width, height = height)
        self.imageFrame.grid(row = 0, column = 0, sticky = "nesw")

    def HSVSliders(self,)

    def run(self):
        self.root.mainloop()

    # def run(self):
    #     self.root.mainloop() 


    
if __name__ == "__main__":
    imgPath = "/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/Color Recognition/images/colors.jpg"
    a = detectColor(imgPath)
    
    a.setName("Blue")
    a.setLowerBound(90,50,50)
    a.setUpperBound(130,255,255)
    a.setKernel(10)

    a.findColor()
    a.showFilteredimage()

    root = tk.Tk()
    imageFrame = tk.Canvas(root, width = 257, height = 260)
    imageFrame.pack()
    # img = tk.PhotoImage(file = "/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/Color Recognition/images/colors.jpg")
    # imageFrame.create_image(0,0, anchor = "nw", image = img)

    root.mainloop()