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

class ModuleCamera(TabModule):
    """Pynorpa Module for importing photos from camera."""
    log = logging.getLogger('ModuleCamera')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.tasks = []
        super().__init__(parent, 'Caméra')

        self.copier = CopyFromCamera()
        self.tracker = GeoTracker()
        self.renderer = Renderer(self.canTasks, None)
        self.loadTasks()
        self.renderer.drawTasks(self.tasks)

    def loadTasks(self):
        """Load the tasks to perform."""
        self.copier.loadImages()
        self.tracker.prepare()
        #self.tasks.append(TestPynorpaTask(5, self.updateTaskDisplay))
        self.tasks.append(MountCameraTask(self.copier, self.updateTaskDisplay))
        self.tasks.append(CopyFromCameraTask(self.copier, self.updateTaskDisplay))
        self.tasks.append(GeoTrackerTask(self.tracker, self.copier.getNumberImages(), self.updateTaskDisplay))
        self.tasks.append(CreateThumbnailsTask(self.copier, self.updateTaskDisplay))

    def copyFiles(self):
        """Start the file copy tasks."""
        self.log.info('Starting %d tasks', len(self.tasks))
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

    def addButton(self, label: str, cmd):
        """Add a Tk Button to this module's frmButtons."""
        btn = tk.Button(self.frmButtons, text = label, command = cmd)
        btn.pack(side=tk.LEFT)
        return btn

    def createWidgets(self):
        """Create user widgets."""

        # Buttons frame
        self.frmButtons = ttk.Frame(self.oFrame, padding=5)
        self.frmButtons.pack(anchor=tk.W)

        # Buttons
        self.btnCopy = self.addButton('Start', self.copyFiles)
        self.btnOpen = self.addButton('Open',  self.openPhotoDir)

        # Canvas
        self.canTasks = tk.Canvas(master=self.oFrame, bd=0, 
                                  #bg='#e0e0e0', 
                                  height=self.oParent.iHeight-200, 
                                  width=self.oParent.iWidth-210, 
                                  highlightthickness=0)
        self.canTasks.pack(side=tk.LEFT)