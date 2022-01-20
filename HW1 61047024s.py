import tkinter as tk
from tkinter import *
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import os

#參考https://www.itread01.com/content/1547705544.html
window = tk.Tk()
window.title('AIP 61047024S')
window.geometry('1000x550')
window.resizable(width=False, height=False)

#參考https://www.locks.wiki/a_keji/202106/197725.html
class ImageProcessing:
    def __init__(self):
        self.Left = None
        self.Right = None
        self.image = None
        self.fname = None
        
        
    def LeftImage(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        image = cv2.resize(image, (350,350))
        image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
        self.Left = Label(image=image)
        self.Left.image = image
        self.Left.pack(side="left")
        
    def RightImage(self, image):
        self.image = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        image = cv2.resize(image, (350,350))
        image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
        self.Right = Label(image=image)
        self.Right.image = image
        self.Right.pack(side="right")

    def button_event(self):
        self.fname = filedialog.askopenfilename()
        if len(self.fname) > 0:
            image = cv2.imdecode(np.fromfile(self.fname, dtype=np.uint8), 1)
            self.LeftImage(image)
            self.RightImage(image)
#參考https://vimsky.com/zh-tw/examples/detail/python-method-tkinter.filedialog.asksaveasfilename.html
    def download(self):
        saveFileName = filedialog.asksaveasfilename()
        extensionFileName = os.path.splitext(saveFileName)[-1].upper() if (os.path.splitext(saveFileName)[-1]) else ".JPG"
        cv2.imencode(extensionFileName, self.image)[1].tofile(saveFileName if (os.path.splitext(saveFileName)[-1]) else (saveFileName + extensionFileName))
        

#參考https://shengyu7697.github.io/python-tkinter-button/            
def main():
    imageProcessing = ImageProcessing()
    mybutton = tk.Button(window, text='選擇影像', bg='yellow',command=imageProcessing.button_event)
    mybutton.pack()
    mybutton = tk.Button(window, text='下載影像', bg='red',command=imageProcessing.download)
    mybutton.pack()
    window.mainloop()
    
if __name__ == '__main__':
    main()

