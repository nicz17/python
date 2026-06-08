"""Modal dialog to confirm results of selection file parsing."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026"
__version__ = "1.0.0"


import logging
import tkinter as tk
from tkinter import ttk

import config
import TextTools
from ModalDialog import ModalDialog
from BaseWidgets import Button
from selectionParser import SelectedPhoto
from taxon import TaxonRank, Taxon, TaxonCache
from pynorpaManager import PynorpaManager


class SelectionParsingDialog(ModalDialog):
    log = logging.getLogger('SelectionParsingDialog')

    def __init__(self, parent: tk.Tk, filename: str):
        """Constructor."""
        super().__init__(parent, 'Confirmation de sélection')
        self.root.geometry('1020x600+300+150')
        self.filename = filename
        self.manager = PynorpaManager()
        self.cache = TaxonCache()

    def onSave(self):
        """Copy the selected photos."""
        pass

    def createWidgets(self):
        # Main frame
        self.frmMain = ttk.Frame(self.root)
        self.frmMain.pack(fill=tk.BOTH)

        # Save/cancel buttons
        self.frmButtons = ttk.Frame(self.frmMain)
        self.frmButtons.pack(fill=tk.X, padx=3, pady=10)
        self.btnSave  = Button(self.frmButtons, 'Enregistrer', self.onSave, 'filesave')
        self.btnExit  = Button(self.frmButtons, 'Quitter', self.exit, 'cancel')
        self.btnSave.pack()
        self.btnExit.pack()

    def hasChanges(self):
        """Check if we have photos to select."""
        return False

    def enableWidgets(self):
        self.btnSave.enableWidget(self.hasChanges())