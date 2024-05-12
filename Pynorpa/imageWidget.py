"""
Tkinter image widget module.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from PIL import ImageTk, Image


class ImageWidget():
    """A widget displaying an image from a file."""
    log = logging.getLogger('ImageWidget')

    def __init__(self):
        """Constructor"""
        self.log.info('Constructor')

    def loadData(self, filename: str):
        """Display the specified image if it exists."""
        if filename:
            img = ImageTk.PhotoImage(Image.open(filename))
            self.lblImage.configure(image=img)
            self.lblImage.image = img
        else:
            self.setDefaultImage()

    def setDefaultImage(self):
        """Display the default image."""
        pass
        
    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        self.lblImage = tk.Label(master=parent, text='Choisir une photo')
        self.lblImage.pack()
        self.setDefaultImage()
    