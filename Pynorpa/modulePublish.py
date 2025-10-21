"""
 Pynorpa Module for creating and uploading HTML pages.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import tkinter as tk

import exporter
import uploader
import DateTools
import TextTools

from appParam import AppParamCache
from TabsApp import *
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
        self.uploader = uploader.Uploader()
        self.web = BrowserWidget()
        self.apCache = AppParamCache()
        super().__init__(parent, 'Publier')
        self.isExported = False

    def onExport(self):
        """Create HTML pages."""
        self.setLoadingIcon()
        self.exporter.buildBasePages()
        self.loadData()
        self.setLoadingIcon(True)
        self.isExported = True
        self.enableWidgets()

    def onReload(self):
        """Reload our home page."""
        self.loadData()

    def onUpload(self):
        """Upload HTML pages."""
        self.setLoadingIcon()
        fDuration = self.uploader.uploadModified()
        # TODO add progress bar
        self.setLoadingIcon(True)
        self.isExported = False
        status = f'Publié en {TextTools.durationToString(fDuration)}'
        self.lblStatus.configure(text=status)
        self.enableWidgets()

    def loadData(self):
        tLastUpload = self.apCache.getLastUploadAt()
        homePage = f'{config.dirWebExport}index.html'
        self.oParent.setStatus(f'Chargement de {homePage}')
        status = f'Dernier upload: {DateTools.datetimeToString(tLastUpload)}, {self.uploader.countModified()} photos à publier'
        self.lblStatus.configure(text=status)
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

        # Status label
        self.lblStatus = ttk.Label(self.frmButtons)
        self.lblStatus.pack(side=tk.LEFT)

        # Browser widget 
        self.web.createWidgets(self.oFrame)
        self.enableWidgets()

    def enableWidgets(self):
        self.btnExport.enableWidget(not self.isRunning)
        self.btnUpload.enableWidget(self.isExported)
        self.btnReload.enableWidget(not self.isRunning)
