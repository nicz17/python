"""Modal dialog to add a taxon hierarchy using iNat API visually."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025"
__version__ = "1.0.0"


import logging
import tkinter as tk
from tkinter import ttk

from ModalDialog import ModalDialog
from BaseWidgets import Button


class INatTaxonDialog(ModalDialog):
    log = logging.getLogger('INatTaxonDialog')

    def __init__(self, parent: tk.Tk, sTaxonName=None):
        """Constructor."""
        super().__init__(parent, '')
        self.root.geometry('1020x600+300+150')

    def createWidgets(self):

        # Input frame
        self.frmInput = ttk.LabelFrame(self.root, text='Recherche')
        self.btnRequest = Button(self.frmInput, 'Requête', self.exit, 'find')
        self.btnRequest.pack(0)
        self.frmInput.pack(fill=tk.X, padx=3, pady=3)

        # Results frame
        self.frmResult = ttk.LabelFrame(self.root, text='Résultats')
        self.frmResult.pack(fill=tk.X, padx=3, pady=3)

        # Save/cancel buttons
        self.frmButtons = ttk.Frame(self.root)
        self.frmButtons.pack(fill=tk.X, padx=3, pady=10)
        self.btnSave = Button(self.frmButtons, 'Enregistrer', self.exit, 'filesave')
        self.btnExit = Button(self.frmButtons, 'Annuler', self.exit, 'cancel')
        self.btnSave.pack()
        self.btnExit.pack()