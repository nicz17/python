"""
 Pynorpa Module for backups to external disk.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk

from appParam import AppParam, AppParamCache
from BaseWidgets import Button
from TabsApp import TabsApp, TabModule


class ModuleBackups(TabModule):
    """Pynorpa Module for backup tasks."""
    log = logging.getLogger('ModuleBackups')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.tasks = []
        self.isRunning = False
        self.apCache = AppParamCache()
        super().__init__(parent, 'Backups')

    def loadData(self):
        """Load data and tasks."""
        # TODO display last backup timestamp
        apLastBackup = self.apCache.findByName('backupBook')
        if apLastBackup:
            self.log.info(f'Last backup: {apLastBackup.getDateVal()}')
        self.loadTasks()

    def loadTasks(self):
        """Load the tasks to perform."""
        # TODO check free disk space
        # TODO local database dump
        # TODO check if external disk is mounted
        # TODO copy DB dump to external
        # TODO copy or sync pic directories since last backup
        #self.tasks.append(CheckDiskSpace())

    def runBackups(self):
        self.log.info('Running backup tasks')

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Buttons frame
        self.frmButtons = ttk.Frame(self.frmLeft, padding=5)
        self.frmButtons.pack(anchor=tk.W)

        # Buttons
        self.btnRun = self.addButton('Backup', 'run',  self.runBackups)

    def addButton(self, label: str, icon: str, cmd) -> Button:
        """Add a Tk Button to this module's frmButtons."""
        btn = Button(self.frmButtons, label, cmd, icon)
        btn.pack(9)
        return btn