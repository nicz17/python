"""Module modulePictures"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
from BaseTable import *
from TabsApp import *
import BaseWidgets
import imageWidget
from picture import Picture, PictureCache


class ModulePictures(TabModule):
    """Class ModulePictures"""
    log = logging.getLogger("ModulePictures")

    def __init__(self, parent: TabsApp):
        """Constructor."""
        self.window = parent.window
        self.table  = PictureTable(self.onSelectPicture)
        self.editor = PictureEditor(self.onSavePicture)
        self.imageWidget = imageWidget.ImageWidget(f'{config.dirPicsBase}medium/blank.jpg')
        super().__init__(parent, 'Photos')

    def loadData(self):
        """Load data from cache and populate table."""
        self.pictureCache = PictureCache()
        self.table.loadData(self.pictureCache.getPictures())

    def onSelectPicture(self, picture: Picture):
        """Display selected object in editor."""
        self.log.info(f'Selected {picture}')
        self.editor.loadData(picture)

        fileMedium = None
        if picture is not None:
            fileMedium = f'{config.dirPicsBase}medium/{picture.filename}'
        self.imageWidget.loadData(fileMedium)

    def onSavePicture(self, picture: Picture):
        """Save changes to edited object."""
        pass

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()
        self.table.createWidgets(self.frmLeft)
        self.editor.createWidgets(self.frmRight)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.loadData(None)

    def __str__(self):
        str = "ModulePictures"
        return str


class PictureTable(BaseTable):
    """Class PictureTable"""
    log = logging.getLogger("PictureTable")

    def __init__(self, cbkSelect):
        """Constructor."""
        super().__init__(cbkSelect, "photos")
        self.columns = ('Nom', 'Date', 'Lieu', 'Taxon')

    def loadData(self, pictures):
        """Display the specified objects in this table."""
        self.clear()
        self.data = pictures
        picture: Picture
        for picture in pictures:
            rowData = (picture.getFilename(), picture.getShotAt(), picture.getLocationName(), picture.getTaxonName())
            self.addRow(rowData)

    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        super().createWidgets(parent, self.columns)

    def __str__(self):
        str = "PictureTable"
        return str


class PictureEditor(BaseWidgets.BaseEditor):
    """Class PictureEditor"""
    log = logging.getLogger("PictureEditor")

    def __init__(self, cbkSave):
        """Constructor."""
        super().__init__(cbkSave)
        self.picture = None

    def loadData(self, picture: Picture):
        """Display the specified object in this editor."""
        self.picture = picture
        self.setValue(picture)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Picture Editor')
        
        self.widFilename = self.addTextReadOnly('Nom', Picture.getFilename)
        self.widShotAt = self.addDateTimeReadOnly('Date', Picture.getShotAt)
        self.widLocation = self.addTextReadOnly('Lieu', Picture.getLocationName)
        self.widRemarks = self.addTextArea('Remarques', Picture.getRemarks)
        self.widTaxon = self.addTextReadOnly('Taxon', Picture.getTaxonName)
        self.widUpdatedAt = self.addDateTimeReadOnly('Modifié', Picture.getUpdatedAt)
        self.widRating = self.addIntInput('Qualité', Picture.getRating)
        
        self.createButtons(True, True, False)
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.picture is not None
        modified = self.hasChanges(self.picture)
        super().enableWidgets(editing)
        BaseWidgets.enableWidget(self.btnSave, modified)
        BaseWidgets.enableWidget(self.btnCancel, modified)
        BaseWidgets.enableWidget(self.btnDelete, False)
        self.widRemarks.resetModified()

    def __str__(self):
        str = "PictureEditor"
        return str


