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
import TextTools
from TabsApp import *
from PhotoInfo import *
from BaseTable import *
from taxon import Taxon, TaxonRank, TaxonCache
from picture import Picture, PictureCache
from tkinter import filedialog as fd

# TODO:
# add Taxon assignment section:
# suggest selection name based on current taxon
# no need for Taxon tree, maybe ComboBox with child taxa ?
# if no matching taxon, take user input
# option to set GPS data from default location if missing

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
        self.selector = TaxonSelector()
        super().__init__(parent, 'Sélection')
        self.photos = []
        self.dir = None

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
        self.photos = []
        self.getDefaultDir()
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

        # Buttons frame
        self.frmButtons = ttk.Frame(self.frmLeft, padding=5)
        self.frmButtons.pack(anchor=tk.W)

        # Buttons
        self.btnReload = self.addButton('Recharger', self.loadData)
        self.btnOpen   = self.addButton('Ouvrir', self.selectDir)

    def addButton(self, label: str, cmd):
        """Add a Tk Button to this module's frmButtons."""
        btn = tk.Button(self.frmButtons, text = label, command = cmd)
        btn.pack(side=tk.LEFT)
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
        basename = input.replace(' ', '-')
        if taxon:
            basename = TextTools.lowerCaseFirst(taxon.getName()).replace(' ', '-')
            if taxon.getRank() == TaxonRank.GENUS:
                basename += '-sp'
        seq = self.getSequenceNext(basename, taxon)
        if taxon and taxon.getRank().value < TaxonRank.GENUS.value:
            seq = int(self.photo.getNameShort()[-8:-4])
        self.newName = f'{basename}{seq:03d}.jpg'

    def getSequenceNext(self, basename: str, taxon: Taxon) -> int:
        """Get the next number in sequence for renaming the photo."""
        imax = 0
        if taxon:
            picsDb = self.picCache.getForTaxon(taxon.getIdx())
            self.log.info(f'Found {len(picsDb)} pictures for {taxon}:')
            for pic in picsDb:
                self.log.info(f'  {pic}')
                seq = int(pic.getFilename()[-7:-4])
                imax = max(seq, imax)
        picsLocal = glob.glob(f'{self.dir}/photos/{basename}*.jpg')
        self.log.info(f'Found {len(picsLocal)} local files for {basename}:')
        for file in picsLocal:
            self.log.info(f'  {file}')
            seq = int(file[-7:-4])
            imax = max(seq, imax)
        return imax+1

    def loadData(self, photo: PhotoInfo):
        """Sets the original photo to select and rename."""
        self.photo = photo
        if self.newName:
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

    def onModified(self, event = None):
        """Callback for user input. Look for a matching taxon."""
        input = self.txtInput.get().strip()
        if input and len(input) > 2:
            self.log.info('Looking for taxon named like %s', f'%{input}%')
            where = f"taxName like '%{input.replace(' ', '%')}%'"
            ids = self.taxonCache.fetchFromWhere(where)
            taxon = None
            if ids and len(ids) > 0:
                taxon = self.taxonCache.findById(ids[0])
                taxonName = f'{taxon.getRankFr()} : {taxon.getName()} ({taxon.getNameFr()})'
                self.lblTaxon.configure(text=taxonName)
            else:
                self.newName = f'{input}-sp00x.jpg'
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

        self.lblTaxon = tk.Label(self.frmSelect, text='Taxon non défini')
        self.lblTaxon.pack()

        self.lblName = tk.Label(self.frmSelect, text='Choisir un taxon ou un nom')
        self.lblName.pack()

        self.btnSelect = self.addButton('Sélectionner', self.onSelect)
        self.btnClear  = self.addButton('Effacer', self.onClear)
        self.btnGimp   = self.addButton('Ouvrir avec Gimp', self.onOpenGimp)
        self.enableWidgets()

    def addButton(self, label: str, cmd):
        """Add a Tk Button to this module's frmButtons."""
        btn = tk.Button(self.frmSelect, text=label, command=cmd)
        btn.pack(side=tk.LEFT, padx=3, pady=3)
        return btn

    def enableWidgets(self):
        """Enable or disable our widgets."""
        self.enableWidget(self.btnSelect, self.photo is not None and self.newName is not None)
        self.enableWidget(self.btnGimp, self.lastSelected is not None)
        self.enableWidget(self.btnClear, self.newName is not None)

    def enableWidget(self, oWidget, enabled: bool):
        """Enable or disable the widget."""
        if oWidget:
            oWidget['state'] = tk.NORMAL if enabled else tk.DISABLED

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