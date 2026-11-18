"""
 Pynorpa Module for cleaning FTP server.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging

from ftpCleaner import FTPCleaner, FTPFile
from Timer import Timer

from gridTable import GridTable
from TabsApp import TabsApp, TabModule


class ModuleCleanup(TabModule):
    """Pynorpa Module for FTP cleanup."""
    log = logging.getLogger('ModuleCleanup')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.parent = parent
        super().__init__(parent, 'Nettoyage FTP', FTPFile.__name__)
        self.cleaner = FTPCleaner()
        self.table = GridTable('Fichiers à effacer', None, 743)
        self.isLoading = False

    def loadData(self):
        self.enableWidgets()
        pass # don't auto-load as it takes too long

    def onLoadData(self):
        """Scan FTP server for files to cleanup."""
        timer = Timer()
        self.isLoading = True
        self.enableWidgets()
        self.setLoadingIcon()

        files = self.cleaner.getFilesToRemove()
        self.table.loadData(files, timer)

        self.isLoading = False
        self.enableWidgets()
        self.setLoadingIcon(True)

    def onCleanup(self):
        pass

    def onSelectFile(self, file: FTPFile):
        pass
        # TODO display details: unkown taxon, or taxon pics if known, websearch

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftCenterRightFrames()

        self.table.addColumn('Chemin',  FTPFile.getPath, 100)
        self.table.addColumn('Fichier', FTPFile.getName, 280)
        self.table.createWidgets(self.frmLeft)
        self.btnLoad  = self.table.addButton('Charger',  'run',   self.onLoadData)
        self.btnClean = self.table.addButton('Nettoyer', 'clear', self.onCleanup)

    def enableWidgets(self):
        self.btnLoad.enableWidget(not self.isLoading)
        self.btnClean.enableWidget(self.table.getSize() > 0)