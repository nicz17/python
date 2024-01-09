"""
 Pynorpa App window based on BaseApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
from BaseApp import *
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
        self.loadTasks()

    def loadTasks(self):
        """Load the tasks to perform."""
        self.tasks.append(Task('Mount Camera', 'Mount camera memory card', 1))
        self.tasks.append(Task('Copy photos', 'Copy 42 pictures from camera memory card', 42))
        self.tasks.append(Task('Create thumbs', 'Create thumbnails for 42 photos', 42))
        self.tasks.append(Task('GeoTracking', 'Add GPS tags to 42 photos', 42))

    def copyFiles(self):
        pass

    def createWidgets(self):
        """Create user widgets."""

        # Buttons
        self.btnCopy = self.addButton('Copier', self.copyFiles)

        # Canvas
        self.canTasks = tk.Canvas(master=self.frmMain, bg='#c0f0f0', bd=0, 
                                height=self.iHeight-50, width=self.iWidth-200, 
                                highlightthickness=0)
        self.canTasks.pack(side=tk.LEFT)