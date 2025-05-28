"""Modal dialog to add a taxon hierarchy using iNat API visually."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025"
__version__ = "1.0.0"


import logging
import tkinter as tk
from tkinter import ttk

import TextTools
from ModalDialog import ModalDialog
from BaseWidgets import Button
from taxon import TaxonRank, Taxon, TaxonCache


class INatTaxonDialog(ModalDialog):
    log = logging.getLogger('INatTaxonDialog')

    def __init__(self, parent: tk.Tk, sTaxonName=None):
        """Constructor."""
        super().__init__(parent, 'Ajouter des taxons via iNaturalist')
        self.root.geometry('1020x600+300+150')
        self.cache = TaxonCache()

    def onSearch(self):
        """Callback for search button."""
        input = TextTools.upperCaseFirst(self.txtEntry.get().strip())
        self.log.info(f'Searching for {input}')
        self.lblStatus.configure(text=f'Recherche de {input}')
        taxon = None
        if input:
            taxon = self.cache.findByName(input)
        if taxon:
            self.log.info(f'Found {taxon}')
            self.setStatus(f'Existe en DB: {taxon}')
            self.displayTaxon(taxon)
        else:
            self.setStatus(f'Pas de résultats pour {input}')
            # TODO query iNat API

    def onReset(self):
        """Reset the results grid."""
        self.txtEntry.delete(0, tk.END)
        self.setStatus('Entrez le nom du taxon à ajouter')
        for rank in TaxonRank:
            iRank = rank.value
            self.lblName[iRank].configure(text='')
            self.lblNameFr[iRank].configure(text='')
        self.enableWidgets()
        self.txtEntry.focus()

    def displayTaxon(self, taxon: Taxon):
        """Display the taxon in the results table."""
        if not taxon:
            return
        iRank = taxon.rank.value
        self.lblName[iRank].configure(text=taxon.getName())
        self.lblNameFr[iRank].configure(text=taxon.getNameFr())
        self.displayTaxon(taxon.parent)

    def setStatus(self, msg: str):
        self.lblStatus.configure(text=msg)

    def createWidgets(self):
        # Main frame
        self.frmMain = ttk.Frame(self.root)
        self.frmMain.pack(fill=tk.BOTH)

        # Input frame
        self.frmInput = ttk.LabelFrame(self.frmMain, text='Recherche')
        self.frmInput.pack(fill=tk.X, padx=3, pady=3)
        self.txtEntry = tk.Entry(self.frmInput, width=50)
        self.txtEntry.grid(column=0, row=0)
        self.btnRequest = Button(self.frmInput, 'Requête', self.onSearch, 'find')
        self.btnRequest.grid(0, 1)
        self.lblStatus = ttk.Label(self.frmInput, text='Status')
        self.lblStatus.grid(column=0, row=1, columnspan=2)

        # Results frame
        self.frmResult = ttk.LabelFrame(self.frmMain, text='Résultats')
        self.frmResult.pack(fill=tk.X, padx=3, pady=3)

        self.lblName = []
        self.lblNameFr = []
        for rank in TaxonRank:
            iRank = rank.value
            lblRank = ttk.Label(self.frmResult, text=rank.getNameFr())
            lblRank.grid(column=0, row=iRank, padx=4)
            lblName = ttk.Label(self.frmResult, text='Nom latin')
            lblName.grid(column=1, row=iRank, padx=6)
            self.lblName.append(lblName)
            lblNameFr = ttk.Label(self.frmResult, text='Nom français')
            lblNameFr.grid(column=2, row=iRank, padx=6)
            self.lblNameFr.append(lblNameFr)
            # TODO add icons

        # Save/cancel buttons
        self.frmButtons = ttk.Frame(self.frmMain)
        self.frmButtons.pack(fill=tk.X, padx=3, pady=10)
        self.btnSave  = Button(self.frmButtons, 'Enregistrer', self.exit, 'filesave')
        self.btnExit  = Button(self.frmButtons, 'Annuler', self.exit, 'cancel')
        self.btnReset = Button(self.frmButtons, 'Reset', self.onReset, 'refresh')
        self.btnSave.pack()
        self.btnExit.pack()
        self.btnReset.pack()

        self.onReset()

    def enableWidgets(self):
        self.btnSave.enableWidget(False)