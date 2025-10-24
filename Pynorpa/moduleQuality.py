"""Module for quality check issues."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging

from BaseTable import AdvTable, TableColumn
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
        self.imageWidget = CaptionImageWidget(f'{config.dirPicsBase}medium/blank.jpg')
        super().__init__(parent, 'Qualité')

    def loadData(self):
        """Load data from cache and populate table."""
        self.checker = QualityChecker()
        self.checker.runAllChecks()
        self.table.loadData(self.checker.getIssues())

    def onSelectIssue(self, issue: QualityIssue):
        if issue:
            self.imageWidget.loadThumb(issue.getPic())
        else:
            self.imageWidget.loadThumb(None)

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()
        self.table.createWidgets(self.frmLeft, 36)
        self.table.addRefreshButton(self.loadData)
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
        self.addColumn(TableColumn('Description', QualityIssue.getDesc, 700))

    def loadData(self, issues: list[QualityIssue]):
        """Display the specified objects in this table."""
        self.clear()
        self.data = issues
        self.addRows(issues)

    def __str__(self):
        return 'QualityTable'
    

# TODO add class QualityIssueEditor

