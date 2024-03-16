"""
 Pynorpa App window based on BaseApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
from BaseApp import *
from CopyFromCamera import *
from Renderer import *
from PynorpaTask import *

class PynorpaApp(BaseApp):
    """Pynorpa App window."""
    log = logging.getLogger('PynorpaApp')

    def __init__(self) -> None:
        """Constructor."""
        self.tasks = []
        self.iHeight = 800
        self.iWidth  = 1000
        sGeometry = f'{self.iWidth}x{self.iHeight}'
        super().__init__('Pynorpa', sGeometry)

        self.copier = CopyFromCamera()
        self.tracker = GeoTracker()

        self.renderer = Renderer(self.canTasks, self.window)
        self.loadTasks()
        self.renderer.drawTasks(self.tasks)

    def loadTasks(self):
        """Load the tasks to perform."""
        self.copier.loadImages()
        self.tracker.prepare()
        self.tasks.append(TestPynorpaTask(5, self.updateTaskDisplay))
        self.tasks.append(MountCameraTask(self.copier, self.updateTaskDisplay))
        self.tasks.append(CopyFromCameraTask(self.copier, self.updateTaskDisplay))
        self.tasks.append(GeoTrackerTask(self.tracker, self.updateTaskDisplay))
        #self.tasks.append(TestPynorpaTask(10, self.updateTaskDisplay))
        self.tasks.append(PynorpaTask('Create thumbs', 'Not implemented yet', self.copier.getNumberImages()))

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
            self.showErrorMsg(f'Photo directory not found:\n{dir}')

    def createWidgets(self):
        """Create user widgets."""

        # Buttons
        self.btnCopy = self.addButton('Start', self.copyFiles)
        self.btnOpen = self.addButton('Open',  self.openPhotoDir)

        # Canvas
        self.canTasks = tk.Canvas(master=self.frmMain, bg='#e0e0e0', bd=0, 
                                height=self.iHeight-50, width=self.iWidth-200, 
                                highlightthickness=0)
        self.canTasks.pack(side=tk.LEFT)