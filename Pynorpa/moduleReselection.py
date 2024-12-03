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
from moduleSelection import TablePhotos, PhotoEditor
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
        self.editor = PhotoEditor()
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
        #self.selector.setDir(f'{config.dirPhotosBase}Nature-{yearMonth}')
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
        #self.selector.loadData(photo)

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Widgets
        self.table.createWidgets(self.frmLeft)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.createWidgets(self.frmRight)
        #self.selector.createWidgets(self.frmRight)

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