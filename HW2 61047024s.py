import tkinter as tk
from tkinter import *
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self.canvas = None
        
    def LeftImage(self, image, event):
        if event == 'histogram':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (350,350))
            image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
#參考https://stackoverflow.com/questions/3482081/how-to-update-the-image-of-a-tkinter-label-widget   
            self.Left.configure(image=image)
            self.Left.image = image
            self.Left.pack(side="left")
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
            image = cv2.resize(image, (350,350))
            image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
            self.Left = Label(image=image)
            self.Left.image = image
            self.Left.pack(side="left")
        
    def RightImage(self, image, event):
#https://www.cnblogs.com/brightyuxl/p/9832248.html
#https://www.itranslater.com/qa/details/2106581108069499904
#https://blog.gtwang.org/programming/python-opencv-matplotlib-plot-histogram-tutorial/
        if event == "histogram":
            self.Right.destroy()
            self.Right = Figure(figsize=(3.5, 3.5), dpi=100)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            plot = self.Right.add_subplot(111)
            plot.title.set_text('Histogram')
            plot.hist(image.ravel(), 256, [0, 256])
            self.canvas = FigureCanvasTkAgg(self.Right, master = window)
            self.canvas.get_tk_widget().pack(side="right", padx=5, pady=5)

        else:
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
            self.LeftImage(image,"original")
            self.RightImage(image,"original")
#參考https://vimsky.com/zh-tw/examples/detail/python-method-tkinter.filedialog.asksaveasfilename.html
    def download(self):
        saveFileName = filedialog.asksaveasfilename()
        extensionFileName = os.path.splitext(saveFileName)[-1].upper() if (os.path.splitext(saveFileName)[-1]) else ".JPG"
        cv2.imencode(extensionFileName, self.image)[1].tofile(saveFileName if (os.path.splitext(saveFileName)[-1]) else (saveFileName + extensionFileName))

    def histogram(self):
        self.LeftImage(self.image,"histogram")
        self.RightImage(self.image,"histogram")
        

#參考https://shengyu7697.github.io/python-tkinter-button/
#https://ithelp.ithome.com.tw/articles/10228097            
def main():
    imageProcessing = ImageProcessing()
    button_frame = Frame(window)
    button_frame.pack(side=TOP)
    mybutton = Button(button_frame, text='選擇影像', bg='yellow',command=imageProcessing.button_event)
    mybutton.pack(side=LEFT)
    mybutton1 = tk.Button(button_frame, text='下載影像', bg='red',command=imageProcessing.download)
    mybutton1.pack(side=LEFT)
    mybutton2 = tk.Button(button_frame, text='直方圖', bg='red',command=imageProcessing.histogram)
    mybutton2.pack(side=LEFT)
    window.mainloop()
    
if __name__ == '__main__':
    main()

