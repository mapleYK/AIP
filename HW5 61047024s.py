import tkinter as tk
from tkinter import *
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import random
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#參考https://www.itread01.com/content/1547705544.html
window = tk.Tk()
window.title('AIP 61047024S')
window.geometry('1000x550')
window.resizable(width=False, height=False)

#https://www.delftstack.com/zh-tw/howto/python-tkinter/how-to-create-a-new-window-with-a-button-in-tkinter/
#https://jennaweng0621.pixnet.net/blog/post/403560362-%5Bpython%5D-tkinter-%E6%96%87%E5%AD%97%E6%A1%86%28entry%29
class msgbox:
    def __init__(self, parent,text):
        self.sd = None

        self.top = Toplevel(parent)
        self.top.geometry('300x50')
        self.top.resizable(width=False, height=False)

        self.label = Label(self.top, text=text, fg='#000000').pack(side=LEFT)
        self.entry = Entry(self.top)
        self.entry.pack(padx=5, side=LEFT)
        self.button = Button(self.top, text='確定', command=self.send).pack(side=LEFT)
 
    def send(self): 
        self.sd = self.entry.get()
        self.top.destroy()

#參考https://www.locks.wiki/a_keji/202106/197725.html
class ImageProcessing:
    def __init__(self):
        self.Left = None
        self.Right = None
        self.Right2 = None
        self.image = None
        self.fname = None
        self.canvas = None
        self.size = None
        self.Left_frame = None
        self.Left_HE = None
        self.Left_canvas = None
        self.Right_frame = None
        self.Right_HE = None
        self.Right_canvas = None

    def LeftImage(self, image, event):
        if event == "HistogramEqualization":
            self.Left.destroy()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (512,256))
            PILImage = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))

            self.Left_frame = Frame(window)
            self.Left_frame.pack(side="left")
            self.Left = Label(self.Left_frame, image=PILImage,width=512,height=256)
            self.Left.image = PILImage
            self.Left.grid(row=1, column=1)
            self.Left_HE = Figure(figsize=(5.1, 2.5), dpi=100)
            plot = self.Left_HE.add_subplot(111)
            plot.title.set_text('Histogram')
            plot.bar(range(1,257), [x[0] for x in iter(list(cv2.calcHist([image], [0], None, [256], [0, 256])))])
            self.Left_canvas = FigureCanvasTkAgg(self.Left_HE, self.Left_frame)
            self.Left_canvas.get_tk_widget().grid(row=2, column=1, padx=10, pady=5)
      
        elif event == 'histogram' or event == 'gaussian' or event == 'wavelet':
            if event != "gaussian":
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image = cv2.resize(image, (512,512))
            image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
#參考https://stackoverflow.com/questions/3482081/how-to-update-the-image-of-a-tkinter-label-widget   
            self.Left.configure(image=image)
            self.Left.image = image
            self.Left.pack(side="left")

        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
            image = cv2.resize(image, (512,512))
            image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
            self.Left = Label(image=image)
            self.Left.image = image
            self.Left.pack(side="left")
        
    def RightImage(self, image, event):
#https://www.cnblogs.com/brightyuxl/p/9832248.html
#https://www.itranslater.com/qa/details/2106581108069499904
#https://blog.gtwang.org/programming/python-opencv-matplotlib-plot-histogram-tutorial/
        if event == "HistogramEqualization":
            self.Right.destroy()
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (512,256))
            PILImage = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(image))
            
            self.Right_frame = Frame(window)
            self.Right_frame.pack(side="right")
            self.Right = Label(self.Right_frame, image=PILImage,width=512,height=256)
            self.Right.image = PILImage
            self.Right.grid(row=1, column=1)
            self.Right_HE = Figure(figsize=(5.1, 2.5), dpi=100)
            plot = self.Right_HE.add_subplot(111)
            plot.title.set_text('Histogram')
            plot.bar(range(1,257), [x[0] for x in iter(list(cv2.calcHist([image], [0], None, [256], [0, 256])))])
            self.Right_canvas = FigureCanvasTkAgg(self.Right_HE, self.Right_frame)
            self.Right_canvas.get_tk_widget().grid(row=2, column=1, padx=10, pady=5)

        elif event == "histogram" or event == "gaussian":
            self.Right.destroy()
            self.Right = Figure(figsize=(3.5, 3.5), dpi=100)
            if event != "gaussian":
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            plot = self.Right.add_subplot(111)
            plot.title.set_text('Histogram')
            plot.hist(image.ravel(), 256, [0, 256])
            self.canvas = FigureCanvasTkAgg(self.Right, master = window)
            self.canvas.get_tk_widget().pack(side="right", padx=5, pady=5)

        else:
            if event == 'wavelet':
                self.Right.destroy()
            if event != 'wavelet':
                self.image = image
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
                image = cv2.resize(image, (512,512))
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

    def Gaussian(self):
        G = 256
        get_sd = msgbox(window,'標準差:')
        window.wait_window(get_sd.top)

        image = self.image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (512,512))

        new = np.zeros((350, 350), np.uint8)

