"""
 Pynorpa Module for displaying and editing taxa.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from TabsApp import *
from BaseTree import *
import BaseWidgets
from taxon import Taxon, TaxonCache


class ModuleTaxon(TabModule):
    """Pynorpa Module for taxa."""
    log = logging.getLogger('ModuleTaxon')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        super().__init__(parent, 'Taxons')
        self.cache  = TaxonCache()
        self.tree   = TaxonTree(self.onSelectTaxon)
        self.editor = TaxonEditor(self.onSaveTaxon)

    def loadData(self):
        self.cache.load()
        tax: Taxon
        for tax in self.cache.getTopLevelTaxa():
            self.tree.addTaxon(tax)

    def onSelectTaxon(self, id: str):
        """Callback for selection of taxon with specified id."""
        taxon: Taxon
        taxon = None
        if id is not None:
            taxon = self.cache.findById(int(id))
        self.log.info('Selected %s', taxon)

        # Display in widgets
        self.editor.loadData(taxon)

    def onSaveTaxon(self, taxon: Taxon):
        pass

    def createWidgets(self):
        """Create user widgets."""

        # Frames
        self.frmLeft = tk.Frame(master=self.oFrame)
        self.frmLeft.pack(fill=tk.Y, side=tk.LEFT, pady=0)
        self.frmRight = tk.Frame(master=self.oFrame)
        self.frmRight.pack(fill=tk.Y, side=tk.LEFT, pady=6, padx=6)

        # Taxon tree and editor
        self.tree.createWidgets(self.frmLeft)
        self.editor.createWidgets(self.frmRight)

class TaxonTree(BaseTree):
    """Subclass of BaseTree displaying taxa."""
    log = logging.getLogger('TaxonTree')

    def __init__(self, cbkSelectItem):
        super().__init__(self.onSelectEvent)
        self.cbkSelectItem = cbkSelectItem

    def addTaxon(self, taxon: Taxon):
        """Adds a taxon and its children to the tree."""
        parentId = None
        if taxon.getParent() is not None:
            parentId = str(taxon.getParent())
        self.addItem(str(taxon.getIdx()), taxon.getName(), parentId)
        for child in taxon.getChildren():
            self.addTaxon(child)

    def onSelectEvent(self, event):
        self.cbkSelectItem(self.getSelectedId())

class TaxonEditor(BaseWidgets.BaseEditor):
    """A widget for editing Pynorpa taxa."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSave):
        """Constructor with save callback."""
        super().__init__(cbkSave)
        self.taxon = None

    def loadData(self, taxon: Taxon):
        """Display the specified object in this editor."""
        self.taxon = taxon
        self.enableWidgets()
        self.txtName.setValue(None)
        self.txtNameFr.setValue(None)
        self.txtRank.setValue(None)
        self.intOrder.setValue(None)
        if taxon:
            self.txtName.setValue(taxon.getName())
            self.txtNameFr.setValue(taxon.getNameFr())
            self.txtRank.setValue(taxon.getRank())
            self.intOrder.setValue(taxon.getOrder())
        self.enableWidgets()

    def hasChanges(self) -> bool:
        """Check if the editor has any changes."""
        if self.taxon:
            if self.taxon.getName() != self.txtName.getValue():
                return True
            if self.taxon.getNameFr() != self.txtNameFr.getValue():
                return True
            if self.taxon.getRank() != self.txtRank.getValue():
                return True
            if self.taxon.getOrder() != self.intOrder.getValue():
                return True
        return False

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        self.cbkSave(self.taxon)

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.taxon)

    def onDelete(self):
        """Delete the edited object."""
        pass

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Taxon Editor')

        # Taxon attributes
        self.txtName     = self.addText('Nom latin')
        self.txtNameFr   = self.addText('Nom français')
        self.txtRank     = self.addText('Rang')
        self.intOrder    = self.addIntInput('Ordre')

        # Buttons: save, cancel, delete
        frmButtons = ttk.Frame(self.frmEdit, padding=5)
        frmButtons.grid(row=self.row, column=0, columnspan=2)
        self.btnSave = tk.Button(frmButtons, text = 'Save', command = self.onSave)
        self.btnSave.grid(row=0, column=0, padx=3)
        self.btnCancel = tk.Button(frmButtons, text = 'Cancel', command = self.onCancel)
        self.btnCancel.grid(row=0, column=1, padx=3)
        self.btnDelete = tk.Button(frmButtons, text = 'Delete', command = self.onCancel)
        self.btnDelete.grid(row=0, column=2, padx=3)

        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.taxon is not None
        modified = self.hasChanges()
        self.txtName.enableWidget(editing)
        self.txtNameFr.enableWidget(editing)
        self.txtRank.enableWidget(editing)
        self.intOrder.enableWidget(editing)
        BaseWidgets.enableWidget(self.btnSave, modified)
        BaseWidgets.enableWidget(self.btnCancel, modified)
        BaseWidgets.enableWidget(self.btnDelete, False)

    def __str__(self) -> str:
        return 'TaxonEditor'
