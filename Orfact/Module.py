"""
GUI tests using Tkinter.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
from Palette import *
from ImageMask import *
from PolarMask import *

class Module:
    log = logging.getLogger('Module')

    def __init__(self, sTitle) -> None:
        self.log.info('Creating top-level frame %s', sTitle)
        self.window = tk.Tk()
        self.window.title(sTitle)
        self.window.geometry('800x500')
        self.createWidgets()
        self.displayImage()
        self.window.mainloop()
        self.log.info('Goodbye!')

    def onClick(self):
        self.log.info('Generating random image')
        self.generateImage()
        self.displayImage()

    def close(self):
        self.window.destroy()

    def generateImage(self):
        oPal = RandomPalette()
        oMask = RoseWindowImageMask(600, 400)
        oMask.randomize()
        oMask.generate()
        sFilename = 'images/RandomImage00.png'
        oMask.toImage(oPal, sFilename)

    def displayImage(self):
        imgRandom = tk.PhotoImage(file="images/RandomImage00.png")
        self.lblImage.configure(image=imgRandom)
        self.lblImage.image = imgRandom

    def createWidgets(self):
        frame1 = tk.Frame(master=self.window, width=100, height=100, bg="black")
        frame1.pack(fill=tk.Y, side=tk.LEFT)
        frame2 = tk.Frame(master=self.window, width=700, bg="black")
        frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        btnGen = tk.Button(master=frame1, text='Generate', command=self.onClick)
        btnGen.pack()
        btnExit = tk.Button(master=frame1, text='Exit', command=self.close)
        btnExit.pack()
        self.lblImage = tk.Label(master=frame2, text='Image')
        self.lblImage.pack()



    

