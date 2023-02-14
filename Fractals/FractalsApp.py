"""
 Fractals App window based on BaseApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
from BaseApp import *
from MandelbrotSet import *

class FractalsApp(BaseApp):
    log = logging.getLogger('FractalsApp')

    def __init__(self, sTitle, sGeometry = '1200x800') -> None:
        self.oFractal = MandelbrotSet(100, 2.0)
        self.iSize = 600
        super().__init__(sTitle, sGeometry)

    def plot(self):
        self.setStatus('plot: Not implemented yet!')
        self.oImage = tk.PhotoImage(file = "../Orfact/palettes/HeatPalette.png")
        self.canPalette.create_image(self.iSize, 25, anchor=tk.CENTER, image=self.oImage)

    

    def reset(self):
        self.setStatus('reset: Not implemented yet!')

    def createWidgets(self):
        """Create user widgets"""
        btnPlot = tk.Button(master=self.frmButtons, text='Plot', command=self.plot)
        btnPlot.pack(fill=tk.X)
        btnReset = tk.Button(master=self.frmButtons, text='Reset', command=self.reset)
        btnReset.pack(fill=tk.X)

        self.frmMain.configure(bg='black')
        self.canPalette = tk.Canvas(master=self.frmMain, bg='black', bd=0, 
                                    height=50, width=1100, highlightthickness=0)
        self.canPalette.pack()
        self.canFractal = tk.Canvas(master=self.frmMain, bg='red', bd=0, 
                                    height=self.iSize, width=self.iSize, highlightthickness=0)
        self.canFractal.pack()
