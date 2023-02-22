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
from SimulationMask import *
from PolarMask import *
from TabsApp import *

class Module(TabsApp):
    log = logging.getLogger('Module')

    def __init__(self, sTitle) -> None:
        self.iImgWidth  = 600
        self.iImgHeight = 400
        self.sFilename = 'images/RandomImage00.png'
        super().__init__(sTitle, '800x500')

    def getMask(self):
        """Choose an image mask at random."""
        aMasks = [#MultiGaussImageMask(self.iImgWidth, self.iImgHeight),
                  #GaussianBlurMask(self.iImgWidth, self.iImgHeight),
                  #RandomWalkMask(self.iImgWidth, self.iImgHeight),
                  #StarFishImageMask(self.iImgWidth, self.iImgHeight),
                  #RoseWindowImageMask(self.iImgWidth, self.iImgHeight),
                  FractalMask(self.iImgWidth, self.iImgHeight)]
        oMask = random.choice(aMasks)
        return oMask
    
    def getPalette(self):
        """Choose a palette at random."""
        aPalettes = [RandomPalette(),
                     HeatPalette(),
                     FractalPalette(),
                     GhostPalette(),
                     SepiaPalette()]
        oPalette = random.choice(aPalettes)
        return oPalette

    def regenerate(self):
        """Regenerate an image and display it."""
        self.log.info('Generating random image')
        self.window.configure(cursor='watch')
        self.window.update()
        self.generateImage()
        self.displayImage()
        self.window.configure(cursor='')

    def generateImage(self):
        """Generates a random image."""
        oPal  = self.getPalette()
        oMask = self.getMask()
        sMsg = oMask.__str__() + ' rendered with ' + oPal.sName
        self.setStatus(sMsg)
        oMask.randomize()
        oMask.generate()
        oMask.toImage(oPal, self.sFilename)

    def displayImage(self):
        imgRandom = tk.PhotoImage(file=self.sFilename)
        self.lblImage.configure(image=imgRandom)
        self.lblImage.image = imgRandom

    def createWidgets(self):
        tabImg = self.addTab('Image')
        tabSet = self.addTab('Settings')
        
        # Image tab
        self.frmButtons = tk.Frame(master=tabImg, width=100, height=100)
        self.frmButtons.pack(fill=tk.Y, side=tk.LEFT)
        self.frmMain = tk.Frame(master=tabImg, width=700, bg='black')
        self.frmMain.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.addButton('Generate', self.regenerate)
        self.addButton('Exit', self.close)
        self.lblImage = tk.Label(master=self.frmMain, borderwidth=20, relief='solid', text='Image')
        self.lblImage.pack()
        
        # Settings tab 
        lfPalettes = ttk.LabelFrame(tabSet, text='Palettes')
        lfPalettes.pack(side=tk.LEFT, pady=20)
        
        aPalettes = ['RandomPalette', 'HeatPalette', 'GhostPalette', 'SepiaPalette']
        for sPal in aPalettes:
            chkPal = tk.Checkbutton(lfPalettes, text=sPal)
            chkPal.pack(fill=tk.X, anchor="w")
        
        self.displayImage()
        self.setStatus('Welcome to ' + self.sTitle)

    def addButton(self, sLabel, fnCmd):
        """Add a button with the specified label and callback."""
        btn = tk.Button(master=self.frmButtons, text=sLabel, command=fnCmd)
        btn.pack(fill=tk.X, padx=4, pady=2)
