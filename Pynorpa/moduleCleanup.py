"""
 Pynorpa Module for cleaning FTP server.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import os
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog as sd

from BaseWidgets import Button
from TabsApp import TabsApp, TabModule
from gridTable import GridTable
from pynorpaManager import PynorpaManager
from ftpCleaner import FTPCleaner, FTPFile
from Timer import Timer


class ModuleCleanup(TabModule):
    """Pynorpa Module for FTP cleanup."""
    log = logging.getLogger('ModuleCleanup')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.parent = parent
        super().__init__(parent, 'Nettoyage', FTPFile.__name__)
        self.manager = PynorpaManager()
        self.cleaner = FTPCleaner()
        self.table = GridTable('Fichiers à effacer', None, 750)

    def loadData(self):
        self.enableWidgets()
        pass # don't auto-load as it takes too long

    def onLoadData(self):
        """Scan FTP server for files to cleanup."""
        timer = Timer()
        self.setLoadingIcon()
        files = self.cleaner.getFilesToRemove()
        self.table.loadData(files, timer)
        self.enableWidgets()
        self.setLoadingIcon(True)

    def onCleanup(self):
        pass

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftCenterRightFrames()

        self.table.addColumn('Chemin',  FTPFile.getPath, 100)
        self.table.addColumn('Fichier', FTPFile.getName, 240)
        self.table.createWidgets(self.frmLeft)
        self.btnLoad  = self.table.addButton('Charger',  'run',   self.onLoadData)
        self.btnClean = self.table.addButton('Nettoyer', 'clear', self.onCleanup)

    def enableWidgets(self):
        self.btnClean.enableWidget(False)