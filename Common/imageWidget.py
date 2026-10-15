"""
A widget displaying one or several images.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import io
import logging
import tkinter as tk
import urllib.request
from tkinter import ttk
from PIL import ImageTk, Image


class WebPhoto:
    """A photo referenced by a web URL."""
    log = logging.getLogger('WebPhoto')

    def __init__(self, url: str, desc: str):
        self.url = url
        self.desc = desc
        self.img = None

    def loadData(self):
        with urllib.request.urlopen(self.url) as u:
            rawdata = u.read()
            image = Image.open(io.BytesIO(rawdata))
            self.img = ImageTk.PhotoImage(image)
            self.log.info(f'Done loading data from {self.url}')

    def getImage(self) -> ImageTk.PhotoImage:
        if not self.img:
            self.loadData()
        return self.img
    
    def getSize(self) -> str:
        if not self.img:
            return '-'
        return f'{self.img.width()}x{self.img.height()}px'
    
    def getDescription(self) -> str:
        return self.desc

    def __str__(self):
        return f'WebPhoto {self.url}'


class ImageWidget():
    """A widget displaying an image from a file."""
    log = logging.getLogger('ImageWidget')

    def __init__(self):
        """Constructor"""
        self.img = None

    def display(self, photo: WebPhoto):
        """Load the web photo data and display it."""
        self.log.info(f'Loading image {photo}')
        img = photo.getImage()
        if img:
            self.log.info('Displaying image data')
            self.lblImage.config(image=img)
        else:
            self.log.warning(f'No image data in {photo}')
        
    def createWidgets(self, parent: ttk.Frame):
        """Create user widgets."""
        self.lblImage = ttk.Label(master=parent, anchor=tk.CENTER, text='Choisir une photo')
        self.lblImage.pack(side=tk.TOP, pady=6)
