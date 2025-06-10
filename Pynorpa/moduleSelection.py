"""
 Pynorpa Module for displaying photo previews and assigning them to a Taxon.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import glob
import json
import logging
import re

import BaseWidgets
import imageWidget
import DateTools
import TextTools
from TabsApp import *
from PhotoInfo import *
from BaseTable import *
import LocationCache
from taxon import Taxon, TaxonRank, TaxonCache
from picture import PictureCache
from tkinter import filedialog as fd
from Timer import Timer


class ModuleSelection(TabModule):
    """Pynorpa Module for photos."""
    log = logging.getLogger('ModuleSelection')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.app = parent
        self.window = parent.window
        self.table = TablePhotos(self.onSelectPhoto)
        #self.mapWidget = MapWidget()
        self.imageWidget = imageWidget.ImageWidget(f'{config.dirPicsBase}medium/blank.jpg')
        self.editor = PhotoEditor()
        self.selector = TaxonSelector()
        self.locationCache = LocationCache.LocationCache()
        super().__init__(parent, 'Sélection')
        self.photos = []
        self.dir = None
        self.getDefaultDir()

    def getDefaultDir(self):
        """Find the default photo dir."""
        yearMonth = DateTools.nowAsString('%Y-%m')
        self.dir = f'{config.dirPhotosBase}Nature-{yearMonth}/orig'
        if not os.path.exists(self.dir):
            self.log.info('Revert to previous month for default dir')
            yearMonth = DateTools.timestampToString(DateTools.addDays(DateTools.now(), -28), '%Y-%m')
            self.dir = f'{config.dirPhotosBase}Nature-{yearMonth}/orig'
        self.selector.setDir(f'{config.dirPhotosBase}Nature-{yearMonth}')
        self.log.info('Default dir: %s', self.dir)

    def loadData(self):
        """Load the photos to display."""
        self.setLoadingIcon()
        timer = Timer()
        self.photos = []
        metadata = self.loadMetadata()
        files = sorted(glob.glob(f'{self.dir}/*.JPG'))
        for file in files:
            photo = PhotoInfo(file)
            photo.identify()
            if metadata and photo.getNameShort() in metadata['orig']:
                idxLocClosest = metadata['orig'][photo.getNameShort()]['closeTo']
                #self.log.info(f'Using metadata closeTo {idxLocClosest} for {photo.getNameShort()}')
                photo.setCloseTo(self.locationCache.getById(idxLocClosest))
            else:
                photo.setCloseTo(self.locationCache.getClosest(photo.lat, photo.lon))
            self.photos.append(photo)
        self.table.loadData(self.photos)
        self.setLoadingIcon(True)
        self.app.setStatus(f'Chargé {self.dir} en {timer.getElapsed()}')
        self.writeMetadata()

    def loadMetadata(self):
        """Read metadata about orig photos from a json file."""
        filename = f'{self.dir.removesuffix("orig")}metadata.json'
        metadata = None
        if os.path.exists(filename):
            self.log.info(f'Loading metadata from {filename}')
            file = open(filename, 'r')
            metadata = json.load(file)
            file.close()
        else:
            self.log.info(f'No metadata found under {filename}')
        return metadata

    def writeMetadata(self):
        """Write metadata about orig photos to a json file."""
        filename = f'{self.dir.removesuffix("orig")}metadata.json'
        self.log.info(f'Writing metadata to {filename}')
        metadata = {
            'tAt': DateTools.nowAsString(),
            'orig': {}
        }
        photo: PhotoInfo
        for photo in self.photos:
            loc = photo.getClosestLocation()
            metadata['orig'][photo.getNameShort()] = {
                'closeTo': loc.getIdx() if loc else None
            }
        file = open(filename, 'w')
        file.write(json.dumps(metadata, indent=2))
        file.close()


    def onSelectPhoto(self, photo: PhotoInfo):
        """Photo selection callback."""
        self.log.info(f'Selected {photo}')
        self.imageWidget.loadThumb(photo)
        #self.mapWidget.loadData(photo)
        self.editor.loadData(photo)
        self.selector.loadData(photo)

    def selectDir(self):
        """Display a dialog to choose a photo dir."""
        self.dir = fd.askdirectory(mustexist=True, initialdir=config.dirPhotosBase)
        self.selector.setDir(self.dir.replace('orig', ''))
        self.oParent.setStatus(f'Selected {self.dir}')
        self.loadData()

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Widgets
        self.table.createWidgets(self.frmLeft)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.createWidgets(self.frmRight)
        self.selector.createWidgets(self.frmRight)
        self.table.setStatus('Chargement...')

        # Buttons frame
        self.frmButtons = ttk.Frame(self.frmLeft, padding=5)
        self.frmButtons.pack(anchor=tk.W)

        # Buttons
        self.btnReload = self.addButton('Recharger', self.loadData, 'refresh')
        self.btnOpen   = self.addButton('Ouvrir', self.selectDir, 'open')

    def addButton(self, label: str, cmd, icon: str) -> BaseWidgets.Button:
        """Add a Tk Button to this module's frmButtons."""
        btn = BaseWidgets.Button(self.table.frmToolBar, label, cmd, icon)
        btn.pack(0)
        return btn
    
