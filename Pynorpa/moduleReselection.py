"""
 Pynorpa Module for displaying selected photos and re-assigning them to another Taxon.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import datetime as dt
import glob
import logging

import LocationCache
from TabsApp import *
from BaseTable import TableColumn
from BaseWidgets import BaseEditor, Button, ComboBox
from moduleSelection import TablePhotos, PhotoEditor, TaxonSelector, DirectorySelector
from pynorpaManager import PynorpaManager, PynorpaException
from PhotoInfo import *
import imageWidget
from mapWidget import MapWidget
from ModalDialog import *
from LatLonZoom import LatLonZoom
from tkinter import messagebox as mb
from taxon import Taxon, TaxonCache


class ReselectionContext:
    """
    Container class for navigation to reselection module
    at a given timestamp or photo.
    """
    def __init__(self, at: dt.datetime, photo: PhotoInfo):
        self.at = at
        self.photo = photo
    def __str__(self):
        return f'ReselectionContext at {self.at} for {self.photo}'

class ModuleReselection(TabModule):
    """Pynorpa Module for reselecting photos."""
    log = logging.getLogger('ModuleReselection')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.app = parent
        self.window = parent.window
        super().__init__(parent, 'Confirmation', 'ReselectionContext')
        self.locationCache = LocationCache.LocationCache()
        self.taxonCache = TaxonCache()
        self.table = TableReselection(self.onSelectPhoto)
        self.imageWidget = imageWidget.ImageWidget(f'{config.dirPicsBase}medium/blank.jpg')
        self.editor = PhotoEditorReselection()
        self.selector = TaxonReselector(self.onRename)
        self.dirSelector = DirectorySelector(self.onSelectDir)
        self.manager = PynorpaManager()
        self.photos = []
        self.photo = None
        self.dir = None
        self.getDefaultDir()

    def getDefaultDir(self):
        """Find the default photo dir."""
        dir = self.manager.getDefaultDir()
        self.dir =  f'{dir}/photos'
        self.selector.setDir(dir)
        self.log.info(f'Default dir: {self.dir}')

    def loadData(self):
        """Load the photos to display."""
        self.photos = []
        self.setLoadingIcon()
        files = sorted(glob.glob(f'{self.dir}/*.jpg'))
        for file in files:
            photo = PhotoInfo(file)
            photo.identify()
            photo.setCloseTo(self.locationCache.getClosest(photo.lat, photo.lon))
            self.photos.append(photo)
        self.photos = sorted(self.photos, key=lambda pic: pic.tShotAt)
        self.photo = None
        self.table.loadData(self.photos)
        self.setLoadingIcon(True)
        self.app.setStatus(f'Chargé {self.dir}')
        self.enableWidgets()

    def navigateToObject(self, context: ReselectionContext):
        """Navigate to the timestamp in context."""
        self.log.info(f'Navigating to {context}')
        dir = f'{self.manager.getDirAt(context.at)}/photos'
        if dir != self.dir:
            self.onSelectDir(dir)
        if context.photo:
            self.table.selectByIdx(context.photo.getIdx())

    def onSelectDir(self, dir: str):
        """Change the photos directory and reload our data."""
        self.log.info('Setting dir to %s', dir)
        self.dir = dir
        self.selector.setDir(dir.replace('/photos', ''))
        self.loadData()
        self.enableWidgets()

    def onSelectPhoto(self, photo: PhotoInfo):
        """Photo selection callback."""
        self.log.info(f'Selected {photo}')
        thumbfile = None  # Thumb size: 500x500px
        if photo is not None:
            thumbfile = photo.filename.replace('photos/', 'thumbs/')
            if not os.path.exists(thumbfile):
                sCmd = f'convert {photo.filename} -resize 500x500 {thumbfile}'
                os.system(sCmd)
        self.photo = photo
        self.imageWidget.loadData(thumbfile)
        self.editor.loadData(photo)
        self.selector.loadData(photo)
        self.enableWidgets()

    def onRename(self, photo):
        """Callback after selected photo was renamed."""
        self.table.updateObject(photo)
        self.editor.loadData(photo)

    def onLocate(self):
        dlgLocate = DialogLocate(self.window, self.photos)
        self.log.info('Opened dialog window, waiting')
        self.window.wait_window(dlgLocate.root)
        self.log.info(f'Dialog closed with data: {dlgLocate.data}')

    def onAddPic(self, event=None):
        """Add the selected PhotoInfo as picture in gallery."""
        self.log.info(f'Will add {self.photo} to gallery')
        pic = None
        try:
            pic = self.manager.addPicture(self.photo.getNameFull(), self.photo.getClosestLocation())
        except PynorpaException as exc:
            self.app.showErrorMsg(exc)
        if pic is not None:
            self.photo.isAdded = True
            taxon: Taxon
            taxon = pic.getTaxon()
            sTaxonDesc = f'{taxon.getRankFr()} {taxon.getNameFr()}'
            msg = f'{pic.getFilename()}\n{sTaxonDesc}\nPrès de {pic.getLocationName()}\nQualité {pic.getRating()}'
            mb.showinfo('Ajouté', 'Ajouté en galerie', detail=msg)
            # TODO replace mb with dialog to edit remark and quality
        self.enableWidgets()

    def onNavigateTaxon(self):
        """Navigate to the selected photo's taxon, if it can be found."""
        taxon = self.getPhotoTaxon()
        if taxon:
            self.app.navigateToObject(taxon)

    def getPhotoTaxon(self) -> Taxon:
        """Find the selected PhotoInfo's taxon based on the filename."""
        taxon = None
        if self.photo:
            taxon = self.taxonCache.findByFilename(self.photo.getNameShort())
        return taxon

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Widgets
        self.table.createWidgets(self.frmLeft)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.createWidgets(self.frmRight)
        self.selector.createWidgets(self.frmRight)
        self.dirSelector.createWidgets(self.frmRight)
        self.table.setStatus('Chargement...')

        # Buttons
        self.btnLocate = self.addButton('Localiser', self.onLocate, 'location22', 'Dialogue de localisation fine')
        self.btnTaxon  = self.addButton('Taxon', self.onNavigateTaxon, 'go-next', 'Naviguer vers le taxon')
        self.btnAddPic = self.addButton('Ajouter', self.onAddPic, 'add', 'Ajouter cette photo en galerie')
        self.enableWidgets()

    def enableWidgets(self):
        """Enable or disable user widgets."""
        self.btnAddPic.enableWidget(self.photo and not self.photo.isAdded)
        self.btnTaxon.enableWidget(self.getPhotoTaxon() is not None)

    def addButton(self, label: str, cmd, icon: str, tootip=None) -> Button:
        """Add a Tk Button to this module's frmButtons."""
        btn = Button(self.table.frmToolBar, label, cmd, icon, tootip)
        btn.pack(0)
        return btn

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
        self.manager.runSystemCommand(cmd)
        self.manager.runSystemCommand(cmd.replace('photos/', 'thumbs/'))
        self.enableWidgets()
        self.photo.filename = target
        self.cbkReselection(self.photo)

