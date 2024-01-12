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
from Task import *

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

        self.renderer = Renderer(self.canTasks, self.window)
        self.loadTasks()
        self.renderer.drawTasks(self.tasks)

    def loadTasks(self):
        """Load the tasks to perform."""
        self.copier.loadImages()
        self.tasks.append(Task('Mount Camera', 'Mount camera memory card', 1))
        self.tasks.append(Task('Copy photos', 'Copy pictures from camera memory card', self.copier.getNumberImages()))
        self.tasks.append(Task('Create thumbs', 'Create photo thumbnails', self.copier.getNumberImages()))
        self.tasks.append(Task('GeoTracking', 'Add GPS tags to 42 photos', 42))

    def copyFiles(self):
        """Start the file copy tasks."""
        self.log.info('Starting %d tasks', len(self.tasks))
        if self.copier.isCameraMounted():
            self.tasks[0].inc()
            self.tasks[0].setDesc(f'Camera is mounted at {self.copier.getCameraDir()}')
        else:
            self.tasks[0].setDesc(f'Camera not mounted at {self.copier.getCameraDir()}')
        self.renderer.drawTasks(self.tasks)

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
        self.canTasks = tk.Canvas(master=self.frmMain, bg='#c0f0f0', bd=0, 
                                height=self.iHeight-50, width=self.iWidth-200, 
                                highlightthickness=0)
        self.canTasks.pack(side=tk.LEFT)