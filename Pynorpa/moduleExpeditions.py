"""Module moduleExpeditions"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from BaseTable import *
from TabsApp import *
import BaseWidgets
from imageWidget import MultiImageWidget
from expedition import Expedition, ExpeditionCache


class ModuleExpeditions(TabModule):
    """Class ModuleExpeditions"""
    log = logging.getLogger("ModuleExcursions")

    def __init__(self, parent: TabsApp):
        """Constructor."""
        self.window = parent.window
        self.table  = ExpeditionTable(self.onSelectExpedition)
        self.editor = ExpeditionEditor(self.onSaveExpedition)
        self.photos = MultiImageWidget()
        super().__init__(parent, 'Excursions')

    def loadData(self):
        """Load data from cache and populate table."""
        self.expeditionCache = ExpeditionCache()
        self.expeditionCache.load()
        self.table.loadData(self.expeditionCache.getExpeditions())

    def onSelectExpedition(self, expedition: Expedition):
        """Display selected object in editor."""
        self.editor.loadData(expedition)

    def onSaveExpedition(self, expedition: Expedition):
        """Save changes to edited object."""
        pass

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()
        self.table.createWidgets(self.frmLeft)
        self.editor.createWidgets(self.frmRight)
        self.photos.createWidgets(self.frmRight)

    def __str__(self):
        return "ModuleExpeditions"


class ExpeditionTable(TableWithColumns):
    """Class ExpeditionTable"""
    log = logging.getLogger("ExpeditionTable")

    def __init__(self, cbkSelect):
        """Constructor."""
        super().__init__(cbkSelect, "expeditions")
        self.addColumn(TableColumn('Titre', Expedition.getName, 256))
        self.addColumn(TableColumn('Lieu',  Expedition.getLocationName, 256))
        self.addColumn(TableColumn('Date',  Expedition.getFrom, 160))

    def loadData(self, expeditions):
        """Display the specified objects in this table."""
        self.clear()
        self.data = expeditions
        self.addRows(expeditions)

    def __str__(self):
        return "ExpeditionTable"


class ExpeditionEditor(BaseWidgets.BaseEditor):
    """Class ExpeditionEditor"""
    log = logging.getLogger("ExpeditionEditor")

    def __init__(self, cbkSave):
        """Constructor."""
        super().__init__(cbkSave, '#62564f')
        self.expedition = None

    def loadData(self, expedition: Expedition):
        """Display the specified object in this editor."""
        self.expedition = expedition
        self.setValue(expedition)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Excursion Editor')
        
        self.widName = self.addText('Titre', Expedition.getName)
        self.widDesc = self.addTextArea('Description', Expedition.getDesc)
        self.widLocation = self.addTextReadOnly('Lieu', Expedition.getLocationName)
        self.widFrom = self.addDateTime('Début', Expedition.getFrom)
        self.widTo = self.addDateTime('Fin', Expedition.getTo)
        self.widTrack = self.addText('GeoTrack', Expedition.getTrack)
        
        self.createButtons(True, True, False)
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable or disable widgets of this editor."""
        editing  = self.expedition is not None
        modified = self.hasChanges(self.expedition)
        super().enableWidgets(editing)
        self.enableButtons(modified, modified, False)

    def __str__(self):
        return "ExpeditionEditor"


