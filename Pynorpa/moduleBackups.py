"""
 Pynorpa Module for backups to external disk.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk

import DateTools
from appParam import AppParamCache
from BaseWidgets import Button
from pynorpaManager import PynorpaManager, PynorpaException
from TabsApp import TabsApp, TabModule
from PynorpaTask import PynorpaTask, CheckDiskSpace


class ModuleBackups(TabModule):
    """Pynorpa Module for backup tasks."""
    log = logging.getLogger('ModuleBackups')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.tasks = []
        self.isRunning = False
        self.apCache = AppParamCache()
        self.manager = PynorpaManager()
        super().__init__(parent, 'Backups')

    def loadData(self):
        """Load data and tasks."""
        apLastBackup = self.apCache.findByName('backupBook')
        if apLastBackup:
            self.log.info(f'Last backup: {apLastBackup.getDateVal()}')
            sLastAt = f'Dernier backup : {DateTools.datetimeToString(apLastBackup.getDateVal())}'
            self.lblStatus.configure(text=sLastAt)
        self.loadTasks()
        self.renderTasks()

    def loadTasks(self):
        """Load the tasks to perform."""
        self.tasks.append(CheckDiskSpace())
        self.tasks.append(LocalDbBackup())
        # TODO check if external disk is mounted
        # TODO copy DB dump to external
        # TODO copy or sync pic directories since last backup

    def getTasks(self) -> list[PynorpaTask]:
        return self.tasks

    def renderTasks(self):
        for task in self.getTasks():
            task.prepare()
            wid = TaskWidget(task)
            wid.createWidgets(self.frmLeft)

    def runBackups(self):
        """Run the backup tasks."""
        self.log.info('Running backup tasks')
        self.manager.backupDatabase()

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Buttons frame
        self.frmButtons = ttk.Frame(self.frmLeft, padding=5)
        self.frmButtons.pack(anchor=tk.W)

        # Buttons
        self.btnRun = self.addButton('Backup', 'run',  self.runBackups)

        # Status label
        self.lblStatus = ttk.Label(self.frmRight)
        self.lblStatus.pack(side=tk.TOP)

    def addButton(self, label: str, icon: str, cmd) -> Button:
        """Add a Tk Button to this module's frmButtons."""
        btn = Button(self.frmButtons, label, cmd, icon)
        btn.pack(9)
        return btn
    

class LocalDbBackup(PynorpaTask):
    """Create a local database dump."""
    log = logging.getLogger('LocalDbBackup')

    def __init__(self, cbkUpdate=None):
        super().__init__('Base de donnée', 'Sauvegarde locale de la DB', 1)
        self.cbkUpdate = cbkUpdate

    def prepare(self):
        pass

    def run(self):
        super().run()
        PynorpaManager().backupDatabase()
        self.setDesc('Sauvegarde DB effectuée')
        self.cbkUpdate()


class TaskWidget:
    """Widget displaying the details and progress of a task."""
    log = logging.getLogger('TaskWidget')

    def __init__(self, task: PynorpaTask):
        self.task = task

    def createWidgets(self, parent: ttk.Frame):
        """Create user widgets."""
        lblFrame = ttk.LabelFrame(parent, text=self.task.title)
        lblFrame.pack(pady=6, fill=tk.X)
        lblStatus = ttk.Label(lblFrame, text=self.task.desc)
        lblStatus.pack()

    def __str__(self):
        return f'TaskWidget for {self.task.title}'
    