class DialogLocate(ModalDialog):
    log = logging.getLogger('DialogLocate')

    def __init__(self, parent: tk.Tk, photos: list[PhotoInfo], defLocation = None):
        self.photos = photos
        self.photo = None
        self.viewer = imageWidget.MultiImageWidget(None, self.onSelectPhoto)
        self.map = MapWidget()
        self.defLocation = defLocation
        self.lastCoords = None
        self.hasChanges = False
        self.locCache = LocationCache.LocationCache()
        super().__init__(parent, 'Localisation fine')
        self.root.geometry('1150x600+300+150')

    def onSelectPhoto(self, photo: PhotoInfo):
        """Photo selection callback."""
        self.photo = photo
        self.hasChanges = False
        llz = MapWidget.defPosition
        status = 'Sans données GPS'
        if photo and photo.lon and photo.lat:
            llz = LatLonZoom(photo.lat, photo.lon, 17)
            status = f'Près de {photo.getCloseTo()}'
        elif self.defLocation:
            llz = self.defLocation.getLatLonZoom()
            status = f'Lieu : {self.defLocation.getName()}'
        self.map.removeMarkers()
        self.map.setLatLonZoom(llz)
        self.map.addMarker(llz, config.mapMarkerRed)
        self.lblStatus.configure(text=status)
        self.enableWidgets()

    def onSelectLocation(self, event=None):
        name = self.cboDefLoc.getValue()
        if name:
            self.defLocation = self.locCache.getByName(name)
        self.enableWidgets()

    def onRepeatCoords(self):
        """Repeat last defined coordinates on the current photo."""
        if self.lastCoords:
            self.map.removeMarkers()
            self.map.setLatLonZoom(self.lastCoords)
            self.map.addMarker(self.lastCoords, config.mapMarkerRed)
            self.hasChanges = True
            self.enableWidgets()

    def onSave(self):
        """Write the last defined coordinates to the current photo."""
        if self.photo and self.lastCoords:
            self.photo.lat = self.lastCoords.lat
            self.photo.lon = self.lastCoords.lon
            cmd = f'exiftool -GPSLatitude*={self.photo.lat} -GPSLongitude*={self.photo.lon} -overwrite_original {self.photo.filename}'
            self.log.info(cmd)
            os.system(cmd)
            self.photo.setCloseTo(self.locCache.getClosest(self.photo.lat, self.photo.lon))
            self.hasChanges = False
            self.enableWidgets()

    def onRightClickSetMarker(self, coords):
        """Add a map marker at right click location."""
        llz = LatLonZoom(coords[0], coords[1], self.map.getZoom())
        self.map.removeMarkers()
        self.map.addMarker(llz, config.mapMarkerGreen)
        self.lastCoords = llz
        self.hasChanges = True
        self.enableWidgets()

    def createWidgets(self):
        # Left and right frames
        self.frmLeft  = ttk.Frame(self.root)
        self.frmRight = ttk.Frame(self.root)
        self.frmLeft.pack( fill=tk.Y, side=tk.LEFT, pady=0)
        self.frmRight.pack(fill=tk.Y, side=tk.LEFT, pady=0, padx=0)

        # Photo viewer
        self.viewer.createWidgets(self.frmLeft, 6)

        # Default location selector
        self.frmDefLoc = ttk.LabelFrame(self.frmRight, text='Lieu par défaut')
        self.frmDefLoc.pack(side=tk.TOP, fill=tk.X, padx=5, pady=6)
        self.cboDefLoc = ComboBox(self.onSelectLocation)
        self.cboDefLoc.createWidgets(self.frmDefLoc, 0, 0)
        self.cboDefLoc.setValues([loc.name for loc in self.locCache.getLocations()])
        if self.defLocation:
            self.cboDefLoc.setValue(self.defLocation.getName())

        # Map widget
        self.map.createWidgets(self.frmRight, 6, 10)
        self.map.mapView.add_right_click_menu_command(label='Placer la photo ici',
            command=self.onRightClickSetMarker, pass_coords=True)
        
        # Location label
        self.lblStatus = ttk.Label(self.frmRight, text='Status')
        self.lblStatus.pack(fill=tk.X)

        # Buttons
        self.frmButtons = ttk.Frame(self.frmRight)
        self.frmButtons.pack(fill=tk.X, pady=10)
        self.btnRepeat = Button(self.frmButtons, 'Reprendre', self.onRepeatCoords, 'location22')
        self.btnSave   = Button(self.frmButtons, 'Enregistrer', self.onSave, 'filesave')
        self.btnExit   = Button(self.frmButtons, 'Fermer', self.exit, 'ok')
        self.btnRepeat.pack()
        self.btnSave.pack()
        self.btnExit.pack()

        self.viewer.loadImages(self.photos)
        self.enableWidgets()

    def enableWidgets(self):
        self.btnRepeat.enableWidget(self.lastCoords is not None)
        self.btnSave.enableWidget(self.hasChanges)