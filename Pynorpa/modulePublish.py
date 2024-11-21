"""
 Pynorpa Module for creating and uploading HTML pages.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import tkinter as tk
import logging
from TabsApp import *
import exporter
import uploader
from BaseWidgets import Button
from browserWidget import BrowserWidget

class ModulePublish(TabModule):
    """Pynorpa Module for creating and uploading HTML pages."""
    log = logging.getLogger('ModulePublish')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.tasks = []
        self.isRunning = False
        self.exporter = exporter.Exporter()
        self.uploader = uploader.Uploader(True)
        self.web = BrowserWidget()
        super().__init__(parent, 'Publier')

    def onExport(self):
        """Create HTML pages."""
        self.exporter.buildTest()
        self.exporter.buildBasePages()
        self.loadData()

    def onReload(self):
        """Reload our home page."""
        self.loadData()

    def onUpload(self):
        """Upload HTML pages."""
        self.uploader.uploadAll()

    def loadData(self):
        homePage = f'{config.dirWebExport}index.html'
        self.oParent.setStatus(f'Chargement de {homePage}')
        self.web.loadData(homePage)

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
        self.btnExport = self.addButton('Exporter',  'internet', self.onExport)
        self.btnReload = self.addButton('Recharger', 'refresh',  self.onReload)
        self.btnUpload = self.addButton('Publier',   'go-up',    self.onUpload)

        # Browser widget 
        self.web.createWidgets(self.oFrame)

    def enableWidgets(self):
        self.btnExport.enableWidget(not self.isRunning)
        self.btnUpload.enableWidget(not self.isRunning)
        self.btnReload.enableWidget(not self.isRunning)
