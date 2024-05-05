"""
A collection of simple Tk widgets.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk


class IntInput():
    """A integer input widget based on ttk.Entry."""
    log = logging.getLogger('IntInput')

    def __init__(self, cbkModified):
        """Constructor with row selection callback."""
        self.log.info('Constructor')
        self.cbkModified = cbkModified

    def setValue(self, value: int):
        """Set the integer value."""
        self.oEntry.delete(0, tk.END)
        if value:
            self.oEntry.insert(0, str(value))

    def getValue(self):
        """Get the current integer value."""
        value = int(self.oEntry.get(1.0, tk.END).strip())
        return value
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        cmdValidate = (parent.register(self.cbkValidate))
        self.oEntry = ttk.Entry(parent, width=6, validate='all', 
                                validatecommand=(cmdValidate, '%P'))
        self.oEntry.grid(row=row, column=col, padx=5, sticky='w')

    def cbkValidate(self, input: str):
        """Check if input is a digit or empty."""
        return str.isdigit(input) or input == ""