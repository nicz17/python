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
from BaseWidgets import BaseEditor, Button, ComboBox, SpinBox
from moduleSelection import TablePhotos, PhotoEditor, TaxonSelector
from PhotoInfo import *
import imageWidget
from MapWidget import MapWidget
from ModalDialog import *
from LatLonZoom import LatLonZoom

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
        self.dirSelector = DirectorySelector(self.onSelectDir)
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

    def onSelectDir(self, dir: str):
        """Change the photos directory and reload our data."""
        self.log.info('Setting dir to %s', dir)
        self.dir = dir
        self.selector.setDir(dir.replace('/photos', ''))
        self.loadData()

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

    def onLocate(self):
        dlgLocate = DialogLocate(self.window, self.photos)
        self.log.info('Opened dialog window, waiting')
        self.window.wait_window(dlgLocate.root)
        self.log.info(f'Dialog closed with data: {dlgLocate.data}')

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Widgets
        self.table.createWidgets(self.frmLeft)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.createWidgets(self.frmRight)
        self.selector.createWidgets(self.frmRight)
        self.dirSelector.createWidgets(self.frmRight)

        # Buttons frame
        self.frmButtons = ttk.Frame(self.frmLeft, padding=5)
        self.frmButtons.pack(anchor=tk.W)

        # Buttons
        #self.btnReload = self.addButton('Recharger', self.loadData, 'refresh')
        self.btnLocate = self.addButton('Localiser', self.onLocate, 'location')

    def addButton(self, label: str, cmd, icon: str) -> Button:
        """Add a Tk Button to this module's frmButtons."""
        btn = Button(self.frmButtons, label, cmd, icon)
        btn.pack()
        return btn
    

class DirectorySelector:
    """Select a photos dir based on year and month."""
    log = logging.getLogger("DirectorySelector")

    def __init__(self, cbkReload):
        self.cbkReload = cbkReload
        dtNow = DateTools.nowDatetime()
        self.year  = dtNow.year
        self.month = dtNow.month
    
    def getYear(self, object=None):
        return self.year
    
    def getMonth(self):
        return self.month
    
    def getDirectory(self):
        return f'{config.dirPhotosBase}Nature-{self.year}-{self.month:02d}/photos'
    
    def onModified(self, event=None):
        self.year  = self.spiYear.getValue()
        self.month = self.cboMonth.getSelectionIndex()+1
        self.enableWidgets()

    def onReload(self):
        self.cbkReload(self.getDirectory())

    def createWidgets(self, parent: ttk.Frame):
        """Create our widgets in the parent frame."""
        self.frmMain = ttk.LabelFrame(parent, text='Sélection de répertoire photos')
        self.frmMain.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=False, pady=5)

        self.cboMonth = ComboBox(self.onModified)
        self.cboMonth.createWidgets(self.frmMain, 0, 0)
        self.cboMonth.setValues(DateTools.aMonthFr)
        self.cboMonth.setValue(DateTools.aMonthFr[self.month-1])

        self.spiYear = SpinBox(self.onModified, self.getYear, 2015, self.year)
        self.spiYear.createWidgets(self.frmMain, 0, 1)
        self.spiYear.setValue(self)

        self.btnReload = Button(self.frmMain, 'Recharger', self.onReload, 'open')
        self.btnReload.grid(0, 2)
        self.enableWidgets()

    def enableWidgets(self):
        enabled = os.path.exists(self.getDirectory())
        self.btnReload.enableWidget(enabled)


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

    def createWidgets(self, parent: ttk.Frame):
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

class DialogLocate(ModalDialog):
    log = logging.getLogger('DialogLocate')

    def __init__(self, parent: tk.Tk, photos: list[PhotoInfo]):
        self.photos = photos
        self.viewer = imageWidget.MultiImageWidget(None, self.onSelectPhoto)
        self.map = MapWidget()
        super().__init__(parent, 'Localisation fine')
        self.root.geometry('1000x700')

    def onSelectPhoto(self, photo: PhotoInfo):
        """Photo selection callback."""
        self.map.setLatLonZoom(LatLonZoom(photo.lat, photo.lon, 15))

    def createWidgets(self):
        self.frmLeft  = ttk.Frame(self.root)
        self.frmRight = ttk.Frame(self.root)
        self.frmLeft.pack( fill=tk.Y, side=tk.LEFT, pady=0)
        self.frmRight.pack(fill=tk.Y, side=tk.LEFT, pady=0, padx=0)

        self.viewer.createWidgets(self.frmLeft)
        self.map.createWidgets(self.frmRight, 6, 10)

        self.btnExit = Button(self.frmRight, 'Fermer', self.exit, 'ok')
        self.btnExit.pack(20)

        self.viewer.loadImages(self.photos)