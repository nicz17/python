"""
 Pynorpa Module for displaying photo previews.
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


class ModulePhotos(TabModule):
    """Pynorpa Module for photos."""
    log = logging.getLogger('ModulePhotos')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.table = TablePhotos(self.onSelectPhoto)
        #self.mapWidget = MapWidget()
        self.imageWidget = imageWidget.ImageWidget()
        self.editor = PhotoEditor()
        super().__init__(parent, 'Photos')
        self.photos = []
        self.getDefaultDir()
        #self.loadData()

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

        # Frames
        self.frmLeft = tk.Frame(master=self.oFrame)
        self.frmLeft.pack(fill=tk.Y, side=tk.LEFT, pady=0)
        self.frmRight = tk.Frame(master=self.oFrame, width=600)
        self.frmRight.pack(fill=tk.Y, side=tk.LEFT, pady=6, padx=6)

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
        super().__init__(self.onRowSelection, 'photos')
        self.columns = ('Nom', 'Date', 'Taille')
        self.data = []
        self.cbkSelect = cbkSelect

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

    def onRowSelection(self, event):
        """Row selection callback."""
        idxRow = self.getSelectedRow()
        self.cbkSelect(self.data[idxRow] if idxRow is not None else None)

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
        self.lblName     = self.addTextReadOnlyRefl('Nom',        PhotoInfo.getNameFull)
        self.lblDate     = self.addTextReadOnlyRefl('Date',       PhotoInfo.getShotAtString)
        self.lblPicSize  = self.addTextReadOnlyRefl('Taille',     PhotoInfo.getSizeString)
        self.lblPosition = self.addTextReadOnlyRefl('Position',   PhotoInfo.getGPSString)
        self.lblExposure = self.addTextReadOnlyRefl('Exposition', PhotoInfo.getExposureDetails)

    def __str__(self) -> str:
        return 'PhotoEditor'