"""Module for quality check issues."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import tkinter as tk

from BaseTable import AdvTable, TableColumn
from BaseWidgets import BaseEditor
from imageWidget import CaptionImageWidget
from TabsApp import TabModule, TabsApp
from qualityChecker import QualityChecker, QualityIssue


class ModuleQuality(TabModule):
    """Class ModuleQuality"""
    log = logging.getLogger("ModuleQuality")

    def __init__(self, parent: TabsApp):
        """Constructor."""
        self.window = parent.window
        self.checker = None
        self.table   = QualityTable(self.onSelectIssue)
        self.editor  = QualityIssueEditor(parent)
        self.imageWidget = CaptionImageWidget(f'{config.dirPicsBase}medium/blank.jpg')
        super().__init__(parent, 'Qualité', QualityIssue.__name__)

    def loadData(self):
        """Load data from cache and populate table."""
        self.checker = QualityChecker()
        self.checker.runAllChecks()
        self.table.loadData(self.checker.getIssues())

    def onSelectIssue(self, issue: QualityIssue):
        self.editor.loadData(issue)
        if issue:
            self.imageWidget.loadThumb(issue.getPic())
        else:
            self.imageWidget.loadThumb(None)

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()
        self.table.createWidgets(self.frmLeft, 36)
        self.table.addRefreshButton(self.loadData)
        self.editor.createWidgets(self.frmRight)
        self.imageWidget.createWidgets(self.frmRight)

    def __str__(self):
        return 'ModuleQuality'
    

class QualityTable(AdvTable):
    """Class QualityTable"""
    log = logging.getLogger("QualityTable")

    def __init__(self, cbkSelect):
        """Constructor."""
        super().__init__(cbkSelect, "Problèmes", 6)

    def addColumns(self):
        """Define the table columns."""
        self.addColumn(TableColumn('Type', QualityIssue.getKind, 60))
        self.addColumn(TableColumn('Description', QualityIssue.getDesc, 600))

    def loadData(self, issues: list[QualityIssue]):
        """Display the specified objects in this table."""
        self.clear()
        self.data = issues
        self.addRows(issues)

    def __str__(self):
        return 'QualityTable'


class QualityIssueEditor(BaseEditor):
    """Editor for quality issue details. Read-only."""
    log = logging.getLogger('QualityIssueEditor')

    def __init__(self, app: TabsApp):
        """Constructor."""
        super().__init__(None, '#62564f')
        self.app = app
        self.issue = None

    def loadData(self, issue: QualityIssue):
        """Display the specified object in this editor."""
        self.setValue(issue)
        self.issue = issue

    def navigate(self):
        self.log.info(f'Navigating to {self.issue.getLink()}')
        self.app.navigateToObject(self.issue.getLink())

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Propriétés du problème')
        self.widKind = self.addTextReadOnly('Type', QualityIssue.getKind)
        self.widDesc = self.addTextArea('Descr.',   QualityIssue.getDesc)
        self.widDesc = self.addTextArea('Détails',  QualityIssue.getDetails)
        self.createButtons(False, False, False)
        self.btnResolve = self.addButton('Résoudre', self.navigate, 'go-next')
        self.enableWidgets(True)

    def __str__(self):
        return 'QualityIssueEditor'

