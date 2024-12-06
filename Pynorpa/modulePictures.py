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
        self.imageWidget.loadThumb(picture)

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


class PictureTable(TableWithColumns):
    """Class PictureTable"""
    log = logging.getLogger("PictureTable")

    def __init__(self, cbkSelect):
        """Constructor."""
        super().__init__(cbkSelect, "photos")
        #self.addColumn(TableColumn('Nom',    Picture.getFilename,     200))
        self.addColumn(TableColumn('Taxon',   Picture.getTaxonName,    200))
        self.addColumn(TableColumn('Date',    Picture.getShotAt,       160))
        self.addColumn(TableColumn('Lieu',    Picture.getLocationName, 200))
        self.addColumn(TableColumn('Qualité', Picture.getRating,        55))

    def loadData(self, pictures):
        """Display the specified objects in this table."""
        self.clear()
        self.data = pictures
        self.addRows(pictures)

    def __str__(self):
        return 'PictureTable'


class PictureEditor(BaseWidgets.BaseEditor):
    """Class PictureEditor"""
    log = logging.getLogger("PictureEditor")

    def __init__(self, cbkSave):
        """Constructor."""
        super().__init__(cbkSave, '#62564f')
        self.picture = None

    def loadData(self, picture: Picture):
        """Display the specified object in this editor."""
        self.picture = picture
        self.setValue(picture)

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.picture)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Picture Editor')
        
        self.widFilename = self.addTextReadOnly('Nom', Picture.getFilename)
        self.widShotAt = self.addDateTimeReadOnly('Date', Picture.getShotAt)
        self.widLocation = self.addTextReadOnly('Lieu', Picture.getLocationName)
        self.widRemarks = self.addTextArea('Remarques', Picture.getRemarks)
        self.widTaxon = self.addTextReadOnly('Taxon', Picture.getTaxonName)
        self.widUpdatedAt = self.addDateTimeReadOnly('Modifié', Picture.getUpdatedAt)
        self.widRating = self.addSpinBox('Qualité', Picture.getRating, 1, 5)
        
        self.createButtons(True, True, False)
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.picture is not None
        modified = self.hasChanges(self.picture)
        super().enableWidgets(editing)
        self.enableButtons(modified, modified, False)
        self.widRemarks.resetModified()

    def __str__(self):
        str = "PictureEditor"
        return str


