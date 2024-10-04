"""
 Pynorpa Module for displaying and editing taxa.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from TabsApp import *
from BaseTree import *
from taxon import Taxon, TaxonCache


class ModuleTaxon(TabModule):
    """Pynorpa Module for taxa."""
    log = logging.getLogger('ModuleTaxon')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        super().__init__(parent, 'Taxons')
        self.cache = TaxonCache()
        self.tree = TaxonTree(self.onSelectTaxon)

    def loadData(self):
        self.cache.load()
        tax: Taxon
        for tax in self.cache.getTopLevelTaxa():
            self.tree.addTaxon(tax)
        #self.tree.addTestItems()


    def onSelectTaxon(self, id: str):
        """Callback for selection of taxon with specified id."""
        taxon: Taxon
        taxon = None
        if id is not None:
            taxon = self.cache.findById(int(id))
        self.log.info('Selected %s', taxon)

        # Display in widgets
        #self.editor.loadData(taxon)

    def createWidgets(self):
        """Create user widgets."""

        # Frames
        self.frmLeft = tk.Frame(master=self.oFrame)
        self.frmLeft.pack(fill=tk.Y, side=tk.LEFT, pady=0)
        self.frmRight = tk.Frame(master=self.oFrame)
        self.frmRight.pack(fill=tk.Y, side=tk.LEFT, pady=6, padx=6)

        # Taxon tree and editor
        self.tree.createWidgets(self.frmLeft)
        #self.editor.createWidgets(self.frmRight)

class TaxonTree(BaseTree):
    """Subclass of BaseTree displaying taxa."""
    log = logging.getLogger('TaxonTree')

    def __init__(self, cbkSelectItem):
        super().__init__(self.onSelectEvent)
        self.cbkSelectItem = cbkSelectItem

    def addTaxon(self, taxon: Taxon):
        """Adds a taxon to the tree."""
        parentId = None
        if taxon.getParent() is not None:
            parentId = str(taxon.getParent())
        self.addItem(str(taxon.getIdx()), taxon.getName(), parentId)
        for child in taxon.getChildren():
            self.addTaxon(child)

    def onSelectEvent(self, event):
        self.cbkSelectItem(self.getSelectedId())
