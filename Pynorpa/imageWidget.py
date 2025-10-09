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
from PhotoInfo import PhotoInfo
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
            if isinstance(picture, Picture):
                self.log.info('Loading thumb for Picture %s', picture.filename)
                fileMedium = f'{config.dirPicsBase}medium/{picture.filename}'
            if isinstance(picture, PhotoInfo):
                self.log.info('Loading thumb for PhotoInfo %s', picture.filename)
                if picture.filename.startswith(config.dirPictures):
                    # It's the PhotoInfo of a database Picture
                    fileMedium = picture.filename.replace(config.dirPictures, f'{config.dirPicsBase}medium/')
                elif '/orig/' in picture.filename:
                    # It's the PhotoInfo of a original photo
                    fileMedium = picture.filename.replace('orig/', 'thumbs/')
                else:
                    # It's the PhotoInfo of a preselected photo
                    fileMedium = picture.filename.replace('photos/', 'thumbs/')
                if fileMedium and not os.path.exists(fileMedium):
                    self.log.info('Creating medium image for %s', picture.filename)
                    os.system(f'convert {picture.filename} -resize 500x500 {fileMedium}')
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


class CaptionImageWidget(ImageWidget):
    """Subclass of ImageWidget with an additional caption label."""
    log = logging.getLogger('CaptionImageWidget')

    def loadThumb(self, picture: Picture):
        super().loadThumb(picture)

        # Display caption
        mtdCaption = getattr(picture, 'getCaption', None)
        if callable(mtdCaption):
            caption = mtdCaption()
        else:
            caption = str(picture)
        if caption is None:
            caption = ''
        self.lblCaption.configure(text=caption)

    def setDefaultImage(self):
        super().setDefaultImage()
        self.lblCaption.configure(text='')
        
    def createWidgets(self, parent: ttk.Frame, pady=6):
        """Create user widgets."""
        self.lblImage = ttk.Label(master=parent, anchor=tk.CENTER, text='Choisir une photo')
        self.lblImage.pack(side=tk.TOP, fill=tk.X, pady=pady)
        self.lblCaption = ttk.Label(master=parent, anchor=tk.CENTER, text='Caption', wraplength=500)
        self.lblCaption.pack(side=tk.TOP, fill=tk.X)
        self.setDefaultImage()


class MultiImageWidget(ImageWidget):
    """A widget displaying multiple images."""
    log = logging.getLogger('MultiImageWidget')

    def __init__(self, defImage=None, cbkSelectImage=None):
        """Constructor"""
        super().__init__(defImage)
        self.cbkSelectImage = cbkSelectImage
        self.files = []
        self.iSelected = None

    def loadImages(self, files: list):
        """Display the specified images."""
        self.files = files
        if self.files is not None and len(self.files) > 0:
            self.iSelected = 0
        else:
            self.iSelected = None
        self.loadImage()
        self.enableWidgets()

    def loadImage(self):
        """Display the current image."""
        obj = None
        if self.iSelected is None:
            self.setDefaultImage()
            self.lblStatus.configure(text='')
        else:
            obj = self.files[self.iSelected]
            self.log.debug('Displaying image [%d/%d] %s', self.iSelected, self.size(), obj)
            if isinstance(obj, Picture):
                self.loadThumb(obj)
                status = f'[{self.iSelected+1}/{self.size()}] {obj.getTaxonName()}'
                self.lblStatus.configure(text=status)
            elif isinstance(obj, PhotoInfo):
                self.loadThumb(obj)
                status = f'[{self.iSelected+1}/{self.size()}] {obj.getNameShort()}'
                self.lblStatus.configure(text=status)
        if self.cbkSelectImage:
            self.cbkSelectImage(obj)

    def onPrev(self):
        if self.iSelected is not None:
            self.iSelected = ((self.iSelected - 1) % self.size())
        self.loadImage()

    def onNext(self):
        if self.iSelected is not None:
            self.iSelected = ((self.iSelected + 1) % self.size())
        self.loadImage()

    def size(self):
        return 0 if self.files is None else len(self.files)

    def createWidgets(self, parent: ttk.Frame, padx=0):
        """Create user widgets."""
        self.frmImage = ttk.Frame(parent, width=500, height=532)
        self.frmImage.pack(side=tk.TOP, fill=None, expand=False, padx=padx, pady=6)
        self.lblImage = ttk.Label(self.frmImage, anchor=tk.CENTER, text='')
        self.lblImage.place(x=250, y=250, anchor=tk.CENTER)
        self.btnPrev = Button(self.frmImage, None, self.onPrev, 'go-prev')
        self.btnPrev.btn.configure(width=0)
        self.btnPrev.btn.place(x=0, y=516, anchor=tk.SW)
        self.lblStatus = ttk.Label(self.frmImage, anchor=tk.CENTER, text='', width=46)
        self.lblStatus.place(x=250, y=500, anchor=tk.S)
        self.btnNext = Button(self.frmImage, None, self.onNext, 'go-next')
        self.btnNext.btn.configure(width=0)
        self.btnNext.btn.place(x=500, y=516, anchor=tk.SE)
        self.setDefaultImage()
        self.enableWidgets()

    def enableWidgets(self):
        enabled = self.files is not None and len(self.files) > 1
        self.btnPrev.enableWidget(enabled)
        self.btnNext.enableWidget(enabled)