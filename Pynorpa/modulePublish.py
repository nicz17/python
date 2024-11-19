"""
 Pynorpa Module for creating and uploading HTML pages.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
from TabsApp import *
import exporter
from BaseWidgets import Button

class ModulePublish(TabModule):
    """Pynorpa Module for creating and uploading HTML pages."""
    log = logging.getLogger('ModulePublish')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.tasks = []
        self.isRunning = False
        self.exporter = exporter.Exporter()
        super().__init__(parent, 'Publier')

    def onExport(self):
        """Create HTML pages."""
        self.exporter.buildLinks()

    def onUpload(self):
        """Upload HTML pages."""
        #self.uploader.upload()

    def addButton(self, label: str, icon: str, cmd) -> Button:
        """Add a Tk Button to this module's frmButtons."""
        btn = Button(self.frmButtons, label, cmd, icon)
        btn.pack()
        return btn

    def createWidgets(self):
        """Create user widgets."""

        # Buttons frame
        self.frmButtons = ttk.Frame(self.oFrame, padding=5)
        self.frmButtons.pack(anchor=tk.W)

        # Buttons
        self.btnExport = self.addButton('Exporter', 'internet', self.onExport)
        self.btnUpload = self.addButton('Publier',  'go-up',    self.onUpload)

        # Browser widget 
        # frame = tkinterweb.HtmlFrame(root)
        # frame.load_website(YOUR_WEBSITE)
        # frame.pack(fill="both", expand=True)

    def enableWidgets(self):
        self.btnExport.enableWidget(not self.isRunning)
        self.btnUpload.enableWidget(not self.isRunning)
