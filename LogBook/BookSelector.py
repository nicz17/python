"""
A ttk ComboBox to select an existing book.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import glob
import logging
import os
import tkinter as tk
from tkinter import ttk
from LogBook import *


class BookSelector():
    """A ComboBox to select an existing book."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        self.log.info('Constructor')
        self.cbkSelect = cbkSelect

    def loadData(self, book: LogBook):
        """Load existing LogBooks into the comboBox, select the specified book."""
        ext = '.logbook'
        files = sorted(glob.glob(LogBook.dir + f'*{ext}'))
        names = []
        for file in files:
            names.append(os.path.basename(file).replace(ext, ''))
        self.cboBooks['values'] = names
        self.cboBooks.set(book.name)

    def onSelection(self, evt):
        """Callback for ComboBox selection event."""
        selection = self.cboBooks.get()
        self.cbkSelect(selection)

    def build(self, parent: tk.Frame):
        """Add the widgets to the parent frame."""
        frmEdit = ttk.LabelFrame(parent, text='Book Selection')
        frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True, pady=5)

        self.cboBooks = ttk.Combobox(frmEdit, state='readonly', values=[])
        self.cboBooks.pack(fill=tk.X, expand=True, padx=8, pady=5)
        self.cboBooks.bind("<<ComboboxSelected>>", self.onSelection)

