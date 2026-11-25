"""
 Pynorpa Module for cleaning FTP server.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os

from ftpCleaner import FTPCleaner, FTPFile
from Timer import Timer

from BaseWidgets import Button, Label, ProgressBar
from gridTable import GridTable
from imageWidget import MultiImageWidget
from TabsApp import TabsApp, TabModule
from taxon import TaxonCache


class ModuleCleanup(TabModule):
    """Pynorpa Module for FTP cleanup."""
    log = logging.getLogger('ModuleCleanup')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.parent = parent
        super().__init__(parent, 'Nettoyage FTP', FTPFile.__name__)
        self.progbar = ProgressBar('FTP file cleanup loading', 4)
        self.cleaner = FTPCleaner(self.progbar)
        self.cache = TaxonCache()
        self.table = GridTable('Fichiers à effacer', self.onSelectFile, 743)
        self.imageViewer = MultiImageWidget(showFilename=True)
        self.isLoading = False
        self.files = None
        self.file = None

    def loadData(self):
        self.enableWidgets()
        pass # don't auto-load as it takes too long

    def onLoadData(self):
        """Scan FTP server for files to cleanup."""
        timer = Timer()
        self.isLoading = True
        self.enableWidgets()
        self.progbar.show()
        self.setLoadingIcon()

        self.files = self.cleaner.getFilesToRemove()
        self.table.loadData(self.files, timer)

        self.isLoading = False
        self.progbar.hide()
        self.enableWidgets()
        self.setLoadingIcon(True)

    def onCleanup(self):
        self.isLoading = True
        self.enableWidgets()
        self.progbar.show()
        self.setLoadingIcon()

        self.cleaner.removeFiles(self.files)
        self.files = None
        self.table.loadData([])

        self.isLoading = False
        self.progbar.hide()
        self.enableWidgets()
        self.setLoadingIcon(True)
        

    def onSelectFile(self, file: FTPFile):
        self.file = file
        if not file:
            return
        taxon = self.cache.findByFilename(file.getName())
        if taxon:
            # If known taxon, display its pics
            desc = f'{taxon.getName()} : {taxon.getRankFr()} avec {taxon.countAllPictures()} photos'
            self.lblTaxon.setText(desc)
            self.imageViewer.loadImages(taxon.getPictures())
        else:
            # If unkown taxon, display closest match and websearch
            name = self.cache.filenameToTaxonName(file.getName())
            closest = self.cache.findByClosest(name)
            closeto = f'proche de {closest.getName()}' if closest else 'sans taxon proche'
            desc = f'Taxon inconnu : {name}, {closeto}'
            self.lblTaxon.setText(desc)
            self.imageViewer.loadImages(closest.getPictures() if closest else None)
        self.enableWidgets()

    def onWebSearch(self):
        """Open a web search in browser."""
        # https://www.ecosia.org/search?q=leiobunum
        if self.file:
            query = self.cache.filenameToTaxonName(self.file.getName())
            os.system(f'firefox https://www.ecosia.org/search?q="{query}" &')

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftCenterRightFrames()

        self.table.addColumn('Chemin',  FTPFile.getPath, 100)
        self.table.addColumn('Fichier', FTPFile.getName, 280)
        self.table.createWidgets(self.frmLeft)
        self.btnLoad  = self.table.addButton('Charger',  'run',   self.onLoadData)
        self.btnClean = self.table.addButton('Nettoyer', 'clear', self.onCleanup)
        self.progbar.createWidgets(self.frmLeft)

        self.lblTaxon = Label(self.frmRight, 'Choisir un fichier').pack()
        self.imageViewer.createWidgets(self.frmRight)
        self.btnSearch = Button(self.frmRight, 'Recherche web', self.onWebSearch, 'internet')
        self.btnSearch.pack()

    def enableWidgets(self):
        self.btnLoad.enableWidget(not self.isLoading)
        self.btnClean.enableWidget(self.files is not None)
        self.btnSearch.enableWidget(self.file is not None)