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
        if book is not None:
            self.cboBooks.set(book.name)

    def onSelection(self, evt):
        """Callback for ComboBox selection event."""
        selection = self.cboBooks.get()
        self.cbkSelect(selection)

    def build(self, parent: tk.Frame):
        """Add the widgets to the parent frame."""
        self.frmEdit = ttk.LabelFrame(parent, text='Book Selection')
        self.frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True, pady=5)

        self.cboBooks = ttk.Combobox(self.frmEdit, state='readonly', values=[])
        self.cboBooks.pack(fill=tk.X, expand=True, padx=8, pady=5)
        self.cboBooks.bind("<<ComboboxSelected>>", self.onSelection)
        
    def enableButton(self, btn: ttk.Button, enabled: bool):
        """Enable the specified button if bEnabled is true."""
        if btn:
            if enabled:
                btn['state'] = tk.NORMAL
            else:
                btn['state'] = tk.DISABLED


class BookSelectorMove(BookSelector):
    """Select a book to move a task into."""
    log = logging.getLogger('BookSelectorMove')

    def __init__(self, cbkMove):
        self.cbkMove = cbkMove
        super().__init__(None)

    def onSelection(self, evt):
        selection = self.cboBooks.get()
        self.enableButton(self.btnMove, selection is not None)

    def onMove(self):
        self.cbkMove(self.cboBooks.get())

    def createWidgets(self, parent: tk.Frame):
        """Add the widgets to the parent frame."""
        self.build(parent)
        self.frmEdit.configure(text='Move task to another book')
        self.btnMove = ttk.Button(master=self.frmEdit, text='Move', command=self.onMove)
        self.btnMove.pack(padx=4, pady=2)
        self.enableButton(self.btnMove, False)