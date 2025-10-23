"""
Pynorpa module to help create photo albums or calendars 
with iFolor or smartphoto.ch
"""

import config
import logging
import os

import BaseWidgets
import TextTools
import tkinter as tk
import imageWidget
from tkinter import ttk
from TabsApp import TabModule, TabsApp
from BaseTable import TableColumn, AdvTable
from picture import Picture, PictureCache
from LocationCache import LocationCache
from taxon import TaxonCache
from bookManager import Book, BookKind, BookPicFilter, BookManager, PictureInBook


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
        self.manager.loadBooks()
        bookNames = [book.getName() for book in self.manager.getBooks()]
        self.cboBooks.setValues(bookNames)
        self.cboBooks.setValue(bookNames[0])
        self.book = self.manager.getBooks()[0]
        self.onSelectBook(self.book)
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
        self.picFilter = book.getFilter()
        self.filterEditor.loadData(self.picFilter)
        self.loadPictures()
        self.tableBookPics.loadData(book.getPictures())
        if book.getPicCount() > 0:
            self.onSelectBookPicture(book.getPictures()[0])

    def onComboBookSel(self, evt=None):
        """Book combo selection callback."""
        name = self.cboBooks.getValue()
        self.log.info(f'Book selection change: {name}')
        for book in self.manager.getBooks():
            if book.getName() == name:
                self.onSelectBook(book)

    def onAddBook(self):
        """Add a new book."""
        newBook = self.manager.addBook()
        bookNames = [book.getName() for book in self.manager.getBooks()]
        self.cboBooks.setValues(bookNames)
        self.cboBooks.setValue(newBook.getName())
        self.book = newBook
        self.onSelectBook(self.book)
        self.enableWidgets()

    def onPreviewBook(self):
        """Preview a book."""
        self.manager.toHtml(self.book)

    def onSaveBook(self, book: Book):
        """Save the selected book."""
        book.setFilter(self.picFilter)
        self.manager.saveBook(book)

    def onSaveBookPic(self, pic: PictureInBook):
        """Save the selected book after picture edition."""
        self.manager.saveBook(self.book)

    def onFilterPics(self):
        """Reload pictures table using the filter."""
        self.log.info(f'Loading pictures with {self.picFilter}')
        self.log.info(f'Filter SQL: {self.picFilter.getFilterClause().getSQL()}')
        self.loadPictures()

    def onSelectPicture(self, picture: Picture):
        """Picture table selection callback."""
        self.picture = picture
        self.imageWidget.loadThumb(picture)
        self.enableWidgets()

    def onSelectBookPicture(self, bookPic: PictureInBook):
        """Book picture table selection callback."""
        self.bookPic = bookPic
        self.log.info(f'Selected {bookPic}')
        self.imageWidget.loadThumb(bookPic)
        self.bookPicEditor.loadData(bookPic)
        self.enableWidgets()

    def onAddPicture(self):
        """Add the selected picture to the selected book."""
        if self.picture and self.book:
            self.setLoadingIcon()
            self.bookPic = self.manager.addPictureInBook(self.picture, self.book)
            self.setLoadingIcon(True)
            self.onSelectBook(self.book)
            self.window.update()
            self.onSelectBookPicture(self.bookPic)

    def onRefresh(self):
        """Refresh the selected book."""
        self.onSelectBook(self.book)

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftCenterRightFrames()

        # Filter on location, taxon, quality
        self.filterEditor = FilterEditor(self.onFilterPics)
        self.filterEditor.createWidgets(self.frmLeft)

        # Table of filtered photos
        self.tablePics = PictureSelectionTable(self.onSelectPicture)
        self.tablePics.createWidgets(self.frmLeft, 32)

        # Book selector
        frmBooks = ttk.LabelFrame(self.frmCenter, text='Choix de livre')
        frmBooks.pack(fill=tk.X)
        self.cboBooks = BaseWidgets.ComboBox(self.onComboBookSel)
        self.cboBooks.createWidgets(frmBooks, 0, 0)

        # Book editor
        self.bookEditor = BookEditor(self.onSaveBook)
        self.bookEditor.createWidgets(self.frmCenter)

        # Table of pics in selected Book
        self.tableBookPics = BookPictureTable(self.onSelectBookPicture)
        self.tableBookPics.createWidgets(self.frmCenter, 20)

        # Book picture editor
        self.bookPicEditor = BookPictureEditor(self.onSaveBookPic)
        self.bookPicEditor.createWidgets(self.frmRight)

        # Image preview
        self.imageWidget = imageWidget.CaptionImageWidget(f'{config.dirPicsBase}medium/blank.jpg')
        self.imageWidget.createWidgets(self.frmRight, 4)

        # Buttons
        self.btnAddPic = BaseWidgets.Button(self.frmLeft, 'Ajouter', self.onAddPicture, 'add')
        self.btnAddPic.pack(0)
        # TODO add external image to book
        frmButtons = ttk.Frame(self.frmCenter)
        frmButtons.pack(fill=tk.X)
        self.btnAddBook = BaseWidgets.Button(frmButtons, 'Nouveau livre', self.onAddBook, 'new')
        self.btnAddBook.pack(0)
        self.btnPreview = BaseWidgets.Button(frmButtons, 'Aperçu', self.onPreviewBook, 'zoom')
        self.btnPreview.pack(0)
        self.btnRefresh = BaseWidgets.IconButton(frmButtons, 'refresh', 'Recharger le livre', self.onRefresh, 6)

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
        self.locCache = LocationCache()
        self.taxCache = TaxonCache()

    def loadData(self, filter: BookPicFilter):
        """Display the specified filter in this editor."""
        self.filter = filter
        self.setValue(filter)

    def onSave(self, evt=None):
        """Save changes to the edited object."""
        location = self.locCache.getByName(self.widLoc.getValue())
        self.filter.setLocation(location)
        taxonName = self.widTaxon.getValue()
        taxon = self.taxCache.findByName(TextTools.upperCaseFirst(taxonName))
        self.filter.setTaxon(taxon)
        self.filter.setQuality(self.widQuality.getValue())
        self.cbkSave()
        self.enableWidgets()

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Filtrer les photos')
        locNames = [loc.name for loc in self.locCache.getLocations()]
        locNames.insert(0, '(Tous)')
        self.widLoc     = self.addComboBoxRefl('Lieu', BookPicFilter.getLocationName, locNames)
        self.widTaxon   = self.addText('Taxon', BookPicFilter.getTaxonName, 42)
        self.widQuality = self.addSpinBox('Qualité min', BookPicFilter.getQuality, 1, 5)
        self.createButtons(True, False, False)
        self.btnSave.setLabel('Recharger')
        self.btnSave.setIcon('refresh')
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.filter is not None
        modified = self.hasChanges(self.filter)
        super().enableWidgets(editing)
        self.enableButtons(modified, False, False)


