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
import DateTools
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
        yearMonth = DateTools.nowAsString('%Y-%m')
        dirPhotosOrig = f'{config.dirPhotosBase}Nature-{yearMonth}/orig/'
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
        self.lblName.setValue(None)
        self.lblDate.setValue(None)
        self.lblPicSize.setValue(None)
        self.lblPosition.setValue(None)
        self.lblExposure.setValue(None)
        if photo:
            self.lblName.setValue(photo.getNameFull())
            self.lblDate.setValue(photo.getShotAtString())
            self.lblPicSize.setValue(photo.getSizeString())
            self.lblPosition.setValue(photo.getGPSString())
            self.lblExposure.setValue(photo.getExposureDetails())

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Propriétés de la photo')

        # Photo attributes
        self.lblName     = self.addTextReadOnly('Nom')
        self.lblDate     = self.addTextReadOnly('Date')
        self.lblPicSize  = self.addTextReadOnly('Taille')
        self.lblPosition = self.addTextReadOnly('Position')
        self.lblExposure = self.addTextReadOnly('Exposition')

    def __str__(self) -> str:
        return 'PhotoEditor'