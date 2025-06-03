"""Modal dialog to add a taxon hierarchy using iNat API visually."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025"
__version__ = "1.0.0"


import logging
import tkinter as tk
from tkinter import ttk

import config
import TextTools
from ModalDialog import ModalDialog
from BaseWidgets import Button
from iNatApiRequest import INatApiRequest
from taxon import TaxonRank, Taxon, TaxonCache
from pynorpaManager import PynorpaManager


class INatTaxonDialog(ModalDialog):
    log = logging.getLogger('INatTaxonDialog')

    def __init__(self, parent: tk.Tk, sTaxonName=None):
        """Constructor."""
        super().__init__(parent, 'Ajouter des taxons via iNaturalist')
        self.root.geometry('1020x600+300+150')
        self.manager = PynorpaManager()
        self.cache = TaxonCache()
        self.req = INatApiRequest()
        self.taxa = []

    def queryINat(self, name: str):
        """Query the iNat API about the named taxon."""
        self.setStatus(f'Requête à iNat pour {name} ...')
        self.setLoadingIcon()
        inatTaxon = self.req.getTaxonFromName(name)
        if not inatTaxon:
            self.log.error(f'Failed to find iNat id for taxon name {name}')
            self.setStatus(f'iNat ne connait pas {name}')
        else:
            self.log.info(f'Found {inatTaxon}')
            self.setStatus(f'Trouvé {inatTaxon}')
            taxon = self.cache.createFromINatTaxon(inatTaxon, -1)
            self.displayTaxon(taxon)
            self.root.update()
            self.queryAncestors(inatTaxon.id)
            self.taxa.append(taxon)
        self.setLoadingIcon(False)
        self.enableWidgets()

    def queryAncestors(self, inatId: int):
        """Query the ancestors of an iNat taxon."""
        ancestors = self.req.getAncestors(inatId)
        if ancestors is None or len(ancestors) == 0:
            self.log.error(f'Failed to find iNat ancestors for {inatId}')
            self.setStatus(f'iNat ne trouve pas la hiérarchie de {inatId})')
            return
        
        # Loop over ancestors, look if already in Panorpa DB
        self.log.info(f'Found {len(ancestors)} ancestors')
        idxParent = None
        for ancestor in ancestors:
            self.log.info(ancestor)
            taxon = self.cache.findByName(ancestor.name)
            if taxon:
                self.log.info(f'  Found: {taxon}')
                idxParent = taxon.idx
            else:
                taxon = self.cache.createFromINatTaxon(ancestor, idxParent)
                self.log.info(f'  Missing: {taxon}')
                idxParent = taxon.idx
            self.taxa.append(taxon)
            self.displayTaxon(taxon)

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
            self.queryINat(input)

    def onReset(self):
        """Reset the results grid."""
        self.taxa = []
        self.txtEntry.delete(0, tk.END)
        self.setStatus('Entrez le nom du taxon à ajouter')
        for rank in TaxonRank:
            iRank = rank.value
            self.icons[iRank] = None
            self.lblName[iRank].configure(text='')
            self.lblNameFr[iRank].configure(text='')
            self.lblIcon[iRank].configure(image=None)
        self.enableWidgets()
        self.txtEntry.focus()

    def onSave(self):
        """Save the new taxa to database."""
        self.log.info(f'Saving new taxa from {len(self.taxa)} taxa')
        self.data = self.manager.saveINatTaxa(self.taxa, self.setStatus)
        self.taxa = []
        self.enableWidgets()

    def displayTaxon(self, taxon: Taxon):
        """Display the taxon in the results table."""
        if not taxon:
            return
        iRank = taxon.rank.value
        iconName = 'ok' if taxon.idx > 0 else 'filesave'
        icon = tk.PhotoImage(file=f'{config.dirIcons}{iconName}.png')
        self.icons[iRank] = icon
        self.lblName[iRank].configure(text=taxon.getName())
        self.lblNameFr[iRank].configure(text=taxon.getNameFr())
        self.lblIcon[iRank].configure(image=icon)
        self.displayTaxon(taxon.parent)

    def setStatus(self, msg: str):
        """Set our status message."""
        self.lblStatus.configure(text=msg)
        #self.root.update()  # no, blocks init

    def hasChanges(self):
        """Check if we have new taxa to save."""
        if self.taxa is not None:
            for taxon in self.taxa:
                if taxon.idx < 0:
                    return True
        return False

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
        self.lblIcon = []
        self.icons = []
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
            lblIcon = ttk.Label(self.frmResult)
            lblIcon.grid(column=3, row=iRank, padx=6)
            self.lblIcon.append(lblIcon)
            self.icons.append(None)

        # Save/cancel buttons
        self.frmButtons = ttk.Frame(self.frmMain)
        self.frmButtons.pack(fill=tk.X, padx=3, pady=10)
        self.btnSave  = Button(self.frmButtons, 'Enregistrer', self.onSave, 'filesave')
        self.btnExit  = Button(self.frmButtons, 'Annuler', self.exit, 'cancel')
        self.btnReset = Button(self.frmButtons, 'Reset', self.onReset, 'refresh')
        self.btnSave.pack()
        self.btnExit.pack()
        self.btnReset.pack()

        self.onReset()

    def enableWidgets(self):
        self.btnSave.enableWidget(self.hasChanges())