class PictureSelectionTable(AdvTable):
    """
    Table to select pictures to add to books.
    Filters on location, taxon, quality etc.
    """
    log = logging.getLogger("PictureSelectionTable")

    def __init__(self, cbkSelectRow):
        super().__init__(cbkSelectRow, 'Photos en galerie', 12)

    def addColumns(self):
        """Define the table columns."""
        self.addColumn(TableColumn('Taxon',   Picture.getTaxonName,    200))
        self.addColumn(TableColumn('Date',    Picture.getShotAtFmtDMY,  90))
        self.addColumn(TableColumn('Lieu',    Picture.getLocationName, 100))
        self.addColumn(TableColumn('Qual',    Picture.getRating,        38))


class BookPictureTable(AdvTable):
    """Table of pictures in book."""
    log = logging.getLogger('BookPictureTable')

    def __init__(self, cbkSelectRow):
        super().__init__(cbkSelectRow, 'Photos du livre', 12)

    def addColumns(self):
        """Define the table columns."""
        self.addColumn(TableColumn('Ordre',  PictureInBook.getOrder,     60))
        self.addColumn(TableColumn('Photo',  PictureInBook.getFilename, 370))
        

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
        self.book.setName(self.widName.getValue())
        self.book.setDesc(self.widDesc.getValue())
        self.book.setStatus(self.widStatus.getValue())
        self.book.setKind(BookKind[self.widKind.getValue()])
        self.cbkSave(self.book)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Propriétés du livre')
        
        self.widName   = self.addText('Nom', Book.getName, 42)
        self.widDesc   = self.addText('Description', Book.getDesc, 42)
        self.widKind   = self.addComboBoxRefl('Type', Book.getKindName, [kind.name for kind in BookKind])
        self.widStatus = self.addText('Status', Book.getStatus, 42)
        self.widPicCnt = self.addTextReadOnly('Photos', Book.getPicCount)
        
        self.createButtons(True, True, False)
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.book is not None
        modified = self.hasChanges(self.book)
        super().enableWidgets(editing)
        self.enableButtons(modified, modified, False)

    def __str__(self):
        return f'BookEditor editing {self.book}'
        

class BookPictureEditor(BaseWidgets.BaseEditor):
    """Class BookPictureEditor"""
    log = logging.getLogger("BookPictureEditor")

    def __init__(self, cbkSave):
        """Constructor."""
        super().__init__(cbkSave, '#62564f')
        self.bookPic = None

    def loadData(self, bookPic: PictureInBook):
        """Display the specified pic in this editor."""
        self.bookPic = bookPic
        self.setValue(bookPic)
        self.enableWidgets()

    def onSave(self, evt=None):
        """Save changes to the edited object."""
        self.bookPic.setCaption(self.widCaption.getValue())
        self.bookPic.setOrder(self.widOrder.getValue())
        self.cbkSave(self.bookPic)
        self.enableWidgets()

    def onOpenGimp(self):
        """Open with Gimp button command."""
        if self.bookPic and self.bookPic.hasOriginal():
            cmd = f'gimp {self.bookPic.getOrigFilename()} &'
            os.system(cmd)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Photo du livre')
        self.widOrder    = self.addIntInput('Ordre',   PictureInBook.getOrder)
        self.widCaption  = self.addTextArea('Légende', PictureInBook.getCaption, 6, 46)
        self.widOrigSize = self.addTextReadOnly('Original', PictureInBook.getOrigSize)
        self.createButtons(True, True, False)
        self.btnGimp     = self.addButton('Retoucher', self.onOpenGimp, 'gimp')
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.bookPic is not None
        modified = self.hasChanges(self.bookPic)
        super().enableWidgets(editing)
        self.enableButtons(modified, modified, False)
        self.btnGimp.enableWidget(editing and self.bookPic.hasOriginal())
        self.widCaption.resetModified()

    def __str__(self):
        return f'BookPictureEditor editing {self.bookPic}'