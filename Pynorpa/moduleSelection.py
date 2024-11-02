"""
 Pynorpa Module for displaying photo previews and assigning them to a Taxon.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import config
import glob
import BaseWidgets
import imageWidget
import DateTools
from TabsApp import *
from PhotoInfo import *
from BaseTable import *
from tkinter import filedialog as fd

# TODO:
# rename to ModuleSelection
# add Taxon assignment section:
# add input text for Taxon lookup, trigger when at least 2 chars, fetch limit 1
# suggest selection name based on current taxon
# no need for Taxon tree, maybe ComboBox with child taxa ?
# if no matching taxon, take user input

class ModuleSelection(TabModule):
    """Pynorpa Module for photos."""
    log = logging.getLogger('ModuleSelection')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.table = TablePhotos(self.onSelectPhoto)
        #self.mapWidget = MapWidget()
        self.imageWidget = imageWidget.ImageWidget()
        self.editor = PhotoEditor()
        super().__init__(parent, 'Sélection')
        self.photos = []
        self.getDefaultDir()

    def getDefaultDir(self):
        """Find the default photo dir."""
        yearMonth = DateTools.nowAsString('%Y-%m')
        self.dir = f'{config.dirPhotosBase}Nature-{yearMonth}/orig'

    def loadData(self):
        """Load the photos to display."""
        self.photos = []
        files = sorted(glob.glob(f'{self.dir}/*.JPG'))
        for file in files:
            photo = PhotoInfo(file)
            photo.identify()
            self.photos.append(photo)
        self.table.loadData(self.photos)

    def onSelectPhoto(self, photo: PhotoInfo):
        """Photo selection callback."""
        self.log.info(f'Selected {photo}')
        thumbfile = None
        if photo is not None:
            thumbfile = photo.filename.replace('orig/', 'thumbs/')
        self.imageWidget.loadData(thumbfile)
        #self.mapWidget.loadData(photo)
        self.editor.loadData(photo)

    def selectDir(self):
        """Display a dialog to choose a photo dir."""
        self.dir = fd.askdirectory(mustexist=True, initialdir=config.dirPhotosBase)
        self.oParent.setStatus(f'Selected {self.dir}')
        self.loadData()

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Widgets
        self.table.createWidgets(self.frmLeft)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.createWidgets(self.frmRight)

        # Buttons frame
        self.frmButtons = ttk.Frame(self.frmLeft, padding=5)
        self.frmButtons.pack(anchor=tk.W)

        # Buttons
        self.btnReload = self.addButton('Reload',     self.loadData)
        self.btnOpen   = self.addButton('Change dir', self.selectDir)

    def addButton(self, label: str, cmd):
        """Add a Tk Button to this module's frmButtons."""
        btn = tk.Button(self.frmButtons, text = label, command = cmd)
        btn.pack(side=tk.LEFT)
        return btn

class TablePhotos(BaseTable):
    """Table widget for Pynorpa photo."""
    log = logging.getLogger("TablePhotos")

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        self.log.info('Constructor')
        super().__init__(cbkSelect, 'photos')
        self.columns = ('Nom', 'Date', 'Taille')

    def loadData(self, photos):
        """Display the specified photos in this table."""
        self.log.info('Loading %d photos', len(photos))
        self.clear()
        self.data = photos

        photo: PhotoInfo
        for photo in photos:
            rowData = (
                photo.getNameShort(), 
                photo.getShotAtString(),
                photo.getSizeString()
            )
            self.addRow(rowData)

    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        super().createWidgets(parent, self.columns)

    def __str__(self) -> str:
        return 'TablePhotos'

class PhotoEditor(BaseWidgets.BaseEditor):
    """A widget for displaying PhotoInfo properties."""
    log = logging.getLogger('PhotoEditor')

    def __init__(self):
        """Constructor."""
        super().__init__()
        self.photo = None

    def loadData(self, photo: PhotoInfo):
        """Display the specified object in this editor."""
        self.photo = photo
        self.setValue(photo)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Propriétés de la photo')

        # Photo attributes
        self.lblName     = self.addTextReadOnly('Nom',        PhotoInfo.getNameFull)
        self.lblDate     = self.addTextReadOnly('Date',       PhotoInfo.getShotAtString)
        self.lblPicSize  = self.addTextReadOnly('Taille',     PhotoInfo.getSizeString)
        self.lblPosition = self.addTextReadOnly('Position',   PhotoInfo.getGPSString)
        self.lblExposure = self.addTextReadOnly('Exposition', PhotoInfo.getExposureDetails)

    def __str__(self) -> str:
        return 'PhotoEditor'