"""
 Pynorpa Module for displaying and editing taxa.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
from TabsApp import *
from BaseTree import *
import BaseWidgets
import imageWidget
from taxon import Taxon, TaxonCache, TaxonRank


class ModuleTaxon(TabModule):
    """Pynorpa Module for taxa."""
    log = logging.getLogger('ModuleTaxon')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        super().__init__(parent, 'Taxons')
        self.cache  = None
        self.tree   = TaxonTree(self.onSelectTaxon)
        self.editor = TaxonEditor(self.onSaveTaxon)
        self.imageWidget = imageWidget.ImageWidget(f'{config.dirPicsBase}medium/blank.jpg')

    def loadData(self):
        self.cache  = TaxonCache()
        for tax in self.cache.getTopLevelTaxa():
            self.tree.addTaxon(tax)

    def onSelectTaxon(self, id: str):
        """Callback for selection of taxon with specified id."""
        taxon = None
        if id is not None:
            taxon = self.cache.findById(int(id))
        self.log.info('Selected %s', taxon)

        # Display in widgets
        self.editor.loadData(taxon)
        if taxon:
            self.imageWidget.loadThumb(taxon.getTypicalPicture())
        else:
            self.imageWidget.loadThumb(None)

    def onSaveTaxon(self, taxon: Taxon):
        pass

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Taxon tree and editor
        self.tree.createWidgets(self.frmLeft)
        self.editor.createWidgets(self.frmRight)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.loadData(None)


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
        tag = f'taxon-rank{taxon.getRank().value}'
        text = taxon.getName()
        if len(taxon.getChildren()) > 0:
            text += f' ({len(taxon.getChildren())})'
        self.addItem(str(taxon.getIdx()), text, parentId, tag)
        for child in taxon.getChildren():
            self.addTaxon(child)

    def createWidgets(self, parent: tk.Frame):
        super().createWidgets(parent)
        for rank in TaxonRank:
            self.tree.tag_configure(f'taxon-rank{rank.value}', background=rank.getColor())

    def onSelectEvent(self, event):
        self.cbkSelectItem(self.getSelectedId())


class TaxonEditor(BaseWidgets.BaseEditor):
    """A widget for editing Pynorpa taxa."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSave):
        """Constructor with save callback."""
        super().__init__(cbkSave, '#62564f')
        self.taxon = None

    def loadData(self, taxon: Taxon):
        """Display the specified object in this editor."""
        self.taxon = taxon
        self.setValue(taxon)

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        self.cbkSave(self.taxon)

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.taxon)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Taxon Editor')

        # Taxon attributes
        self.txtName     = self.addText('Nom latin',      Taxon.getName)
        self.txtNameFr   = self.addText('Nom français',   Taxon.getNameFr)
        self.txtRank     = self.addTextReadOnly('Rang',   Taxon.getRankFr)
        self.intOrder    = self.addIntInput('Ordre',      Taxon.getOrder)
        self.chkTypical  = self.addCheckBox('Taxon type', Taxon.getTypical, 'Taxon type du parent')

        # Buttons: save, cancel, delete
        self.createButtons(True, True, False)
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.taxon is not None
        modified = self.hasChanges(self.taxon)
        super().enableWidgets(editing)
        self.enableButtons(modified, modified, False)

    def __str__(self) -> str:
        return 'TaxonEditor'
