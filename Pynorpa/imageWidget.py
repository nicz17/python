"""
Tkinter image widget module.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from picture import Picture
from BaseWidgets import Button


class ImageWidget():
    """A widget displaying an image from a file."""
    log = logging.getLogger('ImageWidget')

    def __init__(self, defImage = None):
        """Constructor"""
        self.log.info('Constructor')
        self.defImage = defImage

    def loadData(self, filename: str):
        """Display the specified image if it exists."""
        if filename and os.path.exists(filename):
            img = ImageTk.PhotoImage(Image.open(filename))
            self.lblImage.configure(image=img)
            self.lblImage.image = img
        else:
            self.setDefaultImage()
            if filename:
                self.lblImage.configure(text=f'Could not find\n{filename}')
            else:
                self.lblImage.configure(text='Choisir une photo')

    def loadThumb(self, picture: Picture):
        """Display the thumbnail of the specified picture."""
        fileMedium = None
        if picture is not None:
            fileMedium = f'{config.dirPicsBase}medium/{picture.filename}'
        self.loadData(fileMedium)

    def setDefaultImage(self):
        """Display the default image."""
        if self.defImage and os.path.exists(self.defImage):
            img = ImageTk.PhotoImage(Image.open(self.defImage))
            self.lblImage.configure(image=img)
            self.lblImage.image = img
        else:
            self.lblImage.configure(image='')
            self.lblImage.image = None
        
    def createWidgets(self, parent: ttk.Frame):
        """Create user widgets."""
        self.lblImage = ttk.Label(master=parent, anchor=tk.CENTER, text='Choisir une photo')
        self.lblImage.pack(side=tk.TOP)
        self.setDefaultImage()


class MultiImageWidget(ImageWidget):
    """A widget displaying multiple images."""
    log = logging.getLogger('MultiImageWidget')

    def __init__(self, defImage=None):
        """Constructor"""
        super().__init__(defImage)
        self.files = []

    def onPrev(self):
        pass

    def onNext(self):
        pass

    def createWidgets(self, parent: ttk.Frame):
        """Create user widgets."""
        self.lblImage = ttk.Label(master=parent, anchor=tk.CENTER, text='Choisir une photo')
        self.lblImage.pack(side=tk.TOP)
        self.btnPrev = Button(parent, None, self.onPrev, 'go-prev')
        self.btnPrev.btn.configure(width=0)
        self.btnPrev.pack()
        self.lblStatus = ttk.Label(master=parent, anchor=tk.CENTER, text='Status')
        self.lblStatus.pack(side=tk.LEFT)
        self.btnNext = Button(parent, None, self.onNext, 'go-next')
        self.btnNext.btn.configure(width=0)
        self.btnNext.pack(3, tk.RIGHT)
        self.setDefaultImage()