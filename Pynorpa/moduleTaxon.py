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
from iNatTaxonDialog import INatTaxonDialog
from uploader import Uploader


class ModuleTaxon(TabModule):
    """Pynorpa Module for taxa."""
    log = logging.getLogger('ModuleTaxon')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.parent = parent
        super().__init__(parent, 'Taxons', Taxon.__name__)
        self.cache  = None
        self.taxon  = None
        self.manager = PynorpaManager()
        self.uploader = Uploader()
        self.tree   = TaxonTree(self.onSelectTaxon)
        self.editor = TaxonEditor(self.onSaveTaxon)
        self.imageWidget = imageWidget.CaptionImageWidget(f'{config.dirPicsBase}medium/blank.jpg')

    def loadData(self):
        self.cache = TaxonCache()
        self.tree.loadData()
        self.enableWidgets()

    def navigateToObject(self, taxon: Taxon):
        self.tree.setSelection(taxon)

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

    def onAddTaxonINatDialog(self):
        """Show dialog to add a taxon and its hierarchy using iNaturalist API."""
        dlg = INatTaxonDialog(self.window)
        self.log.info('Opened dialog window, waiting')
        self.window.wait_window(dlg.root)
        self.log.info(f'Dialog closed with data: {dlg.data}')
        taxon = dlg.data
        if taxon:
            self.tree.loadData()
            self.tree.setSelection(taxon)

    def onUpload(self):
        """Upload the selected taxon page."""
        if self.taxon:
            self.uploader.uploadSingleTaxon(self.taxon)

    def onSearch(self, search: str):
        """Search bar callback. Search taxon and select it in tree."""
        if search and len(search) > 2:
            where = f"taxName like '%{search.replace(' ', '% %')}%'"
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
        self.btnAdd.pack(0)
        self.searchBar = BaseWidgets.SearchBar(frmToolbar, 32, self.onSearch)
        self.btnReload = BaseWidgets.IconButton(frmToolbar, 'refresh', 'Recharger les taxons', self.tree.loadData, 6)
        self.btnCollapse = BaseWidgets.IconButton(frmToolbar, 'undo', 'Tout fermer', self.tree.closeAll, 6)
        frmToolbar.pack(fill=tk.X)
        frmToolbar2 = ttk.Frame(self.frmLeft)
        self.btnAddINat = BaseWidgets.Button(frmToolbar2, 'iNat', self.onAddTaxonINatDialog, 'add')
        self.btnAddINat.pack(0)
        self.btnUpload = BaseWidgets.Button(frmToolbar2, 'Publier', self.onUpload, 'go-up')
        self.btnUpload.pack(0)
        frmToolbar2.pack(fill=tk.X)

        # Editor and image
        self.editor.createWidgets(self.frmRight)
        self.imageWidget.createWidgets(self.frmRight)
        self.editor.loadData(None)

    def enableWidgets(self):
        """Enable or disable the buttons."""
        canAdd    = (self.taxon and self.taxon.rank != TaxonRank.SPECIES)
        canUpload = (self.uploader.getTaxonPage(self.taxon) is not None)
        self.btnAdd.enableWidget(canAdd)
        self.btnUpload.enableWidget(canUpload)

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

    def closeAll(self):
        """Close all tree nodes."""
        for node in self.tree.get_children():
            self.tree.item(node, open=False)

class TaxonEditor(BaseWidgets.BaseEditor):
    """A widget for editing Pynorpa taxa."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSave):
        """Constructor with save callback."""
        super().__init__(cbkSave, '#62564f')
        self.manager = PynorpaManager()
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

    def onDelete(self):
        """Delete the edited object."""
        self.manager.deleteTaxon(self.taxon, False)
        self.loadData(None)

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
        # TODO add number of pictures with navigation

        # Buttons: save, cancel, delete
        self.createButtons(True, True, True)
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing   = self.taxon is not None
        modified  = self.hasChanges(self.taxon)
        deletable = self.manager.canDeleteTaxon(self.taxon)
        super().enableWidgets(editing)
        self.enableButtons(modified, modified, deletable)

    def __str__(self) -> str:
        return f'TaxonEditor for {self.taxon}'
