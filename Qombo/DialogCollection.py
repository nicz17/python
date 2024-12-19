"""
Tkinter modal dialog to display a Qombit collection.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
from tkinter import font as tkfont
import logging
from ModalDialog import *
from QombitCollection import *
from Qombit import *

class DialogCollection(ModalDialog):
    log = logging.getLogger(__name__)

    def __init__(self, parent: tk.Tk, collec: QombitCollection):
        self.size = 110
        self.nLevels = 9
        self.nRarities = len(OrRarity)
        super().__init__(parent, 'Collection')
        self.collec = collec
        sGeometry = str(self.size * self.nLevels) + 'x' + str(self.nRarities*self.size + 100)
        self.root.geometry(sGeometry)
        self.fontMsg = tkfont.Font(family='Helvetica', size=24, weight='normal')

    def displayKind(self, kind: OrKind):
        """Display collect for the specified qombit kind."""
        self.log.info('Displaying collection for kind %s', kind)
        self.canCollec.delete('all')
        self.drawMissing()
        qombits = []
        for qombit in self.collec.getByKind(kind):
            qombits.append(qombit)
            self.drawQombit(qombit)
        sStatus = f'{kind} qombits in collection: {len(qombits)} of {self.nRarities*self.nLevels}'
        self.lblStatus.configure(text=sStatus)

    def drawQombit(self, qombit: Qombit):
        """Draw the Qombit on the collection canvas."""
        if qombit:
            tx = (qombit.iLevel-1)*self.size + 5
            ty = qombit.oRarity.value*self.size + 5
            id = self.canCollec.create_image(tx, ty, anchor = tk.NW, image = qombit.getImage())
            #self.aQombitIds.append(id)

    def drawMissing(self):
        """Draw question marks on canvas for missing qombits."""
        for x in range(self.nLevels):
            for y in range(self.nRarities):
                tx = (x + 0.5)*self.size
                ty = (y + 0.5)*self.size
                self.canCollec.create_text(tx, ty, text='?', font=self.fontMsg)

    def createWidgets(self):
        self.lblStatus = tk.Label(self.root, text='Qombit collection')
        self.lblStatus.pack(fill='x')

        self.canCollec = tk.Canvas(master=self.root, bg='#c0f0c0', bd=0, 
                                height=self.size*self.nRarities, 
                                width=self.size*self.nLevels, highlightthickness=0)
        self.canCollec.pack()

        self.btnExit = tk.Button(self.root, text='Close', command=self.exit)
        self.btnExit.pack(padx=4, pady=2)