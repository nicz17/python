"""
Tkinter modal dialog to display a Qombit collection.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
from ModalDialog import *

class DialogCollection(ModalDialog):
    log = logging.getLogger(__name__)

    def __init__(self, parent):
        super().__init__(parent, 'Collection')
        self.size = 110
        self.nByKind = 9
        sGeometry = str(self.size * self.nByKind) + 'x' + str(4*self.size)
        self.root.geometry(sGeometry)

    def createWidgets(self):
        #return super().createWidgets()

        self.btnExit = tk.Button(self.root, text='OK', command=self.exit)
        self.btnExit.pack(padx=4, pady=2)