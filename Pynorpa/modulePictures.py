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
from taxon import Taxon, TaxonCache
from pynorpaManager import PynorpaManager, PynorpaException
from uploader import Uploader
from ModalDialog import *
from moduleTaxon import TaxonTree


class ModulePictures(TabModule):
    """Class ModulePictures"""
    log = logging.getLogger("ModulePictures")

    def __init__(self, parent: TabsApp):
        """Constructor."""
        self.window = parent.window
        self.table   = PictureTable(self.onSelectPicture)
        self.editor  = PictureEditor(self.onSavePicture)
        self.factory = PictureFactory(self.onAddPicture, parent)
        self.imageWidget = imageWidget.ImageWidget(f'{config.dirPicsBase}medium/blank.jpg')
        super().__init__(parent, 'Photos')
        self.picture = None

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
        self.picture = picture
        self.enableWidgets()

    def onSavePicture(self, picture: Picture):
        """Save changes to edited object."""
        self.log.info('Saving %s', picture)
        self.pictureCache.save(picture)
        self.editor.loadData(picture)

    def onAddPicture(self, picture: Picture):
        """Add a picture to gallery."""
        if picture:
            self.table.addObject(picture)
            self.onSelectPicture(picture)

    def onReclassify(self):
        """Reclassify the selected picture."""
        dlg = DialogReclassify(self.window, self.picture)
        self.window.wait_window(dlg.root)

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()
        self.table.createWidgets(self.frmLeft)
        self.factory.createWidgets(self.frmLeft)
        self.editor.createWidgets(self.frmRight)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.loadData(None)

        # Reclassify button
        self.btnReclass = BaseWidgets.Button(self.frmLeft, 'Reclasser', self.onReclassify, 'edit')
        self.btnReclass.pack(0)
        self.enableWidgets()

    def enableWidgets(self):
        """Enable or disable the buttons."""
        hasSelection = (self.picture is not None)
        self.btnReclass.enableWidget(hasSelection)

    def __str__(self):
        return 'ModulePictures'


class PictureFactory():
    """Widget to add a picture to gallery."""
    log = logging.getLogger('PictureFactory')

    def __init__(self, cbkAdd, parent: TabsApp):
        """Constructor with add callback."""
        self.parent = parent
        self.manager = PynorpaManager()
        self.locationCache = LocationCache()
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
            try:
                pic = self.manager.addPicture(filename, loc)
                self.cbkAdd(pic)
            except PynorpaException as exc:
                self.parent.showErrorMsg(exc)

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


class DialogReclassify(ModalDialog):
    log = logging.getLogger('DialogReclassify')

    def __init__(self, parent: tk.Tk, picture: Picture):
        """Constructor."""
        self.picture = picture
        self.newName = None
        super().__init__(parent, f'Reclasser {picture.getFilename()}')
        self.root.geometry('1020x600+300+150')

    def onSave(self):
        """Rename the selected photo."""
        pass

    def onSelectTaxon(self, id: str):
        """Callback for selection of taxon with specified id."""
        taxon = None
        if id is not None:
            taxon = self.cache.findById(int(id))
        self.log.info('Selected %s', taxon)
        # TODO generate new name
        self.enableWidgets()

    def loadData(self):
        self.cache = TaxonCache()
        self.tree.loadData()
        self.tree.setSelection(self.picture.getTaxon())
        self.enableWidgets()

    def createWidgets(self):
        # Left and right frames
        self.frmLeft  = ttk.Frame(self.root)
        self.frmRight = ttk.Frame(self.root)
        self.frmLeft.pack( fill=tk.Y, side=tk.LEFT, pady=0)
        self.frmRight.pack(fill=tk.Y, side=tk.LEFT, pady=0, padx=0)

        # Taxon tree
        self.tree = TaxonTree(self.onSelectTaxon)
        self.tree.createWidgets(self.frmLeft)

        # New name frame
        frmNewname = ttk.LabelFrame(self.frmRight, text='Reclasser sous')
        frmNewname.pack(fill=tk.X)
        self.lblNewName = ttk.Label(frmNewname, text='Choisir un nouveau taxon')
        self.lblNewName.pack(fill=tk.X)

        # TODO table/list of existing pictures for taxon

        # Buttons
        self.frmButtons = ttk.Frame(self.frmRight)
        self.frmButtons.pack(fill=tk.X, pady=10)
        self.btnSave = BaseWidgets.Button(self.frmButtons, 'Reclasser', self.onSave, 'edit')
        self.btnExit = BaseWidgets.Button(self.frmButtons, 'Annuler',   self.exit, 'cancel')
        self.btnSave.pack()
        self.btnExit.pack()

    def enableWidgets(self):
        self.btnSave.enableWidget(self.newName is not None)


