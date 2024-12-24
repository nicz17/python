"""
 Pynorpa Module for importing photos from camera.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
from TabsApp import *
from CopyFromCamera import *
from Renderer import *
from PynorpaTask import *
from BaseWidgets import ComboBox, ToolTip, Button
from MapWidget import *
from LocationCache import *

class ModuleCamera(TabModule):
    """Pynorpa Module for importing photos from camera."""
    log = logging.getLogger('ModuleCamera')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.tasks = []
        self.isRunning = False
        self.defLocation = None
        super().__init__(parent, 'Caméra')

        self.copier = CopyFromCamera()
        self.tracker = GeoTracker(self.copier, self.onAddCoords, self.onBoundingBoxMap)
        self.cache = LocationCache()
        self.mapWidget = MapWidget()

    def loadData(self):
        # Renderer and tasks
        self.renderer = Renderer(self.canTasks, None)
        self.loadTasks()
        self.renderer.drawTasks(self.tasks)

    def loadTasks(self):
        """Load the tasks to perform."""
        self.copier.loadImages()
        self.tracker.prepare()
        #self.tasks.append(TestMapView(self.onCenterMap, self.onBoundingBoxMap, self.onAddCoords))
        #self.tasks.append(TestPynorpaTask(5, self.updateTaskDisplay))
        self.tasks.append(MountCameraTask(self.copier, self.updateTaskDisplay))
        self.tasks.append(CopyFromCameraTask(self.copier, self.updateTaskDisplay))
        self.tasks.append(GeoTrackerTask(self.tracker, self.copier.getNumberImages(), self.updateTaskDisplay))
        self.tasks.append(CreateThumbnailsTask(self.copier, self.updateTaskDisplay))

    def copyFiles(self):
        """Start the file copy tasks."""
        self.log.info('Starting %d tasks', len(self.tasks))
        self.isRunning = True
        self.enableWidgets()
        self.setLoadingIcon()

        task: PynorpaTask
        for task in self.tasks:
            if not task.isOver():
                task.prepare()
        self.renderer.drawTasks(self.tasks)

        for task in self.tasks:
            if not task.isOver():
                task.run()
                if not task.isOver():
                    break
        self.renderer.drawTasks(self.tasks)
        self.setLoadingIcon(True)
        self.isRunning = False
        self.enableWidgets()

    def updateTaskDisplay(self):
        """Update the task rendering."""
        self.renderer.drawTasks(self.tasks)
        self.window.update()
        self.window.update_idletasks()

    def openPhotoDir(self):
        """Open the copied photos dir in EyeOfGnome if possible."""
        dir = self.copier.targetDir + 'orig/'
        self.log.info('Opening photos dir %s', dir)
        if dir is not None and os.path.exists(dir):
            #os.system(f'nautilus {dir}')
            os.system(f'eog {dir} &')
        else:
            self.oParent.showErrorMsg(f'Photo directory not found:\n{dir}')

    def onSelectLocation(self, event=None):
        self.defLocation = None
        name = self.cboDefLoc.getValue()
        if name:
            self.defLocation = self.cache.getByName(name)
        if self.defLocation:
            self.mapWidget.setLatLonZoom(self.defLocation.getLatLonZoom())
        self.tracker.setDefaultLocation(self.defLocation)
        self.enableWidgets()

    def onCenterMap(self, center: LatLonZoom):
        """Callback to center the map widget."""
        self.mapWidget.setLatLonZoom(center)

    def onBoundingBoxMap(self, minLat, maxLat, minLon, maxLon):
        """Callback to set the map bounding box."""
        self.mapWidget.setBoundingBox(minLat, minLon, maxLat, maxLon)

    def onAddCoords(self, lat: float, lon: float, iconname=None):
        """Callback after adding GPS data to a photo."""
        self.mapWidget.addMarker(LatLonZoom(lat, lon, 0), iconname)

    def addButton(self, label: str, icon: str, cmd) -> Button:
        """Add a Tk Button to this module's frmButtons."""
        btn = Button(self.frmButtons, label, cmd, icon)
        btn.pack(9)
        return btn

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Buttons frame
        self.frmButtons = ttk.Frame(self.frmLeft, padding=5)
        self.frmButtons.pack(anchor=tk.W)

        # Buttons
        self.btnCopy = self.addButton('Copier', 'run',  self.copyFiles)
        self.btnOpen = self.addButton('Ouvrir', 'open', self.openPhotoDir)
        #ToolTip(self.btnCopy, 'Copier les photos depuis la carte mémoire')

        # Default location selector
        self.frmDefLoc = ttk.LabelFrame(self.frmButtons, text='Lieu par défaut')
        self.frmDefLoc.pack(side=tk.LEFT, padx=5, pady=0)
        self.cboDefLoc = ComboBox(self.onSelectLocation)
        self.cboDefLoc.createWidgets(self.frmDefLoc, 0, 0)
        self.cboDefLoc.setValues([loc.name for loc in self.cache.getLocations()])

        # Canvas
        self.canTasks = tk.Canvas(master=self.frmLeft, bd=0, 
                                  #bg='#e0e0e0', 
                                  bg='#f6f4f2', # Ubuntu theme
                                  height=self.oParent.iHeight-200, 
                                  #width=self.oParent.iWidth-10, 
                                  width=620, 
                                  highlightthickness=0)
        self.canTasks.pack(side=tk.LEFT)

        # Map
        self.mapWidget.createWidgets(self.frmRight, 0, 100)
        self.enableWidgets()

    def enableWidgets(self):
        self.btnCopy.enableWidget(self.defLocation and not self.isRunning)
        self.btnOpen.enableWidget(not self.isRunning)
