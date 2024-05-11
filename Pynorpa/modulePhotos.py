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
from TabsApp import *
from PhotoInfo import *
from BaseTable import *


class ModulePhotos(TabModule):
    """Pynorpa Module for photos."""
    log = logging.getLogger('ModulePhotos')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.table = TablePhotos(self.onSelectPhoto)
        #self.mapWidget = MapWidget()
        self.editor = PhotoEditor()
        super().__init__(parent, 'Photos')
        self.photos = []
        self.loadData()

    def loadData(self):
        """Load the photos to display."""
        dirPhotosOrig = f'{config.dirPhotosBase}Nature-2024-04/orig/'
        files = sorted(glob.glob(f'{dirPhotosOrig}*.JPG'))
        for file in files:
            photo = PhotoInfo(file)
            photo.identify()
            self.photos.append(photo)
        self.table.loadData(self.photos)

    def onSelectPhoto(self, photo: PhotoInfo):
        self.log.info(f'Selected {photo}')
        # Display in map widget
        #self.mapWidget.loadData(photo)
        # Display in editor
        self.editor.loadData(photo)

    def createWidgets(self):
        """Create user widgets."""

        # Frames
        self.frmLeft = tk.Frame(master=self.oFrame)
        self.frmLeft.pack(fill=tk.Y, side=tk.LEFT, pady=0)
        self.frmRight = tk.Frame(master=self.oFrame, width=600)
        self.frmRight.pack(fill=tk.Y, side=tk.LEFT, pady=6, padx=6)

        # Photos table
        self.table.createWidgets(self.frmLeft)

        # Map widget
        #self.mapWidget.createWidgets(self.frmRight)

        # Photo properties
        self.editor.createWidgets(self.frmRight)

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

class PhotoEditor():
    """A widget for displaying PhotoInfo properties."""
    log = logging.getLogger('PhotoEditor')

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        self.photo = None
        self.row = 0

    def loadData(self, photo: PhotoInfo):
        """Display the specified object in this editor."""
        self.photo = photo
        self.lblName.setValue(None)
        self.lblDate.setValue(None)
        self.lblPosition.setValue(None)
        self.lblExposure.setValue(None)
        if photo:
            self.lblName.setValue(photo.getNameFull())
            self.lblDate.setValue(photo.getShotAtString())
            self.lblPosition.setValue(photo.getGPSString())
            self.lblExposure.setValue(photo.getExposureDetails())

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        self.frmEdit = ttk.LabelFrame(parent, text='Propriétés de la photo', width=600)
        self.frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True, pady=5)

        # Photo attributes
        self.lblName = self.addTextReadOnly('Nom')
        self.lblDate = self.addTextReadOnly('Date')
        self.lblPosition = self.addTextReadOnly('Position')
        self.lblExposure = self.addTextReadOnly('Exposition')
    
    def addTextReadOnly(self, label: str) -> BaseWidgets.TextReadOnly:
        """Add a read-only text."""
        self.addLabel(label)
        oInput = BaseWidgets.TextReadOnly(label)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.row += 1
        return oInput

    def addLabel(self, label: str):
        """Add an attribute label at the specified row."""
        oLabel = tk.Label(self.frmEdit, text=label)
        oLabel.grid(row=self.row, column=0, sticky='nw')

    def __str__(self) -> str:
        return 'PhotoEditor'