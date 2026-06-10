"""Modal dialog to confirm results of selection file parsing."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026"
__version__ = "1.0.0"


import logging
import tkinter as tk
from tkinter import ttk

from ModalDialog import ModalDialog
from BaseWidgets import Button
from BaseTable import AdvTable, TableColumn
from selectionParser import SelectedPhoto


class SelectionParsingDialog(ModalDialog):
    log = logging.getLogger('SelectionParsingDialog')

    def __init__(self, parent: tk.Tk, filename: str, selections: list[SelectedPhoto]):
        """Constructor."""
        self.filename = filename
        self.selections = selections
        super().__init__(parent, 'Confirmation de sélection')
        self.root.geometry('900x640+300+150')
        self.data = False

    def loadData(self):
        total = len(self.selections)
        errors = 0
        for sel in self.selections:
            if sel.getError():
                errors +=1
        self.setStatus(f'Lu {total} photos, {errors} erreurs')
        self.tblSel.loadData(self.selections)

    def onSave(self):
        """Copy the selected photos."""
        self.data = True
        self.exit()

    def setStatus(self, msg: str):
        """Set our status message."""
        self.lblStatus.configure(text=msg)

    def createWidgets(self):
        # Main frame
        self.frmMain = ttk.Frame(self.root)
        self.frmMain.pack(fill=tk.BOTH)
        self.lblStatus = ttk.Label(self.frmMain, text='Status')
        self.lblStatus.pack()

        # Table of results
        self.tblSel = TableSelectedPhoto(None)
        self.tblSel.createWidgets(self.frmMain)

        # Save/cancel buttons
        self.frmButtons = ttk.Frame(self.frmMain)
        self.frmButtons.pack(fill=tk.X, padx=3, pady=10)
        self.btnSave  = Button(self.frmButtons, 'Enregistrer', self.onSave, 'filesave')
        self.btnExit  = Button(self.frmButtons, 'Quitter',     self.exit,   'cancel')
        self.btnSave.pack()
        self.btnExit.pack()


class TableSelectedPhoto(AdvTable):
    """Table widget for selected photos."""
    log = logging.getLogger("TableSelectedPhotos")

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        super().__init__(cbkSelect, 'Sélections', 6)
        self.addColumn(TableColumn('No',                SelectedPhoto.getId,         50))
        self.addColumn(TableColumn('Saisie',            SelectedPhoto.getInput,     150))
        self.addColumn(TableColumn('Sélectionné sous',  SelectedPhoto.getSummary,   400))
        self.addColumn(TableColumn('Taxon',             SelectedPhoto.getTaxonName, 200))

    def loadData(self, data: list[SelectedPhoto]):
        """Display the specified selections in this table."""
        self.log.info(f'Loading {len(data)} SelectedPhotos')
        self.clear()
        self.data = data
        self.addRows(data)

        # Set error style on rows
        self.tree.tag_configure('error-row', foreground='#e00000')
        for idx, sel in enumerate(data):
            if sel.hasError():
                self.tree.item(idx, tags='error-row')

    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        super().createWidgets(parent, 25)