#https://stackoverflow.com/questions/33359740/random-number-between-0-and-1-in-python
        for i in range(0,350):
            for j in range(0,350,2):
                r1 = random.random()
                r2 = random.random()

                z1 =  int(get_sd.sd) *np.cos(2 * np.pi * r2) * np.sqrt((-2) * np.log(r1))
                z2 = int(get_sd.sd) * np.sin(2 * np.pi * r2) * np.sqrt((-2) * np.log(r1))
                
                f1 = int(image[i, j] + z1)
                f2 = int(image[i, j + 1] + z2)

                if f1 < 0:
                    new[i,j] = 0
                elif f1 > G-1:
                    new[i,j] = G-1
                else:
                    new[i,j] = f1

                if f2 < 0:
                    new[i,j+1] = 0
                elif f2 > G-1:
                    new[i,j+1] = G-1
                else:
                    new[i,j+1] = f2

        self.LeftImage(new, "gaussian")
        self.RightImage(new, "gaussian")



    def wavelet(self):
        get_ans = msgbox(window, '請輸入層數:')
        window.wait_window(get_ans.top)

        image = self.image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (512,512))
        self.size = list(image.shape)
#https://blog.csdn.net/u010758410/article/details/71554224
        self.Right2 = np.zeros((self.size[0], self.size[1]))
        for i in range(0, int(get_ans.sd)):
            if i == 0:
                self.haar(image)
            else:
                self.haar(self.Right2)
            # set left image
        self.LeftImage(self.image, "wavelet")
        # set Right image
        self.RightImage(self.Right2, "wavelet")

    def haar(self, image):

        height = int(self.size[0] / 2)
        width = int(self.size[1] / 2)

        LL = np.zeros((height, width))
        LH = np.zeros((height, width))
        HH = np.zeros((height, width))
        HL = np.zeros((height, width))
        Lowpass = np.zeros((self.size[0], width))
        Highpass = np.zeros((self.size[0], width))

        for i in range (0, self.size[0]):
            for j in range(0, self.size[1], 2):
                Lowpass[i, int(j/2)] = int((image[i, j] / 2) + (image[i, j+1] / 2))
                Highpass[i, int(j/2)] = image[i, j] - Lowpass[i, int(j/2)]
        
        for i in range (0, Lowpass.shape[0], 2):
            for j in range(0, Lowpass.shape[1]):
                LL[int(i/2), j] = int((Lowpass[i, j]/2) + (Lowpass[i+1, j]/2))
                LH[int(i/2), j] = int((Lowpass[i, j]) - LL[int(i/2), j])
                HH[int(i/2), j] = int((Highpass[i, j]/2) - Highpass[i+1, j]/2)
                HL[int(i/2), j] = int(Highpass[i, j] - HH[int(i/2), j])
        
        
        LH[LH < 0] = 0
        LH = cv2.normalize(LH, None, 0, 255, cv2.NORM_MINMAX)
        HL[HL < 0] = 0
        HL = cv2.normalize(HL, None, 0, 255, cv2.NORM_MINMAX)
        HH[HH < 0] = 0
        HH = cv2.normalize(HH, None, 0, 255, cv2.NORM_MINMAX)

        self.Right2[0:height, 0:width] = LL[:,:]
        self.Right2[height:self.size[0], 0:width] = HL[:,:]
        self.Right2[0:height, width:self.size[1]] = LH[:,:]
        self.Right2[height:self.size[0], width:self.size[1]] = HH[:,:]

        self.size[0] = int(self.size[0] / 2)
        self.size[1] = int(self.size[1] / 2)

#https://codeinfo.space/imageprocessing/histogram-equalization/
    def HistogramEqualization(self):
        image = self.image
        image = cv2.resize(image, (512,512))
        hist, bins = np.histogram(image, 256)
        cdf = hist.cumsum()
        cdf = (cdf-cdf[0])*255/(cdf[-1]-1)
        cdf = cdf.astype(np.uint8)
        result = np.zeros((384, 495, 1), dtype =np.uint8)
        result = cdf[image]

        self.LeftImage(self.image, "HistogramEqualization")
        self.RightImage(result, "HistogramEqualization")

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
    mybutton3 = tk.Button(button_frame, text='高斯雜訊', bg='red',command=imageProcessing.Gaussian)
    mybutton3.pack(side=LEFT)
    mybutton4 = tk.Button(button_frame, text='小波轉換', bg='red',command=imageProcessing.wavelet)
    mybutton4.pack(side=LEFT)
    mybutton5 = tk.Button(button_frame, text='直方圖均化', bg='red',command=imageProcessing.HistogramEqualization)
    mybutton5.pack(side=LEFT)
    window.mainloop()
    
if __name__ == '__main__':
    main()