class TaxonSelector():
    """Widget to assign a taxon to an original photo."""
    log = logging.getLogger("TaxonSelector")

    def __init__(self):
        """Constructor. Loads the Taxon cache."""
        self.taxonCache = TaxonCache()
        self.picCache = PictureCache()
        self.photo = None # PhotoInfo to rename
        self.newName = None
        self.lastSelected = None
        self.dir = None  # For example Pictures/Nature-2024-10

    def buildNewName(self, taxon: Taxon, input: str):
        """Build a new filename from the specified taxon or user input."""
        basename = input.replace(' ', '-').lower()
        if taxon:
            basename = TextTools.lowerCaseFirst(taxon.getName()).replace(' ', '-')
            if taxon.getRank() == TaxonRank.GENUS:
                basename += '-sp'
        seq = self.getSequenceNext(basename, taxon)
        if taxon and taxon.getRank().value < TaxonRank.GENUS.value:
            #seq = int(self.photo.getNameShort()[-8:-4])
            seq = self.extractNumber(self.photo.getNameShort())
        self.newName = f'{basename}{seq:03d}.jpg'

    def getSequenceNext(self, basename: str, taxon: Taxon) -> int:
        """Get the next number in sequence for renaming the photo."""
        imax = 0
        if taxon:
            picsDb = self.picCache.getForTaxon(taxon.getIdx())
            self.log.info(f'Found {len(picsDb)} pictures for {taxon}:')
            for pic in picsDb:
                self.log.info(f'  {pic}')
                #seq = int(pic.getFilename()[-7:-4])
                seq = self.extractNumber(pic.getFilename())
                imax = max(seq, imax)
        picsLocal = glob.glob(f'{self.dir}/photos/{basename}*.jpg')
        self.log.info(f'Found {len(picsLocal)} local files for {basename}:')
        for file in picsLocal:
            self.log.info(f'  {file}')
            #seq = int(file[-7:-4])
            seq = self.extractNumber(file)
            imax = max(seq, imax)
        return imax+1
    
    def extractNumber(self, filename: str) -> int:
        """Extracts the last number sequence from a file name."""
        if filename:
            listNums = re.findall(r'\d+', filename)
            return int(listNums[-1]) if listNums else None
        return None 

    def loadData(self, photo: PhotoInfo):
        """Sets the original photo to select and rename."""
        self.photo = photo
        if self.photo:
            self.onModified()

    def setDir(self, dir: str):
        """Set the base dir, for example Pictures/Nature-2024-10"""
        self.dir = dir

    def onSelect(self):
        """Selection button command."""
        target = f'{self.dir}/photos/{self.newName}'
        cmd = f'cp {self.photo.filename} {target}'
        self.log.info(cmd)
        os.system(cmd)
        self.lastSelected = target
        self.lblName.configure(text=f'Copié sous {self.newName}')
        self.newName = None
        self.enableWidgets()

    def onOpenGimp(self):
        """Open with Gimp button command."""
        if self.lastSelected:
            cmd = f'gimp {self.lastSelected} &'
            os.system(cmd)

    def onClear(self):
        """Clear any user inputs."""
        self.newName = None
        self.txtInput.delete(0, tk.END)
        self.lblName.configure(text='Choisir un taxon ou un nom')
        self.lblTaxon.configure(text='Taxon non défini')
        self.enableWidgets()
        self.txtInput.focus_set()

    def onModified(self, event=None):
        """Callback for user input. Look for a matching taxon."""
        input = self.txtInput.get()
        if input and len(input) > 2:
            self.log.info('Looking for taxon named like %s', f'%{input}%')
            #where = f"taxName like '%{input.replace(' ', '%')}%'"
            where = f"taxName like '%{input.replace(' ', '% %')}%'"
            ids = self.taxonCache.fetchFromWhere(where)
            taxon = None
            if ids and len(ids) > 0:
                taxon = self.taxonCache.findById(ids[0])
                taxonName = f'{taxon.getRankFr()} : {taxon.getName()} ({taxon.getNameFr()})'
                self.lblTaxon.configure(text=taxonName)
            else:
                #self.newName = f'{input}-sp00x.jpg'
                self.lblTaxon.configure(text='Pas de taxon trouvé')
            self.buildNewName(taxon, input)
            self.lblName.configure(text=self.newName)
        self.enableWidgets()

    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        self.frmSelect = ttk.LabelFrame(parent, text='Sélection de taxon')
        self.frmSelect.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=False, pady=5)

        self.txtInput = ttk.Entry(self.frmSelect, width=50)
        self.txtInput.pack(fill=tk.X, padx=3)
        self.txtInput.bind('<KeyRelease>', self.onModified)

        self.lblTaxon = ttk.Label(self.frmSelect, text='Taxon non défini')
        self.lblTaxon.pack()

        self.lblName = ttk.Label(self.frmSelect, text='Choisir un taxon ou un nom')
        self.lblName.pack()

        self.btnSelect = self.addButton('Sélectionner', self.onSelect, 'ok')
        self.btnClear  = self.addButton('Effacer', self.onClear, 'clear-bar')
        self.btnGimp   = self.addButton('Ouvrir dans Gimp', self.onOpenGimp, 'gimp')
        self.enableWidgets()

    def addButton(self, label: str, cmd, icon: str) -> BaseWidgets.Button:
        """Add a Tk Button to this module's frmButtons."""
        btn = BaseWidgets.Button(self.frmSelect, label, cmd, icon)
        btn.pack()
        return btn

    def enableWidgets(self):
        """Enable or disable our widgets."""
        self.btnSelect.enableWidget(self.photo is not None and self.newName is not None)
        self.btnGimp.enableWidget(self.lastSelected is not None)
        self.btnClear.enableWidget(self.txtInput.get())

    def enableWidget(self, oWidget, enabled: bool):
        """Enable or disable the widget."""
        if oWidget:
            oWidget['state'] = tk.NORMAL if enabled else tk.DISABLED

class TablePhotos(TableWithColumns):
    """Table widget for Pynorpa photo."""
    log = logging.getLogger("TablePhotos")

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        self.log.info('Constructor')
        super().__init__(cbkSelect, 'photos')
        self.setColumns()

    def setColumns(self):
        self.addColumn(TableColumn('Nom',     PhotoInfo.getNameNoExt,    130))
        self.addColumn(TableColumn('Date',    PhotoInfo.getShotAtString, 150))
        self.addColumn(TableColumn('Près de', PhotoInfo.getCloseTo,      300))

    def loadData(self, photos: list[PhotoInfo]):
        """Display the specified photos in this table."""
        self.log.info('Loading %d photos', len(photos))
        self.clear()
        self.data = photos
        self.addRows(photos)

    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        super().createWidgets(parent)

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