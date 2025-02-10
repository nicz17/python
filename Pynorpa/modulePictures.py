"""Module modulePictures"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
from tkinter import filedialog as fd

from BaseTable import *
from TabsApp import *
import BaseWidgets
import DateTools
import imageWidget
from LocationCache import LocationCache
from picture import Picture, PictureCache
from PhotoInfo import PhotoInfo
from taxon import TaxonCache
from uploader import Uploader


class ModulePictures(TabModule):
    """Class ModulePictures"""
    log = logging.getLogger("ModulePictures")

    def __init__(self, parent: TabsApp):
        """Constructor."""
        self.window = parent.window
        self.table   = PictureTable(self.onSelectPicture)
        self.editor  = PictureEditor(self.onSavePicture)
        self.factory = PictureFactory(self.onAddPicture)
        self.imageWidget = imageWidget.ImageWidget(f'{config.dirPicsBase}medium/blank.jpg')
        super().__init__(parent, 'Photos')

    def loadData(self):
        """Load data from cache and populate table."""
        self.pictureCache = PictureCache()
        self.table.loadData(self.pictureCache.getPictures())
        self.factory.loadData()

    def onSelectPicture(self, picture: Picture):
        """Display selected object in editor."""
        self.log.info(f'Selected {picture}')
        self.editor.loadData(picture)
        self.imageWidget.loadThumb(picture)

    def onSavePicture(self, picture: Picture):
        """Save changes to edited object."""
        self.log.info('Saving %s', picture)
        self.pictureCache.save(picture)
        self.editor.loadData(picture)

    def onAddPicture(self, picture: Picture):
        """Add a picture to gallery."""
        pass

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()
        self.table.createWidgets(self.frmLeft)
        self.factory.createWidgets(self.frmLeft)
        self.editor.createWidgets(self.frmRight)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.loadData(None)

    def __str__(self):
        return 'ModulePictures'


class PictureFactory():
    """Widget to add a picture to gallery."""
    log = logging.getLogger('PictureFactory')

    def __init__(self, cbkAdd):
        """Constructor with add callback."""
        self.locationCache = LocationCache()
        self.taxonCache = TaxonCache()
        self.cbkAdd = cbkAdd
        self.dir = None

    def onAdd(self, evt=None):
        loc = self.locationCache.getByName(self.cboLocation.getValue())
        filename = fd.askopenfilename(
            title = 'Ajouter une photo en galerie',
            initialdir = self.dir,
            filetypes = [('JPEG files', '*.jpg')])
        if filename:
            self.log.info('Adding picture %s at %s', filename, loc)
            # TODO check picture is not added yet
            info = PhotoInfo(filename)
            info.identify()
            tShotAt = DateTools.timestampToDatetimeUTC(info.getShotAt())
            taxon = self.taxonCache.findByFilename(filename)
            if taxon:
                pic = Picture(-1, filename, tShotAt, None, taxon.getIdx(), DateTools.nowDatetime(), loc.getIdx(), 3)
                pic.taxon = taxon
                pic.location = loc
                self.cbkAdd(pic)
            else:
                self.log.error('Failed to find taxon for %s', filename)
                # TODO GUI error dialog

    def loadData(self):
        self.cboLocation.setValue(self.locationCache.getDefaultLocation().getName())
        self.getDefaultDir()

    def getDefaultDir(self):
        """Find the default photo dir."""
        yearMonth = DateTools.nowAsString('%Y-%m')
        self.dir = f'{config.dirPhotosBase}Nature-{yearMonth}/photos'
        if not os.path.exists(self.dir):
            self.log.info('Revert to previous month for default dir')
            yearMonth = DateTools.timestampToString(DateTools.addDays(DateTools.now(), -28), '%Y-%m')
            self.dir = f'{config.dirPhotosBase}Nature-{yearMonth}/photos'
        self.log.info('Default dir: %s', self.dir)

    def createWidgets(self, parent: tk.Frame):
        self.frmMain = ttk.LabelFrame(parent, text='Ajouter une photo à')
        self.frmMain.pack(side=tk.LEFT, padx=5, pady=0)
        self.cboLocation = BaseWidgets.ComboBox(None)
        self.cboLocation.createWidgets(self.frmMain, 0, 0)
        self.cboLocation.setValues([loc.name for loc in self.locationCache.getLocations()])
        self.btnAdd = BaseWidgets.Button(self.frmMain, 'Ajouter', self.onAdd, 'add')
        self.btnAdd.grid(0, 1)


class PictureTable(TableWithColumns):
    """Class PictureTable"""
    log = logging.getLogger("PictureTable")

    def __init__(self, cbkSelect):
        """Constructor."""
        super().__init__(cbkSelect, "photos")
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
        self.uploader = Uploader()

    def loadData(self, picture: Picture):
        """Display the specified object in this editor."""
        self.picture = picture
        self.setValue(picture)

    def onSave(self, evt=None):
        """Save changes to the edited object."""
        self.picture.setRemarks(self.widRemarks.getValue())
        self.picture.setRating(self.widRating.getValue())
        self.cbkSave(self.picture)

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.picture)

    def onUpload(self):
        """Upload the edited picture."""
        if self.picture:
            self.uploader.uploadSinglePhoto(self.picture)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Propriétés de la photo')
        
        self.widFilename = self.addTextReadOnly('Nom', Picture.getFilename)
        self.widShotAt = self.addDateTimeReadOnly('Date', Picture.getShotAt)
        self.widLocation = self.addTextReadOnly('Lieu', Picture.getCloseTo)
        self.widRemarks = self.addTextArea('Remarques', Picture.getRemarks)
        self.widTaxon = self.addTextReadOnly('Taxon', Picture.getTaxonNames)
        self.widUpdatedAt = self.addDateTimeReadOnly('Modifié', Picture.getUpdatedAt)
        self.widRating = self.addSpinBox('Qualité', Picture.getRating, 1, 5)
        
        self.createButtons(True, True, False)
        self.btnUpload = self.addButton('Publier', self.onUpload, 'go-up')
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.picture is not None
        modified = self.hasChanges(self.picture)
        super().enableWidgets(editing)
        self.enableButtons(modified, modified, False)
        self.btnUpload.enableWidget(editing)
        self.widRemarks.resetModified()

    def __str__(self):
        return 'PictureEditor'


