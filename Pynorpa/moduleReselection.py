"""
 Pynorpa Module for displaying selected photos and re-assigning them to another Taxon.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import config
import glob
import DateTools
import LocationCache
from TabsApp import *
from BaseTable import TableColumn
from BaseWidgets import BaseEditor
from moduleSelection import TablePhotos, PhotoEditor, TaxonSelector
from PhotoInfo import *
import imageWidget

class ModuleReselection(TabModule):
    """Pynorpa Module for reselecting photos."""
    log = logging.getLogger('ModuleReselection')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.app = parent
        self.window = parent.window
        super().__init__(parent, 'Resélection')
        self.locationCache = LocationCache.LocationCache()
        self.table = TableReselection(self.onSelectPhoto)
        self.imageWidget = imageWidget.ImageWidget(f'{config.dirPicsBase}medium/blank.jpg')
        self.editor = PhotoEditorReselection()
        self.selector = TaxonReselector(self.loadData)
        self.photos = []
        self.dir = None
        self.getDefaultDir()

    def getDefaultDir(self):
        """Find the default photo dir."""
        yearMonth = DateTools.nowAsString('%Y-%m')
        self.dir = f'{config.dirPhotosBase}Nature-{yearMonth}/photos'
        if not os.path.exists(self.dir):
            self.log.info('Revert to previous month for default dir')
            yearMonth = DateTools.timestampToString(DateTools.addDays(DateTools.now(), -28), '%Y-%m')
            self.dir = f'{config.dirPhotosBase}Nature-{yearMonth}/photos'
        self.selector.setDir(f'{config.dirPhotosBase}Nature-{yearMonth}')
        self.log.info('Default dir: %s', self.dir)

    def loadData(self):
        """Load the photos to display."""
        self.photos = []
        files = sorted(glob.glob(f'{self.dir}/*.jpg'))
        for file in files:
            photo = PhotoInfo(file)
            photo.identify()
            photo.setCloseTo(self.locationCache.getClosest(photo.lat, photo.lon))
            self.photos.append(photo)
        self.table.loadData(self.photos)
        self.app.setStatus(f'Chargé {self.dir}')

    def onSelectPhoto(self, photo: PhotoInfo):
        """Photo selection callback."""
        self.log.info(f'Selected {photo}')
        thumbfile = None  # Thumb size: 500x500px
        if photo is not None:
            thumbfile = photo.filename.replace('photos/', 'thumbs/')
            if not os.path.exists(thumbfile):
                sCmd = f'convert {photo.filename} -resize 500x500 {thumbfile}'
                os.system(sCmd)
        self.imageWidget.loadData(thumbfile)
        self.editor.loadData(photo)
        self.selector.loadData(photo)

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Widgets
        self.table.createWidgets(self.frmLeft)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.createWidgets(self.frmRight)
        self.selector.createWidgets(self.frmRight)

class TableReselection(TablePhotos):
    """Table widget for Pynorpa photo."""
    log = logging.getLogger("TablePhotos")

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        super().__init__(cbkSelect)

    def setColumns(self):
        self.addColumn(TableColumn('Nom',     PhotoInfo.getNameNoExt,    240))
        self.addColumn(TableColumn('Date',    PhotoInfo.getShotAtString, 150))
        self.addColumn(TableColumn('Près de', PhotoInfo.getCloseTo,      300))

class PhotoEditorReselection(PhotoEditor):
    """A widget for displaying PhotoInfo properties."""
    log = logging.getLogger('PhotoEditorReselection')

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        BaseEditor.createWidgets(self, parent, 'Propriétés de la photo')

        # Photo attributes
        self.lblName     = self.addTextReadOnly('Nom',        PhotoInfo.getNameShortened)
        self.lblDate     = self.addTextReadOnly('Date',       PhotoInfo.getShotAtString)
        self.lblPicSize  = self.addTextReadOnly('Taille',     PhotoInfo.getSizeString)
        self.lblPosition = self.addTextReadOnly('Position',   PhotoInfo.getGPSString)
        self.lblExposure = self.addTextReadOnly('Exposition', PhotoInfo.getExposureDetails)

class TaxonReselector(TaxonSelector):
    log = logging.getLogger("TaxonReselector")

    def __init__(self, cbkReselection):
        super().__init__()
        self.cbkReselection = cbkReselection

    def onSelect(self):
        """Selection button command."""
        self.log.info(f'Renaming {self.photo.filename} to {self.newName}')
        target = f'{self.dir}/photos/{self.newName}'
        cmd = f'mv {self.photo.filename} {target}'
        self.runSystemCommand(cmd)
        self.runSystemCommand(cmd.replace('photos/', 'thumbs/'))
        self.enableWidgets()
        self.cbkReselection()

    def runSystemCommand(self, cmd: str):
        self.log.info(cmd)
        os.system(cmd)