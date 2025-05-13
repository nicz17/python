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
from tkinter import simpledialog as dialog
from pynorpaManager import PynorpaManager, PynorpaException


class ModuleTaxon(TabModule):
    """Pynorpa Module for taxa."""
    log = logging.getLogger('ModuleTaxon')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.parent = parent
        super().__init__(parent, 'Taxons')
        self.cache  = None
        self.taxon  = None
        self.manager = PynorpaManager()
        self.tree   = TaxonTree(self.onSelectTaxon)
        self.editor = TaxonEditor(self.onSaveTaxon)
        self.imageWidget = imageWidget.ImageWidget(f'{config.dirPicsBase}medium/blank.jpg')

    def loadData(self):
        self.cache = TaxonCache()
        self.tree.loadData()
        self.enableWidgets()

    def onSelectTaxon(self, id: str):
        """Callback for selection of taxon with specified id."""
        taxon = None
        if id is not None:
            taxon = self.cache.findById(int(id))
        self.log.info('Selected %s', taxon)
        self.taxon = taxon

        # Display in widgets
        self.editor.loadData(taxon)
        self.imageWidget.loadThumb(taxon.getTypicalPicture() if taxon else None)
        self.enableWidgets()

    def onSaveTaxon(self, taxon: Taxon):
        self.log.info('Saving %s', taxon)
        isNew = taxon.idx < 0
        self.cache.save(taxon)
        self.editor.loadData(taxon)
        if isNew:
            self.tree.addTaxon(taxon)

    def onAddTaxon(self, evt=None):
        """Create a child of the selected taxon and display it in editor."""
        child = self.cache.createChildTaxon(self.taxon)
        self.log.info('Adding child taxon %s', child)
        self.editor.loadData(child)
        self.editor.txtName.oWidget.focus()
        self.imageWidget.loadThumb(None)

    def onAddTaxonINat(self, evt=None):
        name = dialog.askstring('Ajouter un taxon via iNat', "Entrer le nom de l'espèce à ajouter :")
        self.log.info(f'User input: {name}')
        try:
            self.setLoadingIcon()
            self.manager.addTaxonFromINat(name, self)
        except PynorpaException as exc:
            self.setLoadingIcon(True)
            self.parent.showErrorMsg(exc)

    def onSearch(self, evt=None):
        """Search taxon and select it in tree."""
        input = self.txtSearch.get()
        if input and len(input) > 2:
            where = f"taxName like '%{input.replace(' ', '% %')}%'"
            ids = self.cache.fetchFromWhere(where)
            if ids and len(ids) > 0:
                taxon = self.cache.findById(ids[0])
                self.log.info('Found %s', taxon)
                self.tree.setSelection(taxon)
                self.enableWidgets()

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Taxon tree
        self.tree.createWidgets(self.frmLeft)

        # Toolbar
        frmToolbar = ttk.Frame(self.frmLeft)
        self.btnAdd = BaseWidgets.Button(frmToolbar, 'Enfant', self.onAddTaxon, 'add')
        self.btnAdd.pack()
        self.txtSearch = ttk.Entry(frmToolbar, width=18)
        self.txtSearch.pack(side=tk.LEFT, padx=3)
        self.txtSearch.bind('<Return>', self.onSearch)
        self.btnSearch = BaseWidgets.Button(frmToolbar, 'Chercher', self.onSearch, 'find')
        self.btnSearch.pack()
        self.btnReload = BaseWidgets.Button(frmToolbar, None, self.tree.loadData, 'refresh')
        self.btnReload.pack()
        frmToolbar.pack()
        self.btnAddINat = BaseWidgets.Button(self.frmLeft, 'iNat', self.onAddTaxonINat, 'add')
        self.btnAddINat.pack()

        # Editor and image
        self.editor.createWidgets(self.frmRight)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.loadData(None)

    def enableWidgets(self):
        canAdd = (self.taxon and self.taxon.rank != TaxonRank.SPECIES)
        self.btnAdd.enableWidget(canAdd)

class TaxonTree(BaseTree):
    """Subclass of BaseTree displaying taxa."""
    log = logging.getLogger('TaxonTree')

    def __init__(self, cbkSelectItem):
        super().__init__(self.onSelectEvent)
        self.cbkSelectItem = cbkSelectItem
        self.cache = None

    def addTaxon(self, taxon: Taxon):
        """Adds a taxon and its children to the tree."""
        parentId = None
        if taxon.getIdxParent() is not None:
            parentId = str(taxon.getIdxParent())
        tag = None #f'taxon-rank{taxon.getRank().value}'
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

    def loadData(self):
        if not self.cache:
            self.cache = TaxonCache()
        self.clear()
        for tax in self.cache.getTopLevelTaxa():
            self.addTaxon(tax)
        self.log.info(f'Reloaded with {self.size()} taxa')
        self.log.info(f'Cache has {self.cache.size()} taxa')

    def onSelectEvent(self, event):
        self.cbkSelectItem(self.getSelectedId())

    def setSelection(self, taxon: Taxon):
        """Set the tree selection to the specified taxon."""
        if taxon:
            iid = str(taxon.getIdx())
            self.tree.see(iid)
            self.tree.focus(iid)
            self.tree.selection_set(iid)

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

    def onSave(self, evt=None):
        """Save changes to the edited object."""
        self.taxon.setName(self.txtName.getValue())
        self.taxon.setNameFr(self.txtNameFr.getValue())
        self.taxon.setOrder(self.intOrder.getValue())
        self.taxon.setTypical(self.chkTypical.getValue())

        # Fill fr name from latin name if empty
        if not self.taxon.nameFr:
            self.taxon.nameFr = self.taxon.name

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
        self.txtParent   = self.addTextReadOnly('Parent', Taxon.getParentName)
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
