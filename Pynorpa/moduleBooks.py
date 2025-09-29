"""
Pynorpa module to help create photo albums or calendars 
with iFolor or smartphoto.ch
"""

# TODO add Books module 
# - Book has name, description, status, list of pictures
# - status: Project, Ongoing, Ordered, Done
# - select Pictures by filtering on Location or Taxon
# - find original file on disk or backups by matching timestamp
# - add original image file to Book directory orig/ for edition
# - save Book contents in json file
# - generate Book preview html file with medium images and comments 

import config
import logging

import BaseWidgets
import tkinter as tk
from tkinter import ttk
from TabsApp import TabModule, TabsApp
from bookManager import Book, BookPicFilter


class ModuleBooks(TabModule):
    """Class to help design books."""
    log = logging.getLogger('ModuleBooks')

    def __init__(self, parent: TabsApp):
        """Constructor."""
        self.window = parent.window
        super().__init__(parent, 'Livres')
        self.book = None

    def loadData(self):
        self.book = Book('Test01', 'Livre test 1')
        self.onSelectBook(self.book)

    def onSelectBook(self, book: Book):
        """Display selected book in editor."""
        self.log.info(f'Selected {book}')
        self.book = book
        self.bookEditor.loadData(book)

    def onSaveBook(book: Book):
        pass

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Filter on location, taxon, quality
        frmFilter = ttk.LabelFrame(self.frmLeft, text='Filtres')
        frmFilter.pack(fill=tk.X)
        self.lblFilter = ttk.Label(frmFilter, text='Filtrer par lieu, taxon et qualité')
        self.lblFilter.pack(fill=tk.X)

        # Table of filtered photos


        # Book selector


        # Book editor
        self.bookEditor = BookEditor(self.onSaveBook)
        self.bookEditor.createWidgets(self.frmRight)

        # Table of pics in selected Book


        # Buttons


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

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Propriétés du livre')
        
        self.widName   = self.addText('Nom', Book.getName)
        self.widDesc   = self.addText('Description', Book.getDesc)
        self.widStatus = self.addText('Status', Book.getStatus)
        
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