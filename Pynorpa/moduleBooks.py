"""
Pynorpa module to help create photo albums or calendars 
with iFolor or smartphoto.ch
"""

# TODO add Books module 
# - Book has name, description, status, list of pictures
# - status: Project, Ongoing, Ordered, Done
# - select Pictures by filtering on Location, Taxon and quality
# - find original file on disk or backups by matching timestamp
# - add original image file to Book directory orig/ for edition
# - save Book contents in json file
# - generate Book preview html file with medium images and comments 

import config
import logging

import BaseWidgets
import tkinter as tk
import imageWidget
from tkinter import ttk
from TabsApp import TabModule, TabsApp
from picture import Picture, PictureCache
from bookManager import Book, BookPicFilter, BookManager
from modulePictures import PictureTable


class ModuleBooks(TabModule):
    """Class to help design books."""
    log = logging.getLogger('ModuleBooks')

    def __init__(self, parent: TabsApp):
        """Constructor."""
        self.window = parent.window
        self.manager = BookManager()
        self.book = None
        self.picture = None
        super().__init__(parent, 'Livres')

    def loadData(self):
        self.picFilter = BookPicFilter()
        self.book = Book('Test01', 'Livre test 1')
        self.filterEditor.loadData(self.picFilter)
        self.onSelectBook(self.book)
        self.loadPictures()
        self.enableWidgets()

    def loadPictures(self):
        """Load pictures table."""
        self.pictureCache = PictureCache()
        where = self.picFilter.getFilterClause().getSQL()
        ids = self.pictureCache.fetchFromWhere(where)
        pics = [self.pictureCache.findById(id) for id in ids]
        self.tablePics.loadData(pics)

    def onSelectBook(self, book: Book):
        """Display selected book in editor."""
        self.log.info(f'Selected {book}')
        self.book = book
        self.bookEditor.loadData(book)

    def onSaveBook(self, book: Book):
        """Save the selected book."""
        self.manager.saveBook(book)

    def onFilterPics(self):
        """Reload pictures table using the filter."""
        self.log.info(f'Filter SQL: {self.picFilter.getFilterClause().getSQL()}')
        self.loadPictures()

    def onSelectPicture(self, picture: Picture):
        """Picture table selection callback."""
        self.picture = picture
        self.imageWidget.loadThumb(picture)
        self.enableWidgets()

    def onAddPicture(self):
        """Add the selected picture to the selected book."""
        if self.picture and self.book:
            self.log.info(f'Adding {self.picture} to {self.book}')
            self.book.addPicture(self.picture)
            self.manager.findOriginal(self.picture)

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Filter on location, taxon, quality
        self.filterEditor = FilterEditor(self.onFilterPics)
        self.filterEditor.createWidgets(self.frmLeft)

        # Table of filtered photos
        self.tablePics = PictureTable(self.onSelectPicture)
        self.tablePics.createWidgets(self.frmLeft, 32)

        # Book selector
        frmFilter = ttk.LabelFrame(self.frmRight, text='Livres')
        frmFilter.pack(fill=tk.X)
        self.lblFilter = ttk.Label(frmFilter, text='Choix de livre')
        self.lblFilter.pack(fill=tk.X)

        # Book editor
        self.bookEditor = BookEditor(self.onSaveBook)
        self.bookEditor.createWidgets(self.frmRight)

        # Table of pics in selected Book


        # Image preview
        self.imageWidget = imageWidget.ImageWidget(f'{config.dirPicsBase}medium/blank.jpg')
        self.imageWidget.createWidgets(self.frmRight)

        # Buttons
        self.btnAddPic = BaseWidgets.Button(self.frmLeft, 'Ajouter', self.onAddPicture, 'add')
        self.btnAddPic.pack(0)
        self.enableWidgets()

    def enableWidgets(self):
        """Enable or disable the buttons."""
        hasSelection = (self.picture is not None)
        self.btnAddPic.enableWidget(hasSelection)


class FilterEditor(BaseWidgets.BaseEditor):
    """Class FilterEditor"""
    log = logging.getLogger("FilterEditor")

    def __init__(self, cbkSave):
        """Constructor."""
        super().__init__(cbkSave, '#62564f')
        self.filter = None

    def loadData(self, filter: BookPicFilter):
        """Display the specified filter in this editor."""
        self.filter = filter
        self.setValue(filter)

    def onSave(self, evt=None):
        """Save changes to the edited object."""
        self.filter.setQuality(self.widQuality.getValue())
        self.cbkSave()

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Filtrer les photos')
        self.widLoc     = self.addText('Lieu', BookPicFilter.getLocationName)
        self.widTaxon   = self.addText('Taxon', BookPicFilter.getTaxon)
        self.widQuality = self.addSpinBox('Qualité min', BookPicFilter.getQuality, 1, 5)
        self.createButtons(True, False, False)
        self.btnSave.btn.configure(text='Recharger')

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.filter is not None
        modified = self.hasChanges(self.filter)
        super().enableWidgets(editing)
        self.enableButtons(modified, False, False)


class BookEditor(BaseWidgets.BaseEditor):
    """Class BookEditor"""
    log = logging.getLogger("BookEditor")

    def __init__(self, cbkSave):
        """Constructor."""
        super().__init__(cbkSave, '#62564f')
        self.book = None

    def loadData(self, book: Book):
        """Display the specified book in this editor."""
        self.book = book
        self.setValue(book)

    def onSave(self, evt=None):
        """Save changes to the edited object."""
        # TODO add setters and auto-update book
        self.cbkSave(self.book)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Propriétés du livre')
        
        self.widName   = self.addText('Nom', Book.getName)
        self.widDesc   = self.addText('Description', Book.getDesc)
        self.widStatus = self.addText('Status', Book.getStatus)
        self.widPicCnt = self.addIntInput('Photos', Book.getPicCount)
        
        self.createButtons(True, True, False)
        #self.btnUpload = self.addButton('Publier', self.onUpload, 'go-up')
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.book is not None
        modified = self.hasChanges(self.book)
        super().enableWidgets(editing)
        self.enableButtons(modified, modified, False)

    def __str__(self):
        return 'BookEditor'